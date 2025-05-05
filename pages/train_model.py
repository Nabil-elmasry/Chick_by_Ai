# pages/train_model.py

import streamlit as st
from modules.data_loader import load_sensor_data, load_carset
from modules.preprocessing import prepare_training_data
from modules.model import train_and_save_model, evaluate_model
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="📊 تدريب النموذج", layout="wide")

st.title("📊 تدريب نموذج تنبؤ الأعطال")
st.write(
    """
    في هذه الصفحة يمكنك رفع ملف قراءات الحساسات للتدريب وملف Carset لاستخراج العلامات (Fault Codes)،
    ثم تدريب نموذج الـ Random Forest وحفظه تلقائيًا.
    """
)

# رفع ملفات CSV
sensor_file = st.file_uploader(
    "1. ارفع ملف الحساسات (sensor dataset)", type=["csv"], key="sensor_file"
)
carset_file = st.file_uploader(
    "2. ارفع ملف Carset (carset.csv)", type=["csv"], key="carset_file"
)

if st.button("🚀 ابدأ التدريب"):
    if sensor_file is None or carset_file is None:
        st.error("❌ الرجاء رفع كلا الملفين قبل البدء بالتدريب.")
    else:
        with st.spinner("⏳ جاري تحميل وتنظيف البيانات..."):
            # تحميل البيانات
            sensor_df = load_sensor_data(sensor_file)
            carset_df = load_carset(carset_file)
        st.success("✅ تم تحميل البيانات وتنظيفها بنجاح.")

        with st.spinner("⏳ جاري إعداد بيانات التدريب..."):
            X, y = prepare_training_data(sensor_df, carset_df)
        st.success(f"✅ تم تجهيز مجموعة التدريب ({X.shape[0]} عينة، {X.shape[1]} ميزة).")

        with st.spinner("⏳ جاري تدريب النموذج..."):
            model = train_and_save_model(X, y, model_path="fault_model.pkl")
        st.success("🎉 تم تدريب النموذج وحفظه في `fault_model.pkl` بنجاح.")

        st.subheader("📈 تقييم النموذج:")
        with st.spinner("⏳ جاري التقييم..."):
            y_pred, report_df, cm = evaluate_model(X, y, model)

            st.write("✅ **تقرير الأداء:**")
            st.dataframe(report_df.style.format("{:.2f}"))

            # زر تحميل التقرير كـ CSV
            csv_data = report_df.to_csv().encode('utf-8')
            st.download_button(
                label="⬇️ تحميل تقرير الأداء كـ CSV",
                data=csv_data,
                file_name="evaluation_report.csv",
                mime="text/csv"
            )

            st.write("✅ **مصفوفة الالتباس (Confusion Matrix):**")
            fig, ax = plt.subplots()
            sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
            ax.set_xlabel("التوقع")
            ax.set_ylabel("القيمة الحقيقية")
            st.pyplot(fig)