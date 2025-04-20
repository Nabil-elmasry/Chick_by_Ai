
pages/diagnosis.py

import streamlit as st
import pdfplumber
import pandas as pd
import re
import os

st.set_page_config(page_title="AI Car Diagnosis", layout="wide")
st.title("AI Car Diagnosis - Final Sensor-Fault Analyzer")

# ======= دوال استخراج البيانات =======
def extract_text_from_pdf(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        text = ""
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text() + "\n"
    return text

def extract_dtcs(text):
    lines = text.split('\n')
    dtcs = []
    for line in lines:
        match = re.search(r"(P\d{4})", line)
        if match:
            code = match.group(1)
            desc = line.replace(code, "").strip(" :-–")
            dtcs.append([code, desc.strip()])
        elif line.strip():
            dtcs.append(["No Code", line.strip()])
    return dtcs

def extract_sensor_data(text):
    lines = text.split('\n')
    sensors = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) >= 4:
            name = ' '.join(parts[:-3])
            value = parts[-3]
            standard = parts[-2]
            unit = parts[-1]
            sensors.append([name, value, standard, unit])
    return pd.DataFrame(sensors, columns=["Sensor", "Value", "Standard", "Unit"])

# ======= واجهة رفع الملفات =======
sensor_files = st.file_uploader("Upload One or More Sensor Reports (PDF)", type="pdf", accept_multiple_files=True)
code_file = st.file_uploader("Upload Fault Report (PDF)", type="pdf")

if sensor_files and code_file:
    sensor_text = ""
    for file in sensor_files:
        sensor_text += extract_text_from_pdf(file)

    code_text = extract_text_from_pdf(code_file)

    df_sensors = extract_sensor_data(sensor_text)
    dtcs = extract_dtcs(code_text)
    df_dtcs = pd.DataFrame(dtcs, columns=["Code", "Description"])

    st.subheader("1. Extracted Sensor Data")
    st.dataframe(df_sensors)

    st.subheader("2. Extracted Fault Codes")
    st.dataframe(df_dtcs)

    st.subheader("3. Sensor-Fault Matching & Deviation Analysis")
    matches = []
    for _, dtc_row in df_dtcs.iterrows():
        for _, sensor_row in df_sensors.iterrows():
            if sensor_row["Sensor"].lower() in dtc_row["Description"].lower():
                try:
                    value = float(sensor_row["Value"])
                    standard = float(sensor_row["Standard"])
                    deviation_percent = abs(value - standard) / standard * 100 if standard != 0 else 0
                    status = "High Deviation" if deviation_percent > 15 else "OK"
                except:
                    deviation_percent = "N/A"
                    status = "Cannot Evaluate"

                matches.append([
                    dtc_row["Code"],
                    dtc_row["Description"],
                    sensor_row["Sensor"],
                    sensor_row["Value"],
                    sensor_row["Standard"],
                    sensor_row["Unit"],
                    f"{deviation_percent:.1f}%" if isinstance(deviation_percent, float) else deviation_percent,
                    status
                ])

    if matches:
        df_matches = pd.DataFrame(matches, columns=[
            "Code", "Fault Description", "Sensor", "Value", "Standard", "Unit", "Deviation %", "Status"
        ])
        st.success("Sensor deviation analysis completed:")
        st.dataframe(df_matches)
    else:
        st.info("No direct match or deviation detected.")

    # ======= زر يدوي لحفظ وتحميل البيانات =======
    st.subheader("4. حفظ البيانات يدويًا")
    if st.button("احفظ البيانات الحالية"):
        try:
            sensor_dict = {row['Sensor']: row['Value'] for _, row in df_sensors.iterrows()}
            sensor_dict['Fault Codes'] = ','.join(df_dtcs['Code'].tolist())
            new_case_df = pd.DataFrame([sensor_dict])

            csv_filename = "Carset.csv"

            if os.path.exists(csv_filename):
                existing_df = pd.read_csv(csv_filename)
                final_df = pd.concat([existing_df, new_case_df], ignore_index=True)
            else:
                final_df = new_case_df

            final_df.to_csv(csv_filename, index=False)
            st.success("تم حفظ البيانات في Carset.csv")

            # زر التحميل
            with open(csv_filename, "rb") as f:
                st.download_button(
                    label="Download Carset.csv",
                    data=f,
                    file_name="Carset.csv",
                    mime="text/csv"
                )

        except Exception as e:
            st.error(f"Error saving data: {e}")

else:
    st.warning("Please upload one or more sensor PDF reports and a fault code report to proceed.")

