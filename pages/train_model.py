
# pages/train_model.py

import streamlit as st
from modules.data_loader import load_sensor_data, load_carset
from modules.preprocessing import prepare_training_data
from modules.model import train_and_save_model

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
            # هنا يتم حفظ النموذج في fault_model.pkl
            train_and_save_model(X, y, model_path="fault_model.pkl")
        st.success("🎉 تم تدريب النموذج وحفظه في `fault_model.pkl` بنجاح.")
