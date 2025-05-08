import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

st.set_page_config(page_title="تدريب النموذج", layout="wide")
st.title("✨ تدريب النموذج على بيانات الأعطال")

st.subheader("1️⃣ رفع الملفات المعدّلة (بعد إضافة record_id)")

sensor_with_id = st.file_uploader("ارفع ملف الحساسات المعدّل", type="csv", key="sensor_id")
carset_with_id = st.file_uploader("ارفع ملف الأعطال المعدّل", type="csv", key="carset_id")

if sensor_with_id and carset_with_id:
    try:
        sensor_df = pd.read_csv(sensor_with_id)
        carset_df = pd.read_csv(carset_with_id)

        # توحيد الأسماء للتأكد من تطابق العمود
        sensor_df.rename(columns=lambda x: x.strip().lower(), inplace=True)
        carset_df.rename(columns=lambda x: x.strip().lower(), inplace=True)

        st.success("✅ تم رفع الملفين بنجاح")
        st.write("معاينة ملف الحساسات:")
        st.dataframe(sensor_df.head())
        st.write("معاينة ملف الأعطال:")
        st.dataframe(carset_df.head())

        if st.button("🔗 دمج الملفين بناءً على record_id"):
            if "record_id" in sensor_df.columns and "record_id" in carset_df.columns:
                merged_df = pd.merge(sensor_df, carset_df, on="record_id", how="inner")
                st.success("✅ تم الدمج بنجاح")
                st.dataframe(merged_df.head())

                # حفظ يدوي لملف الدمج
                csv = merged_df.to_csv(index=False).encode('utf-8-sig')
                st.download_button(
                    label="💾 تحميل ملف الدمج",
                    data=csv,
                    file_name="merged_data.csv",
                    mime="text/csv"
                )
            else:
                st.error("❌ العمود 'record_id' غير موجود في أحد الملفين")

    except Exception as e:
        st.error(f"❌ خطأ أثناء الدمج: {e}")

st.markdown("---")
st.subheader("2️⃣ رفع ملف الدمج للتدريب")

merged_file = st.file_uploader("ارفع ملف الدمج النهائي", type="csv", key="merged_file")
if merged_file:
    try:
        df = pd.read_csv(merged_file)
        df.rename(columns=lambda x: x.strip().lower(), inplace=True)

        st.success("✅ تم رفع ملف الدمج بنجاح")
        st.dataframe(df.head())

        if st.button("🚀 ابدأ التدريب"):
            if "fault_codes" in df.columns:
                X = df.drop(columns=["fault_codes", "record_id"])
                y = df["fault_codes"]

                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                model = RandomForestClassifier()
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                report = classification_report(y_test, y_pred)

                st.success("✅ تم التدريب بنجاح")
                st.code(report)

                # حفظ يدوي للتقرير
                st.download_button(
                    label="💾 تحميل نتائج التقييم",
                    data=report,
                    file_name="evaluation_report.txt"
                )
            else:
                st.error("❌ العمود 'fault_codes' غير موجود في الملف")
    except Exception as e:
        st.error(f"❌ خطأ أثناء التدريب: {e}")