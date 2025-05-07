import streamlit as st import pandas as pd import os from sklearn.model_selection import train_test_split from sklearn.ensemble import RandomForestClassifier from sklearn.metrics import classification_report

st.set_page_config(page_title="تدريب النموذج", layout="wide") st.title("✨ صفحة تدريب النموذج على بيانات الأعطال")

DATA_DIR = "data" MERGED_FILE = os.path.join(DATA_DIR, "merged_data.csv") MODEL_RESULTS = os.path.join(DATA_DIR, "model_results.txt")

خطوة 1: رفع الملفات

st.subheader("1️⃣ رفع ملفات البيانات") sensor_file = st.file_uploader("ارفع ملف الحساسات", type="csv", key="sensor") carset_file = st.file_uploader("ارفع ملف الأعطال (carset)", type="csv", key="carset")

if not os.path.exists(DATA_DIR): os.makedirs(DATA_DIR)

حفظ يدوي للملفات

if sensor_file and carset_file: st.success("تم رفع الملفين بنجاح!") if st.button("💾 حفظ الملفات يدويًا"): sensor_df = pd.read_csv(sensor_file) carset_df = pd.read_csv(carset_file)

sensor_df.to_csv(os.path.join(DATA_DIR, "sensor.csv"), index=False)
    carset_df.to_csv(os.path.join(DATA_DIR, "carset.csv"), index=False)
    st.success("✅ تم حفظ الملفات بنجاح داخل مجلد data")

# زر الدمج
if os.path.exists(os.path.join(DATA_DIR, "sensor.csv")) and os.path.exists(os.path.join(DATA_DIR, "carset.csv")):
    st.subheader("2️⃣ دمج الملفين")
    if st.button("🔗 دمج الملفين بناء على record_id"):
        try:
            sensor_df = pd.read_csv(os.path.join(DATA_DIR, "sensor.csv"))
            carset_df = pd.read_csv(os.path.join(DATA_DIR, "carset.csv"))
            merged_df = pd.merge(sensor_df, carset_df, on="record_id", how="inner")
            st.dataframe(merged_df.head())
            merged_df.to_csv(MERGED_FILE, index=False)
            st.success("✅ تم الدمج والحفظ في data/merged_data.csv")
        except Exception as e:
            st.error(f"❌ حدث خطأ أثناء الدمج: {e}")

رفع ملف الدمج قبل التدريب

st.subheader("3️⃣ تأكيد ملف الدمج") uploaded_merged = st.file_uploader("ارفع ملف الدمج (أو استخدم المحفوظ)", type="csv", key="merged")

if uploaded_merged or os.path.exists(MERGED_FILE): if uploaded_merged: merged_df = pd.read_csv(uploaded_merged) else: merged_df = pd.read_csv(MERGED_FILE)

st.success("✅ تم تحميل ملف الدمج")
st.dataframe(merged_df.head())

# بدء التدريب
st.subheader("4️⃣ بدء التدريب")
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

