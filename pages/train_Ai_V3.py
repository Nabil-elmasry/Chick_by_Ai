import streamlit as st
import pandas as pd
import base64
import joblib
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(page_title="تدريب النموذج - بيانات سليمة", page_icon="🧠", layout="wide")
st.title("🧠 تدريب النموذج على قراءات الحساسات السليمة")

uploaded_file = st.file_uploader("📤 ارفع ملف قراءات الحساسات السليمة (CSV)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ تم تحميل الملف بنجاح")
    st.dataframe(df.head())

    if st.button("🚀 ابدأ التدريب"):
        try:
            # حذف الأعمدة غير الرقمية (مثل التاريخ أو النصوص)
            df_numeric = df.select_dtypes(include=['number'])

            if df_numeric.empty:
                st.error("❌ لا توجد أعمدة رقمية صالحة للتدريب بعد التنظيف")
            else:
                model = RandomForestClassifier()
                model.fit(df_numeric, [0]*len(df_numeric))  # تصنيف موحد للسجلات السليمة فقط

                joblib.dump(model, "trained_model.pkl")
                st.success("✅ تم حفظ النموذج بنجاح كملف trained_model.pkl")

        except Exception as e:
            st.error(f"❌ حدث خطأ أثناء التدريب: {e}")