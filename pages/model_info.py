
# pages/model_info.py

import streamlit as st
import joblib
import os

st.set_page_config(page_title="📈 معلومات النموذج", layout="wide")
st.title("📈 تفاصيل النموذج المدرب")

model_path = "fault_model.pkl"

if os.path.exists(model_path):
    model = joblib.load(model_path)

    st.markdown("### النوع: RandomForestClassifier")
    st.write(f"عدد الأشجار (n_estimators): {model.n_estimators}")
    st.write(f"عدد الخصائص المستخدمة: {len(model.feature_names_in_)}")
    st.write(f"دقة التدريب: {round(model.oob_score_ * 100, 2) if hasattr(model, 'oob_score_') else 'غير متاح'}%")
else:
    st.warning("⚠️ لم يتم العثور على النموذج. الرجاء تدريب النموذج أولاً.")

