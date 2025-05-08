import streamlit as st
import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import base64

st.set_page_config(page_title="تدريب النموذج", layout="wide")
st.title("✨ صفحة تدريب النموذج على بيانات الأعطال")

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
        st.success("✅ تم إضافة العمود بنجاح")

    if st.button("💾 احفظ ملفات record_id يدويًا"):
        for df, name in [(sensor_df, "sensor_with_id.csv"), (carset_df, "carset_with_id.csv")]:
            csv = df.to_csv(index=False).encode()
            b64 = base64.b64encode(csv).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="{name}">⬇️ اضغط هنا لتحميل {name}</a>'
            st.markdown(href, unsafe_allow_html=True)

st.markdown("---")
st.subheader("2️⃣ رفع الملفات المعدلة (بعد إضافة record_id)")

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
                csv = merged_df.to_csv(index=False).encode()
                b64 = base64.b64encode(csv).decode()
                href = f'<a href="data:file/csv;base64,{b64}" download="merged_data.csv">⬇️ اضغط هنا لتحميل merged_data.csv</a>'
                st.markdown(href, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ خطأ أثناء الدمج: {e}")

st.markdown("---")
st.subheader("3️⃣ رفع ملف الدمج النهائي للتدريب")

merged_upload = st.file_uploader("ارفع ملف الدمج النهائي للتدريب", type="csv", key="merged")

if merged_upload:
    merged_df = pd.read_csv(merged_upload)
    st.success("✅ تم رفع ملف الدمج بنجاح")
    st.dataframe(merged_df.head())

    st.subheader("4️⃣ ابدأ التدريب على البيانات")
    if st.button("🚀 ابدأ التدريب"):
        try:
            if "Fault Codes" not in merged_df.columns:
                raise ValueError("عمود 'Fault Codes' غير موجود!")

            X = merged_df.drop(columns=["Fault Codes", "record_id"])
            y = merged_df["Fault Codes"]

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            model = RandomForestClassifier()
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            report = classification_report(y_test, y_pred)

            st.success("✅ تم التدريب بنجاح")
            st.code(report)

            if st.button("💾 احفظ نتائج التقييم يدويًا"):
                b64 = base64.b64encode(report.encode()).decode()
                href = f'<a href="data:file/txt;base64,{b64}" download="model_results.txt">⬇️ اضغط هنا لتحميل model_results.txt</a>'
                st.markdown(href, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ حدث خطأ أثناء التدريب: {e}")