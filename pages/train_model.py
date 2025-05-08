import streamlit as st import pandas as pd import os from sklearn.model_selection import train_test_split from sklearn.ensemble import RandomForestClassifier from sklearn.metrics import classification_report

st.set_page_config(page_title="تدريب النموذج", layout="wide") st.title("✨ صفحة تدريب النموذج على بيانات الأعطال")

DATA_DIR = "data" MERGED_FILE = os.path.join(DATA_DIR, "merged_data.csv") MODEL_RESULTS = os.path.join(DATA_DIR, "model_results.txt")

if not os.path.exists(DATA_DIR): os.makedirs(DATA_DIR)

الخطوة 1: رفع الملفات الأصلية

st.subheader("1️⃣ رفع الملفات الأصلية (قبل تعديل record_id)") sensor_file = st.file_uploader("ارفع ملف الحساسات الأصلي", type="csv", key="sensor") carset_file = st.file_uploader("ارفع ملف الأعطال الأصلي (carset)", type="csv", key="carset")

حفظ يدوي للملفات الأصلية

if sensor_file and carset_file: if st.button("💾 حفظ الملفات الأصلية"): sensor_df = pd.read_csv(sensor_file) carset_df = pd.read_csv(carset_file)

sensor_df.to_csv(os.path.join(DATA_DIR, "sensor.csv"), index=False)
    carset_df.to_csv(os.path.join(DATA_DIR, "carset.csv"), index=False)
    st.success("✅ تم حفظ الملفات الأصلية داخل مجلد data")

الخطوة 2: رفع الملفات بعد تعديل record_id

st.subheader("2️⃣ رفع الملفات بعد إضافة عمود record_id") sensor_file_id = st.file_uploader("ارفع ملف الحساسات بعد التعديل", type="csv", key="sensor_id") carset_file_id = st.file_uploader("ارفع ملف الأعطال بعد التعديل", type="csv", key="carset_id")

حفظ يدوي للملفات المعدلة

if sensor_file_id and carset_file_id: if st.button("💾 حفظ الملفات المعدلة"): sensor_df_id = pd.read_csv(sensor_file_id) carset_df_id = pd.read_csv(carset_file_id)

sensor_df_id.to_csv(os.path.join(DATA_DIR, "sensor_id.csv"), index=False)
    carset_df_id.to_csv(os.path.join(DATA_DIR, "carset_id.csv"), index=False)
    st.success("✅ تم حفظ الملفات المعدلة داخل مجلد data")

الخطوة 3: الدمج بعد رفع الملفات المعدلة

if os.path.exists(os.path.join(DATA_DIR, "sensor_id.csv")) and os.path.exists(os.path.join(DATA_DIR, "carset_id.csv")): st.subheader("3️⃣ دمج الملفات المعدلة") if st.button("🔗 دمج الملفات بناء على record_id"): try: sensor_df = pd.read_csv(os.path.join(DATA_DIR, "sensor_id.csv")) carset_df = pd.read_csv(os.path.join(DATA_DIR, "carset_id.csv")) merged_df = pd.merge(sensor_df, carset_df, on="record_id", how="inner") st.dataframe(merged_df.head()) merged_df.to_csv(MERGED_FILE, index=False) st.success("✅ تم الدمج والحفظ في data/merged_data.csv") except Exception as e: st.error(f"❌ حدث خطأ أثناء الدمج: {e}")

الخطوة 4: رفع ملف الدمج

st.subheader("4️⃣ تأكيد ملف الدمج") uploaded_merged = st.file_uploader("ارفع ملف الدمج (أو استخدم المحفوظ)", type="csv", key="merged")

if uploaded_merged or os.path.exists(MERGED_FILE): if uploaded_merged: merged_df = pd.read_csv(uploaded_merged) else: merged_df = pd.read_csv(MERGED_FILE)

st.success("✅ تم تحميل ملف الدمج")
st.dataframe(merged_df.head())

# الخطوة 5: بدء التدريب
st.subheader("5️⃣ بدء التدريب")
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
        st.text("نتائج التقييم:")
        st.code(report)

        if st.button("💾 احفظ نتائج التقييم"):
            with open(MODEL_RESULTS, "w") as f:
                f.write(report)
            st.success("✅ تم حفظ نتائج التقييم في model_results.txt")

    except Exception as e:
        st.error(f"❌ حدث خطأ أثناء التدريب: {e}")

else: st.warning("⚠️ من فضلك ارفع ملف الدمج أو تأكد من وجود merged_data.csv قبل بدء التدريب.")

