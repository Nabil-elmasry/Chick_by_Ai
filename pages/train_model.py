import streamlit as st
from modules.data_loader import load_sensor_data, load_carset
from modules.preprocessing import prepare_training_data
from modules.model import train_and_save_model, evaluate_model
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix

st.set_page_config(page_title="📊 تدريب النموذج", layout="wide")

st.title("📊 تدريب نموذج تنبؤ الأعطال")
st.write(
    """
    في هذه الصفحة يمكنك رفع ملف قراءات الحساسات وملف Carset، ثم:
    - إضافة عمود ID تلقائيًا لكل ملف.
    - تدريب نموذج Random Forest.
    - عرض تقييم النموذج.
    """
)

# رفع الملفات
sensor_file = st.file_uploader(
    "1. ارفع ملف الحساسات (sensor dataset)", type=["csv"], key="sensor_file"
)
carset_file = st.file_uploader(
    "2. ارفع ملف Carset (carset.csv)", type=["csv"], key="carset_file"
)

# متغيرات لتخزين الملفات بعد تعديلها
sensor_df = None
carset_df = None

# زر إضافة عمود ID
if st.button("➕ إضافة عمود ID تلقائيًا"):
    if sensor_file is None or carset_file is None:
        st.error("❌ الرجاء رفع كلا الملفين أولاً.")
    else:
        try:
            sensor_df = load_sensor_data(sensor_file)
            carset_df = load_carset(carset_file)

            # إضافة عمود ID بترقيم متسلسل
            sensor_df['id'] = range(1, len(sensor_df) + 1)
            carset_df['id'] = range(1, len(carset_df) + 1)

            st.success("✅ تم إضافة عمود ID بنجاح إلى كلا الملفين.")
        except Exception as e:
            st.error(f"حدث خطأ أثناء الإضافة: {e}")

# زر بدء التدريب
if st.button("🚀 ابدأ التدريب"):
    if sensor_df is None or carset_df is None:
        st.error("❌ تأكد من الضغط على زر 'إضافة عمود ID' أولاً.")
    else:
        with st.spinner("⏳ جاري إعداد البيانات..."):
            X, y = prepare_training_data(sensor_df, carset_df)
        st.success(f"✅ تم تجهيز البيانات ({X.shape[0]} عينة، {X.shape[1]} ميزة).")

        with st.spinner("⏳ جاري تدريب النموذج..."):
            model = train_and_save_model(X, y)
        st.success("✅ تم تدريب النموذج وحفظه بنجاح.")

        with st.spinner("⏳ جاري تقييم النموذج..."):
            y_pred = model.predict(X)
            report = classification_report(y, y_pred, output_dict=True)
            cm = confusion_matrix(y, y_pred)

        st.subheader("📈 تقييم النموذج")

        # عرض تقرير التقييم
        st.write("**تقرير التصنيف:**")
        st.dataframe(pd.DataFrame(report).transpose())

        # رسم مصفوفة الالتباس
        st.write("**مصفوفة الالتباس:**")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
        st.pyplot(fig)