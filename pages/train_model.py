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

رفع الملفين

sensor_file = st.file_uploader("📤 ارفع ملف بيانات الحساسات (Sensor Data)", type=["csv"], key="sensor") carset_file = st.file_uploader("📤 ارفع ملف بيانات الأعطال (Carset Data)", type=["csv"], key="carset")

if sensor_file and carset_file: sensor_df = pd.read_csv(sensor_file) carset_df = pd.read_csv(carset_file)

# زرار إضافة عمود ID
if st.button("➕ إضافة عمود record_id للملفات"):
    sensor_df.insert(0, 'record_id', range(1, 1 + len(sensor_df)))
    carset_df.insert(0, 'record_id', range(1, 1 + len(carset_df)))

    sensor_df.to_csv("data/sensor_with_id.csv", index=False)
    carset_df.to_csv("data/carset_with_id.csv", index=False)

    st.success("✅ تم إضافة العمود record_id وحفظ الملفات بنجاح")

# زرار بدء التدريب
if st.button("🚀 ابدأ التدريب"):
    try:
        # دمج الملفات بناءً على record_id
        merged_df = pd.merge(sensor_df, carset_df, on="record_id", how="inner")
        merged_df.to_csv("data/merged_training_data.csv", index=False)

        st.info("🔄 تم دمج البيانات وحفظ الملف بنجاح")

        # تجهيز البيانات
        X, y = prepare_training_data(sensor_df, carset_df)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # تدريب النموذج
        model = train_and_save_model(X_train, y_train, model_path="model/fault_model.pkl")

        # التقييم
        y_pred = model.predict(X_test)
        report = classification_report(y_test, y_pred)
        matrix = confusion_matrix(y_test, y_pred)

        st.success("✅ تم تدريب النموذج بنجاح")

        # عرض التقييم
        st.subheader("📊 تقرير التقييم")
        st.text(report)

        fig, ax = plt.subplots()
        sns.heatmap(matrix, annot=True, fmt="d", cmap="Blues", ax=ax)
        ax.set_title("مصفوفة الالتباس")
        ax.set_xlabel("التوقع")
        ax.set_ylabel("الحقيقي")
        st.pyplot(fig)

        # حفظ التقرير نصيًا
        with open("data/evaluation_report.txt", "w") as f:
            f.write(report)

        # تحميل الملفات الناتجة
        st.subheader("📥 تحميل الملفات الناتجة")
        with open("model/fault_model.pkl", "rb") as f:
            st.download_button("⬇️ تحميل النموذج المدرب", f, file_name="fault_model.pkl")
        with open("data/merged_training_data.csv", "rb") as f:
            st.download_button("⬇️ تحميل ملف البيانات بعد الدمج", f, file_name="merged_training_data.csv")
        with open("data/evaluation_report.txt", "rb") as f:
            st.download_button("⬇️ تحميل تقرير التقييم", f, file_name="evaluation_report.txt")

    except Exception as e:
        st.error(f"❌ حدث خطأ أثناء التدريب: {e}")

else: st.warning("⚠️ من فضلك ارفع الملفين للبدء")

