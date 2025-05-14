import streamlit as st
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from pathlib import Path

st.set_page_config(page_title="تدريب النموذج - بيانات سليمة", page_icon="🧠", layout="wide")
st.title("🧠 تدريب النموذج على قراءات الحساسات السليمة")

uploaded_file = st.file_uploader("📤 ارفع ملف قراءات الحساسات السليمة (CSV)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ تم تحميل الملف بنجاح")
    st.dataframe(df.head())

    if st.button("🚀 ابدأ التدريب"):
        try:
            model = RandomForestClassifier()
            model.fit(df, [0]*len(df))  # كل السجلات سليمة (بدون أعطال)

            # حفظ النموذج داخل مجلد المشروع
            model_path = Path("trained_model.pkl")
            joblib.dump(model, model_path)

            # عرض رسالة توضح مكان الحفظ
            absolute_path = model_path.resolve()
            st.success("✅ تم حفظ النموذج بنجاح!")
            st.markdown(f"**📁 تم حفظ النموذج في المسار التالي:**\n`{absolute_path}`")

        except Exception as e:
            st.error(f"❌ حدث خطأ أثناء التدريب: {e}")