#final project 

import streamlit as st
import pdfplumber
import pandas as pd
import re
import os
import shutil
import datetime

st.set_page_config(page_title="تشخيص الأعطال", layout="wide")
st.title("AI Car Diagnosis - Sensor & Fault Analyzer")

# ======= زر مسح الملف والذاكرة =======
st.sidebar.subheader("تنظيف البيانات")
if st.sidebar.button("حذف جميع البيانات"):
    try:
        if os.path.exists("Carset.csv"):
            os.remove("Carset.csv")
        if os.path.exists("backup"):
            shutil.rmtree("backup")
        st.session_state.clear()
        st.sidebar.success("تم الحذف الكامل للبيانات.")
    except Exception as e:
        st.sidebar.error(f"حدث خطأ أثناء الحذف: {e}")

# ======= دوال =======
def extract_text_from_pdf(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        return "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())

def extract_dtcs(text):
    dtcs = []
    for line in text.split("\n"):
        match = re.search(r"(P\d{4})", line)
        if match:
            code = match.group(1)
            desc = line.replace(code, "").strip(" :-–")
            dtcs.append([code, desc.strip()])
        elif line.strip():
            dtcs.append(["No Code", line.strip()])
    return dtcs

def extract_sensor_data(text):
    sensors = []
    for line in text.split("\n"):
        parts = line.strip().split()
        if len(parts) >= 4:
            name = " ".join(parts[:-3])
            value, standard, unit = parts[-3], parts[-2], parts[-1]
            sensors.append([name, value, standard, unit])
    return pd.DataFrame(sensors, columns=["Sensor", "Value", "Standard", "Unit"])

# ======= الواجهة =======
sensor_files = st.file_uploader("ارفع تقارير الحساسات (PDF)", type="pdf", accept_multiple_files=True)
code_file = st.file_uploader("ارفع تقرير الأعطال (PDF)", type="pdf")

if sensor_files and code_file:
    sensor_text = "".join([extract_text_from_pdf(file) for file in sensor_files])
    code_text = extract_text_from_pdf(code_file)

    df_sensors = extract_sensor_data(sensor_text)
    dtcs = extract_dtcs(code_text)
    df_dtcs = pd.DataFrame(dtcs, columns=["Code", "Description"])

    st.subheader("بيانات الحساسات")
    st.dataframe(df_sensors)

    st.subheader("أكواد الأعطال")
    st.dataframe(df_dtcs)

    matches = []
    for _, dtc_row in df_dtcs.iterrows():
        for _, sensor_row in df_sensors.iterrows():
            if sensor_row["Sensor"].lower() in dtc_row["Description"].lower():
                try:
                    value = float(sensor_row["Value"])
                    standard = float(sensor_row["Standard"])
                    deviation = abs(value - standard) / standard * 100 if standard != 0 else 0
                    status = "High Deviation" if deviation > 15 else "OK"
                except:
                    deviation = "N/A"
                    status = "Cannot Evaluate"

                matches.append([
                    dtc_row["Code"], dtc_row["Description"],
                    sensor_row["Sensor"], sensor_row["Value"],
                    sensor_row["Standard"], sensor_row["Unit"],
                    f"{deviation:.1f}%" if isinstance(deviation, float) else deviation,
                    status
                ])

    if matches:
        df_matches = pd.DataFrame(matches, columns=[
            "Code", "Description", "Sensor", "Value", "Standard", "Unit", "Deviation %", "Status"
        ])
        st.success("تم التحليل بنجاح")
        st.dataframe(df_matches)

    if st.button("احفظ البيانات"):
        try:
            os.makedirs("backup", exist_ok=True)
            if os.path.exists("Carset.csv"):
                now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                shutil.copyfile("Carset.csv", f"backup/backup_{now}.csv")

            sensor_dict = {row['Sensor']: row['Value'] for _, row in df_sensors.iterrows()}
            sensor_dict["Fault Codes"] = ', '.join(df_dtcs["Code"].tolist())
            new_df = pd.DataFrame([sensor_dict])

            if os.path.exists("Carset.csv"):
                existing_df = pd.read_csv("Carset.csv")
                final_df = pd.concat([existing_df, new_df], ignore_index=True)
            else:
                final_df = new_df

            final_df.to_csv("Carset.csv", index=False)
            st.success("تم حفظ البيانات في Carset.csv")
        except Exception as e:
            st.error(f"حدث خطأ أثناء الحفظ: {e}")
