
import streamlit as st
import pandas as pd
import joblib
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="كشف انحراف قراءات الحساسات", page_icon="📉", layout="wide")
st.title("📉 تحليل انحراف قراءات الحساسات")

uploaded_anomaly_file = st.file_uploader("📤 ارفع ملف قراءات السيارة بها مشكلة (CSV)", type=["csv"])

if uploaded_anomaly_file:
    try:
        model = joblib.load("trained_model.pkl")
        new_data = pd.read_csv(uploaded_anomaly_file)

        normal_data = model.estimators_[0].estimators_[0].tree_.value.shape[1]  # عدد الخصائص المستخدمة في التدريب

        if new_data.shape[1] != model.n_features_in_:
            st.error("❌ عدد أعمدة الملف لا يطابق النموذج المدرّب")
        else:
            # نحسب الفرق بين كل صف في البيانات وبين المتوسط العام للتدريب
            baseline_mean = model.estimators_[0].estimators_[0].tree_.threshold[:model.n_features_in_]
            diffs = np.abs(new_data - baseline_mean)
            deviation_score = diffs.mean(axis=1)

            st.subheader("📊 رسم بياني لدرجة الانحراف")
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.lineplot(data=deviation_score, ax=ax, color="crimson")
            ax.set_title("مستوى انحراف قراءات الحساسات", fontsize=16)
            ax.set_xlabel("رقم السجل")
            ax.set_ylabel("درجة الانحراف")
            st.pyplot(fig)

            st.dataframe(pd.DataFrame({"درجة الانحراف": deviation_score}))
    except Exception as e:
        st.error(f"❌ فشل في تحليل الانحراف: {e}")

