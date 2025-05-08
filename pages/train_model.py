import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import base64

st.set_page_config(page_title="تدريب النموذج", layout="wide")
st.title("✨ صفحة تدريب النموذج على بيانات الأعطال")

# --- الخطوة 1: رفع الملفات الأصلية ---
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
        st.success("✅ تم إضافة العمود")

        # حفظ يدوي
        sensor_csv = sensor_df.to_csv(index=False).encode('utf-8')
        carset_csv = carset_df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ تحميل ملف الحساسات المعدل", sensor_csv, "sensor_with_id.csv", "text/csv")
        st.download_button("⬇️ تحميل ملف الأعطال المعدل", carset_csv, "carset_with_id.csv", "text/csv")

# --- الخطوة 2: رفع الملفات المعدلة ---
st.markdown("---")
st.subheader("2️⃣ رفع الملفات المعدّلة (بعد إضافة record_id) للدمج")

sensor_with_id = st.file_uploader("ارفع ملف الحساسات المعدل", type="csv", key="sensor_id")
carset_with_id = st.file_uploader("ارفع ملف الأعطال المعدل", type="csv", key="carset_id")

if sensor_with_id and carset_with_id:
    sensor_id_df = pd.read_csv(sensor_with_id)
    carset_id_df = pd.read_csv(carset_with_id)

    if st.button("🔗 دمج الملفين بناءً على record_id"):
        merged_df = pd.merge(sensor_id_df, carset_id_df, on="record_id", how="inner")
        st.success("✅ تم الدمج بنجاح")
        st.dataframe(merged_df.head())

        # حفظ يدوي
        merged_csv = merged_df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ تحميل ملف الدمج", merged_csv, "merged_data.csv", "text/csv")

# --- الخطوة 3: رفع ملف الدمج للتدريب ---
st.markdown("---")
st.subheader("3️⃣ رفع ملف الدمج للتدريب")

merged_upload = st.file_uploader("ارفع ملف الدمج النهائي للتدريب", type="csv", key="merged")

if merged_upload:
    merged_df = pd.read_csv(merged_upload)
    st.success("✅ تم رفع ملف الدمج بنجاح")
    st.dataframe(merged_df.head())

    # --- الخطوة 4: تدريب النموذج ---
    st.subheader("4️⃣ ابدأ التدريب على البيانات")
    if st.button("🚀 ابدأ التدريب"):
        try:
            X = merged_df.drop(columns=["fault_code", "record_id"])
            y = merged_df["fault_code"]

            from sklearn.model_selection import train_test_split
            from sklearn.ensemble import RandomForestClassifier
            from sklearn.metrics import classification_report

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            model = RandomForestClassifier()
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            report = classification_report(y_test, y_pred)

            st.success("✅ تم التدريب بنجاح")
            st.code(report)

            # حفظ يدوي للتقرير
            report_bytes = io.BytesIO()
            report_bytes.write(report.encode("utf-8"))
            report_bytes.seek(0)
            st.download_button("⬇️ تحميل تقرير التقييم", report_bytes, "model_results.txt", "text/plain")

        except Exception as e:
            st.error(f"❌ خطأ أثناء التدريب: {e}")