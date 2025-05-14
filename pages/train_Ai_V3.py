# training_anomaly_model.py

import streamlit as st
import pandas as pd
import base64
from sklearn.ensemble import IsolationForest
import joblib

st.set_page_config(page_title="تدريب نموذج الحساسات السليمة", layout="wide")
st.title("📊 تدريب النموذج على قراءات الحساسات السليمة")

# رفع ملف الحساسات
uploaded_file = st.file_uploader("ارفع ملف قراءات الحساسات السليمة (CSV فقط)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ تم رفع الملف بنجاح")
    st.dataframe(df.head())

    if st.button("🚀 ابدأ تدريب النموذج"):
        try:
            model = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)
            model.fit(df)

            joblib.dump(model, "sensor_model.pkl")  # حفظ النموذج
            st.success("✅ تم تدريب النموذج بنجاح وحفظه كـ sensor_model.pkl")
        except Exception as e:
            st.error(f"❌ حدث خطأ أثناء التدريب: {e}")