import streamlit as st
import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

st.set_page_config(page_title="تدريب النموذج", layout="wide")
st.title("✨ صفحة تدريب النموذج على بيانات الأعطال")

DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

st.subheader("1️⃣ رفع ملفات البيانات الأصلية (قبل إضافة record_id)")
sensor_file = st.file_uploader("ارفع ملف الحساسات الأصلي", type="csv", key="sensor")
carset_file = st.file_uploader("ارفع ملف الأعطال الأصلي", type="csv", key="carset")

if sensor_file and carset_file:
    sensor_df = pd.read_csv(sensor_file)
    carset_df = pd.read_csv(carset_file)
    st.success("✅ تم رفع الملفين بنجاح")
    st.write("معاينة ملف الحساسات:")
    st.dataframe(sensor_df.head())
    st.write("معاينة ملف الأعطال:")
    st.dataframe(carset_df.head())

    if st.button("➕ أضف عمود record_id تلقائيًا"):
        sensor_df["record_id"] = range(1, len(sensor_df) + 1)
        carset_df["record_id"] = range(1, len(carset_df) + 1)
        st.success("✅ تم إضافة عمود record_id للملفين")

    if st.button("💾 احفظ الملفات المعدلة يدويًا"):
        sensor_df.to_csv(os.path.join(DATA_DIR, "sensor_with_id.csv"), index=False)
        carset_df.to_csv(os.path.join(DATA_DIR, "carset_with_id.csv"), index=False)
        st.success("✅ تم حفظ الملفات المعدلة داخل مجلد data")

st.markdown("---")
st.subheader("2️⃣ رفع الملفات المعدّلة (بعد إضافة record_id) للدمج")

sensor_with_id = st.file_uploader("ارفع ملف الحساسات المعدل", type="csv", key="sensor_id")
carset_with_id = st.file_uploader("ارفع ملف الأعطال المعدل", type="csv", key="carset_id")

if sensor_with_id and carset_with_id:
    sensor_id_df = pd.read_csv(sensor_with_id)
    carset_id_df = pd.read_csv(carset_with_id)
    if st.button("🔗 دمج الملفين بناءً على record_id"):
        try:
            merged_df = pd.merge(sensor_id_df, carset_id_df, on="record_id", how="inner")
            st.dataframe(merged_df.head())
            st.success("✅ تم الدمج بنجاح")

            if st.button("💾 احفظ ملف الدمج يدويًا"):
                merged_path = os.path.join(DATA_DIR, "merged_data.csv")
                merged_df.to_csv(merged_path, index=False)
                st.success("✅ تم حفظ ملف الدمج داخل data/merged_data.csv")

        except Exception as e:
            st.error(f"❌ حدث خطأ أثناء الدمج: {e}")

st.markdown("---")
st.subheader("3️⃣ رفع ملف الدمج للتدريب")

merged_upload = st.file_uploader("ارفع ملف الدمج النهائي للتدريب", type="csv", key="merged")

if merged_upload:
    merged_df = pd.read_csv(merged_upload)
    st.success("✅ تم رفع ملف الدمج بنجاح")
    st.dataframe(merged_df.head())

    st.subheader("4️⃣ ابدأ التدريب على البيانات")
    if st.button("🚀 ابدأ التدريب"):
        try:
            X = merged_df.drop(columns=["fault_code", "record_id"])
            y = merged_df["fault_code"]

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            model = RandomForestClassifier()
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            report = classification_report(y_test, y_pred)

            st.success("✅ تم التدريب بنجاح")
            st.code(report)

            if st.button("💾 احفظ نتائج التقييم يدويًا"):
                with open(os.path.join(DATA_DIR, "model_results.txt"), "w") as f:
                    f.write(report)
                st.success("✅ تم حفظ نتائج التقييم")

        except Exception as e:
            st.error(f"❌ حدث خطأ أثناء التدريب: {e}")