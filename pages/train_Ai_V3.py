import streamlit as st
import pandas as pd
import base64
import joblib
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(page_title="تدريب النموذج - بيانات سليمة", page_icon="🧠", layout="wide")
st.title("🧠 تدريب النموذج على قراءات الحساسات السليمة")

uploaded_file = st.file_uploader("📤 ارفع ملف قراءات الحساسات السليمة (CSV)", type=["csv"])

# دالة لتحويل الملف إلى رابط تحميل
def get_download_link(file_path, label="تحميل الملف"):
    with open(file_path, "rb") as f:
        bytes_data = f.read()
        b64 = base64.b64encode(bytes_data).decode()
        href = f'<a href="data:file/pkl;base64,{b64}" download="{file_path}">⬇️ {label}</a>'
        return href

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ تم تحميل الملف بنجاح")
    st.dataframe(df.head())

    if st.button("🚀 ابدأ التدريب"):
        try:
            model = RandomForestClassifier()
            model.fit(df, [0]*len(df))  # تصنيف موحد للسجلات السليمة فقط

            # حفظ النموذج
            model_path = "trained_model.pkl"
            joblib.dump(model, model_path)
            st.success("✅ تم حفظ النموذج بنجاح")

            # عرض رابط التحميل اليدوي
            st.markdown("### 📥 تحميل النموذج المدرب يدويًا")
            st.markdown(get_download_link(model_path, "تحميل النموذج trained_model.pkl"), unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ حدث خطأ أثناء التدريب: {e}")