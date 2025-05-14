import streamlit as st
import pandas as pd
import joblib
import base64
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(page_title="تدريب النموذج - بيانات سليمة", page_icon="🧠", layout="wide")
st.title("🧠 تدريب النموذج على قراءات الحساسات السليمة")

uploaded_file = st.file_uploader("📤 ارفع ملف قراءات الحساسات السليمة (CSV)", type=["csv"])

def get_download_link(file_path, label="تحميل الملف"):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        file_name = file_path.split("/")[-1]
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="{file_name}">⬇️ {label}</a>'
        return href

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ تم تحميل الملف بنجاح")
    st.dataframe(df.head())

    if st.button("🚀 ابدأ التدريب"):
        try:
            # حذف الأعمدة غير الرقمية (زي التواريخ)
            numeric_df = df.select_dtypes(include=["number"])

            if numeric_df.empty:
                st.warning("⚠️ لا توجد أعمدة رقمية للتدريب.")
            else:
                model = RandomForestClassifier()
                model.fit(numeric_df, [0]*len(numeric_df))  # كل البيانات سليمة

                file_path = "trained_model.pkl"
                joblib.dump(model, file_path)

                st.success("✅ تم حفظ النموذج بنجاح")
                st.markdown("### 📥 تحميل النموذج المدرب:")
                st.markdown(get_download_link(file_path, "اضغط هنا لتحميل trained_model.pkl"), unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ حدث خطأ أثناء التدريب: {e}")