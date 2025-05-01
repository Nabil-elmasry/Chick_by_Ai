
import streamlit as st
import pandas as pd

st.set_page_config(page_title="دمج الملفات", layout="centered")

st.title("دمج ملفات Carset و Sensor Dataset")

carset_file = st.file_uploader("ارفع ملف Carset", type=["csv"], key="carset")
sensor_file = st.file_uploader("ارفع ملف Sensor Dataset", type=["csv"], key="sensor")

if carset_file and sensor_file:
    try:
        carset_df = pd.read_csv(carset_file)
        sensor_df = pd.read_csv(sensor_file)

        # إنشاء عمود record_id في الملفين
        carset_df["record_id"] = range(1, len(carset_df) + 1)
        sensor_df["record_id"] = range(1, len(sensor_df) + 1)

        # دمج الملفين
        merged_df = pd.merge(carset_df, sensor_df, on="record_id", how="inner")

        st.success("تم دمج الملفين بنجاح!")

        st.subheader("عرض البيانات المدموجة")
        st.dataframe(merged_df)

        # زر لتحميل الملف المدموج
        csv = merged_df.to_csv(index=False).encode("utf-8")
        st.download_button("تحميل الملف المدموج", csv, "merged_dataset.csv", "text/csv")

    except Exception as e:
        st.error(f"حدث خطأ أثناء المعالجة: {e}")
else:
    st.info("يرجى رفع الملفين لإجراء الدمج.")
