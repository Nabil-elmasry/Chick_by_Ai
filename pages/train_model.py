import streamlit as st
import pandas as pd
import os
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from modules.preprocessing import prepare_training_data
from modules.model import train_and_save_model

st.title("🚗 تدريب نموذج التنبؤ بالأعطال")

# إنشاء مجلد data إذا لم يكن موجودًا
os.makedirs("data", exist_ok=True)
os.makedirs("model", exist_ok=True)

# رفع الملفات
sensor_file = st.file_uploader("📤 ارفع ملف بيانات الحساسات (Sensor Data)", type=["csv"], key="sensor")
carset_file = st.file_uploader("📤 ارفع ملف بيانات الأعطال (Carset Data)", type=["csv"], key="carset")

# خطوة 1: إضافة record_id وحفظ الملفات
if sensor_file and carset_file:
    sensor_df = pd.read_csv(sensor_file)
    carset_df = pd.read_csv(carset_file)

    if st.button("➕ إضافة record_id وحفظ الملفات"):
        sensor_df.insert(0, 'record_id', range(1, 1 + len(sensor_df)))
        carset_df.insert(0, 'record_id', range(1, 1 + len(carset_df)))

        sensor_df.to_csv("data/sensor_with_id.csv", index=False)
        carset_df.to_csv("data/carset_with_id.csv", index=False)

        st.success("✅ تم إضافة record_id وحفظ الملفين بنجاح")

        st.session_state["ready_to_merge"] = True  # تحديد جاهزية الدمج

# خطوة 2: زر الدمج يظهر بعد الحفظ
if st.session_state.get("ready_to_merge", False):
    if st.button("🔗 دمج الملفين وحفظ الملف المدموج"):
        try:
            sensor_df = pd.read_csv("data/sensor_with_id.csv")
            carset_df = pd.read_csv("data/carset_with_id.csv")
            merged_df = pd.merge(sensor_df, carset_df, on="record_id", how="inner")
            merged_df.to_csv("data/merged_training_data.csv", index=False)
            st.success("✅ تم الدمج وحفظ الملف بنجاح")
            st.session_state["ready_to_train"] = True
        except Exception as e:
            st.error(f"❌ خطأ أثناء الدمج: {e}")

# خطوة 3: التدريب بعد الدمج
if st.session_state.get("ready_to_train", False):
    if st.button("🚀 ابدأ التدريب"):
        try:
            sensor_df = pd.read_csv("data/sensor_with_id.csv")
            carset_df = pd.read_csv("data/carset_with_id.csv")
            X, y = prepare_training_data(sensor_df, carset_df)
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            model = train_and_save_model(X_train, y_train, model_path="model/fault_model.pkl")

            y_pred = model.predict(X_test)
            report = classification_report(y_test, y_pred)
            matrix = confusion_matrix(y_test, y_pred)

            st.success("✅ تم تدريب النموذج بنجاح")

            st.subheader("📊 تقرير التقييم")
            st.text(report)

            fig, ax = plt.subplots()
            sns.heatmap(matrix, annot=True, fmt="d", cmap="Blues", ax=ax)
            ax.set_title("🧮 مصفوفة الالتباس")
            ax.set_xlabel("التوقع")
            ax.set_ylabel("الحقيقي")
            st.pyplot(fig)

            with open("data/evaluation_report.txt", "w") as f:
                f.write(report)

            st.subheader("📥 تحميل الملفات الناتجة")
            with open("model/fault_model.pkl", "rb") as f:
                st.download_button("⬇️ تحميل النموذج المدرب", f, file_name="fault_model.pkl")
            with open("data/merged_training_data.csv", "rb") as f:
                st.download_button("⬇️ تحميل ملف البيانات بعد الدمج", f, file_name="merged_training_data.csv")
            with open("data/evaluation_report.txt", "rb") as f:
                st.download_button("⬇️ تحميل تقرير التقييم", f, file_name="evaluation_report.txt")

        except Exception as e:
            st.error(f"❌ حدث خطأ أثناء التدريب: {e}")