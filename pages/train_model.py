
import streamlit as st
import pandas as pd
import base64
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

def convert_df_to_download_link(df, filename):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">⬇️ اضغط هنا لتحميل الملف: {filename}</a>'
    return href

st.set_page_config(page_title="تدريب النموذج", layout="wide")
st.title("✨ تدريب النموذج على بيانات الأعطال (يدوي بالكامل)")

# --- الخطوة 1: رفع الملفات الأصلية ---
st.subheader("1️⃣ رفع ملفات البيانات الأصلية")
sensor_file = st.file_uploader("ارفع ملف الحساسات", type="csv")
carset_file = st.file_uploader("ارفع ملف الأعطال", type="csv")

if sensor_file and carset_file:
    sensor_df = pd.read_csv(sensor_file)
    carset_df = pd.read_csv(carset_file)
    st.success("✅ تم رفع الملفين")
    st.dataframe(sensor_df.head())
    st.dataframe(carset_df.head())

    if st.button("➕ أضف عمود record_id"):
        sensor_df["record_id"] = range(1, len(sensor_df)+1)
        carset_df["record_id"] = range(1, len(carset_df)+1)
        st.success("✅ تم إضافة record_id")

        # رابط تحميل يدوي حقيقي
        st.markdown(convert_df_to_download_link(sensor_df, "sensor_with_id.csv"), unsafe_allow_html=True)
        st.markdown(convert_df_to_download_link(carset_df, "carset_with_id.csv"), unsafe_allow_html=True)