
# pages/predict_fault.py

import streamlit as st
import pandas as pd
from modules.data_loader import load_sensor_data, load_codes_data
from modules.model import predict_fault
from modules.viz import plot_deviations

st.set_page_config(page_title="🔍 التنبؤ بالأعطال", layout="wide")

st.title("🔍 تنبؤ الأعطال من قراءات الحساسات")
st.write(
    """
    ارفع ملف قراءات الحساسات الفعلية لتوقع كود العطل المحتمل مع شرحه، 
    بالإضافة إلى رسم بياني يوضح انحراف كل حساس عن القيم الطبيعية.
    """
)

# رفع ملف CSV جديد
new_file = st.file_uploader(
    "1. ارفع ملف قراءات الحساسات الفعلية", type=["csv"], key="new_readings"
)

# تأكد من وجود ملفات assets
codes_path = "assets/codes_dataset.csv"
stats_path = "assets/normal_stats.csv"
model_path = "fault_model.pkl"

if st.button("🔮 تنبؤ العطل"):
    if new_file is None:
        st.error("❌ الرجاء رفع ملف قراءات الحساسات الفعلية أولاً.")
    else:
        with st.spinner("⏳ جاري تحميل نموذج التنبؤ والبيانات..."):
            codes_df = load_codes_data(codes_path)
        st.success("✅ تم تحميل ملف الأكواد.")

        with st.spinner("⏳ تشغيل التنبؤ..."):
            # predict_fault يعيد (code, description, df_new, deviations)
            pred_code, description, df_new, deviations = predict_fault(
                new_data_path=new_file,
                model_path=model_path,
                codes_df=codes_df,
                normal_stats_path=stats_path,
                return_intermediate=True
            )
        st.success(f"✅ تم التنبؤ: **{pred_code}**")

        # عرض النتيجة
        st.markdown(f"### الكود المتوقع: `{pred_code}`")
        st.markdown(f"**الوصف:** {description}")

        # عرض الرسم البياني للانحرافات
        st.write("### رسم بياني لانحرافات الحساسات عن القيم الطبيعية")
        st.pyplot(plot_deviations(deviations))

