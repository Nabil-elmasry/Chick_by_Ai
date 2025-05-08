import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import base64

st.set_page_config(page_title="تدريب النموذج", layout="wide")
st.title("✨ تدريب نموذج الكشف عن الأعطال - خطوات منظمة")

# ===== 1️⃣ رفع الملفات الأصلية =====
st.header("1️⃣ رفع الملفات الأصلية (بدون record_id)")
sensor_file = st.file_uploader("ارفع ملف الحساسات الأصلي", type="csv", key="sensor_original")
carset_file = st.file_uploader("ارفع ملف الأعطال الأصلي", type="csv", key="carset_original")

if sensor_file and carset_file:
    sensor_df = pd.read_csv(sensor_file)
    carset_df = pd.read_csv(carset_file)
    st.success("✅ تم رفع الملفين بنجاح")
    st.dataframe(sensor_df.head())
    st.dataframe(carset_df.head())

    if st.button("➕ أضف عمود record_id"):
        sensor_df["record_id"] = range(1, len(sensor_df) + 1)
        carset_df["record_id"] = range(1, len(carset_df) + 1)
        st.success("✅ تم إضافة عمود record_id")

        # حفظ يدوي - روابط تحميل
        def download_link(df, filename, label):
            csv = df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{label}</a>'
            return href

        st.markdown(download_link(sensor_df, "sensor_with_id.csv", "📥 تحميل ملف الحساسات المعدل"), unsafe_allow_html=True)
        st.markdown(download_link(carset_df, "carset_with_id.csv", "📥 تحميل ملف الأعطال المعدل"), unsafe_allow_html=True)

# ===== 2️⃣ رفع الملفات بعد التعديل =====
st.header("2️⃣ رفع الملفات المعدّلة (بها record_id)")
sensor_id_file = st.file_uploader("ارفع ملف الحساسات المعدل", type="csv", key="sensor_id")
carset_id_file = st.file_uploader("ارفع ملف الأعطال المعدل", type="csv", key="carset_id")

if sensor_id_file and carset_id_file:
    sensor_id_df = pd.read_csv(sensor_id_file)
    carset_id_df = pd.read_csv(carset_id_file)

    if st.button("🔗 دمج الملفين"):
        merged_df = pd.merge(sensor_id_df, carset_id_df, on="record_id", how="inner")
        st.success("✅ تم الدمج بنجاح")
        st.dataframe(merged_df.head())

        # حفظ يدوي لملف الدمج
        st.markdown(download_link(merged_df, "merged_data.csv", "📥 تحميل ملف الدمج"), unsafe_allow_html=True)

# ===== 3️⃣ رفع ملف الدمج =====
st.header("3️⃣ رفع ملف الدمج النهائي")
merged_file = st.file_uploader("ارفع ملف الدمج النهائي", type="csv", key="merged_final")

if merged_file:
    merged_df = pd.read_csv(merged_file)
    st.success("✅ تم رفع الملف")
    st.dataframe(merged_df.head())

    # ===== 4️⃣ المعالجة Processing =====
    st.header("4️⃣ المعالجة (Processing)")
    if st.button("⚙️ تنفيذ المعالجة"):
        try:
            # التأكد من الأعمدة
            if "fault_code" not in merged_df.columns or "record_id" not in merged_df.columns:
                st.error("❌ تأكد من وجود الأعمدة المطلوبة: fault_code, record_id")
            else:
                X = merged_df.drop(columns=["fault_code", "record_id"])
                y = merged_df["fault_code"]
                st.success("✅ تمت معالجة البيانات بنجاح")
                st.dataframe(X.head())

                # ===== 5️⃣ التدريب =====
                st.header("5️⃣ تدريب النموذج")
                if st.button("🚀 ابدأ التدريب"):
                    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                    model = RandomForestClassifier()
                    model.fit(X_train, y_train)
                    y_pred = model.predict(X_test)
                    report = classification_report(y_test, y_pred)
                    st.success("✅ تم تدريب النموذج بنجاح")
                    st.code(report)

                    # حفظ يدوي للتقرير
                    b64_report = base64.b64encode(report.encode()).decode()
                    st.markdown(f'<a href="data:file/txt;base64,{b64_report}" download="model_results.txt">📥 تحميل تقرير التقييم</a>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ خطأ في المعالجة أو التدريب: {e}")