import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import base64
import fitz  # PyMuPDF
import io

st.set_page_config(page_title="كشف انحراف قراءات الحساسات", page_icon="📉", layout="wide")
st.title("📉 تحليل انحراف قراءات الحساسات من تقرير PDF")

# رفع النموذج المدرب
model_file = st.file_uploader("📤 ارفع ملف النموذج المدرب (.pkl)", type=["pkl"])

# رفع تقرير PDF
uploaded_file = st.file_uploader("📤 ارفع تقرير PDF يحتوي على قراءات الحساسات", type=["pdf"])

# اختيار الحد الحرج
threshold = st.slider("📏 اختر الحد الحرج للانحراف", min_value=0.0, max_value=1.0, value=0.5, step=0.01)

# دالة استخراج البيانات من PDF
def extract_sensor_data_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    sensor_data = {}
    for page in doc:
        text = page.get_text()
        lines = text.split("\n")
        for line in lines:
            if ":" in line:
                try:
                    key, value = line.split(":", 1)
                    value = value.strip().split(" ")[0]
                    sensor_data[key.strip()] = float(value)
                except:
                    continue
    doc.close()
    return pd.DataFrame([sensor_data])

# تنفيذ التحليل
if model_file and uploaded_file:
    try:
        model = joblib.load(io.BytesIO(model_file.read()))
        df_input = extract_sensor_data_from_pdf(uploaded_file)

        st.success("✅ تم استخراج بيانات الحساسات من التقرير")
        st.dataframe(df_input)

        model_features = model.feature_names_in_
        missing_cols = [col for col in model_features if col not in df_input.columns]

        if missing_cols:
            st.warning(f"⚠️ الحقول التالية مفقودة: {missing_cols}")
        else:
            df_input = df_input[model_features]
            prediction = model.predict_proba(df_input)[:, 0]
            deviation_score = 1 - prediction[0]

            st.markdown(f"### 🔍 درجة الانحراف: **{deviation_score:.2f}** (الحد الحرج: {threshold})")

            # رسم بياني
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.bar(df_input.columns, df_input.values[0], color='orange')
            ax.axhline(y=threshold, color='red', linestyle='--', label='الحد الحرج')
            ax.set_title("قراءات الحساسات من السيارة", fontsize=14)
            ax.set_ylabel("القيمة")
            ax.tick_params(axis='x', rotation=45)
            ax.legend()
            st.pyplot(fig)

            # توليد تقرير
            report_text = f"تقرير الانحراف:\n\nدرجة الانحراف: {deviation_score:.2f}\nالحد الحرج: {threshold}\n"
            if deviation_score > threshold:
                report_text += "⚠️ يوجد انحراف ملحوظ عن القيم الطبيعية.\n"
            else:
                report_text += "✅ القيم تقع ضمن النطاق الطبيعي.\n"

            st.subheader("📄 تقرير نصي")
            st.code(report_text)

            b64 = base64.b64encode(report_text.encode()).decode()
            href = f'<a href="data:file/txt;base64,{b64}" download="sensor_deviation_report.txt">⬇️ تحميل التقرير</a>'
            st.markdown(href, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ حدث خطأ أثناء التحليل: {e}")