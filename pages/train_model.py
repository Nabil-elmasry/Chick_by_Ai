# pages/train_model.py

import streamlit as st
from modules.data_loader import load_sensor_data, load_carset
from modules.preprocessing import prepare_training_data
from modules.model import train_and_save_model
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix
import os

st.set_page_config(page_title="📊 تدريب النموذج", layout="wide")
st.title("📊 تدريب نموذج تنبؤ الأعطال")

sensor_file = st.file_uploader("تحميل ملف قراءات الحساسات (sensor data)", type=["csv"])
carset_file = st.file_uploader("تحميل ملف Carset (به الأكواد المستهدفة)", type=["csv"])

# خطوة 1: زر لإضافة عمود ID
if st.button("إضافة عمود ID تلقائيًا"):
    if sensor_file and carset_file:
        try:
            sensor_df = pd.read_csv(sensor_file)
            carset_df = pd.read_csv(carset_file)

            sensor_df["record_id"] = range(1, len(sensor_df) + 1)
            carset_df["record_id"] = range(1, len(carset_df) + 1)

            os.makedirs("data", exist_ok=True)
            sensor_path = "data/sensor_with_id.csv"
            carset_path = "data/carset_with_id.csv"
            sensor_df.to_csv(sensor_path, index=False)
            carset_df.to_csv(carset_path, index=False)

            st.success("تم إضافة عمود ID وحفظ الملفات الجديدة بنجاح.")
            st.info(f"تم الحفظ: {sensor_path}, {carset_path}")
            st.session_state["ready_for_training"] = True
        except Exception as e:
            st.error(f"حدث خطأ أثناء إضافة العمود: {e}")
    else:
        st.warning("يرجى رفع الملفين أولاً.")

# خطوة 2: زر التدريب
if st.session_state.get("ready_for_training"):
    if st.button("ابدأ التدريب"):
        try:
            sensor_df = pd.read_csv("data/sensor_with_id.csv")
            carset_df = pd.read_csv("data/carset_with_id.csv")

            # الدمج والإعداد
            X, y, merged_df = prepare_training_data(sensor_df, carset_df)
            merged_df.to_csv("data/training_data_log.csv", index=False)
            st.success("تم حفظ الملف المدمج للتدريب.")

            # تدريب النموذج
            model = train_and_save_model(X, y)

            # التقييم
            y_pred = model.predict(X)
            report = classification_report(y, y_pred, output_dict=False)
            matrix = confusion_matrix(y, y_pred)

            with open("data/evaluation_report.txt", "w", encoding="utf-8") as f:
                f.write(report)

            st.subheader("تقرير دقة التوقع")
            st.text(report)
            st.success("تم حفظ تقرير التقييم.")

            # رسم مصفوفة الالتباس
            st.subheader("مصفوفة الالتباس")
            fig, ax = plt.subplots()
            sns.heatmap(matrix, annot=True, fmt='d', cmap='Blues', ax=ax)
            st.pyplot(fig)

        except Exception as e:
            st.error(f"حدث خطأ أثناء التدريب: {e}")