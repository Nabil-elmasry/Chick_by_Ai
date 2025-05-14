import streamlit as st
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
import base64

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
            model.fit(df, [0]*len(df))  # كل السجلات سليمة

            # حفظ النموذج كملف
            model_filename = "trained_model.pkl"
            joblib.dump(model, model_filename)

            # تحويل الملف إلى base64
            with open(model_filename, "rb") as f:
                data = f.read()
                b64 = base64.b64encode(data).decode()
                href = f'<a href="data:file/pkl;base64,{b64}" download="{model_filename}">⬇️ اضغط هنا لتحميل النموذج المدرب</a>'
                st.markdown("### 📥 تحميل النموذج المدرب")
                st.markdown(href, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ حدث خطأ أثناء التدريب: {e}")