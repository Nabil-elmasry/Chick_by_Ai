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
import traceback

st.set_page_config(page_title="📊 تدريب النموذج", layout="wide")
st.title("📊 تدريب نموذج تنبؤ الأعطال")

sensor_file = st.file_uploader("تحميل ملف الحساسات (sensor.csv)", type=["csv"])
carset_file = st.file_uploader("تحميل ملف carset.csv", type=["csv"])

# مسارات الحفظ
os.makedirs("data", exist_ok=True)
sensor_path = "data/sensor_with_id.csv"
carset_path = "data/carset_with_id.csv"
merged_path = "data/training_data_log.csv"
eval_path = "data/evaluation_report.txt"

# زر إضافة عمود ID
if st.button("1️⃣ إضافة عمود ID تلقائيًا"):
    if sensor_file and carset_file:
        try:
            sensor_df = pd.read_csv(sensor_file)
            carset_df = pd.read_csv(carset_file)

            sensor_df["record_id"] = range(1, len(sensor_df) + 1)
            carset_df["record_id"] = range(1, len(carset_df) + 1)

            sensor_df.to_csv(sensor_path, index=False)
            carset_df.to_csv(carset_path, index=False)

            st.success("تمت إضافة عمود ID وحفظ الملفات.")
            st.download_button("⬇️ تحميل sensor_with_id.csv", sensor_df.to_csv(index=False), file_name="sensor_with_id.csv")
            st.download_button("⬇️ تحميل carset_with_id.csv", carset_df.to_csv(index=False), file_name="carset_with_id.csv")
            st.session_state["ready_for_training"] = True

        except Exception as e:
            st.error("حدث خطأ أثناء إضافة العمود.")
            st.exception(e)
    else:
        st.warning("يرجى رفع الملفين.")

# زر التدريب
if st.session_state.get("ready_for_training"):
    if st.button("2️⃣ ابدأ التدريب"):
        try:
            sensor_df = pd.read_csv(sensor_path)
            carset_df = pd.read_csv(carset_path)

            # إعداد البيانات ودمجها
            X, y, merged_df = prepare_training_data(sensor_df, carset_df)
            merged_df.to_csv(merged_path, index=False)
            st.success("تم حفظ ملف الدمج.")
            st.download_button("⬇️ تحميل ملف الدمج", merged_df.to_csv(index=False), file_name="merged_training_data.csv")

            # تدريب النموذج
            model = train_and_save_model(X, y)

            # التقييم
            y_pred = model.predict(X)
            report = classification_report(y, y_pred, output_dict=False)
            matrix = confusion_matrix(y, y_pred)

            with open(eval_path, "w", encoding="utf-8") as f:
                f.write(report)

            st.success("تم حفظ تقرير التقييم.")
            st.download_button("⬇️ تحميل تقرير التقييم", report, file_name="evaluation_report.txt")

            # عرض التقرير والمصفوفة
            st.subheader("تقرير الدقة:")
            st.text(report)

            st.subheader("مصفوفة الالتباس:")
            fig, ax = plt.subplots()
            sns.heatmap(matrix, annot=True, fmt='d', cmap='YlGnBu', ax=ax)
            st.pyplot(fig)

        except Exception as e:
            st.error("حدث خطأ أثناء التدريب:")
            st.code(traceback.format_exc())  # عرض الخطأ بالتفصيل