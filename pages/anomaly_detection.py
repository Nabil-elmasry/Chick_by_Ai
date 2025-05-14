import streamlit as st
import pandas as pd
import joblib
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="كشف الانحراف", page_icon="📉", layout="wide")
st.title("📉 تحليل انحراف قراءات الحساسات")

# تحميل النموذج المدرب
try:
    model = joblib.load("trained_model.pkl")
except FileNotFoundError:
    st.error("❌ لم يتم العثور على النموذج المدرب. الرجاء تدريب النموذج أولاً.")
    st.stop()

# رفع ملف السيارة التي تحتوي على قراءات مشكوك فيها
uploaded_file = st.file_uploader("📤 ارفع ملف قراءات السيارة المشكوك فيها", type=["csv"])

if uploaded_file:
    df_input = pd.read_csv(uploaded_file)
    st.success("✅ تم تحميل الملف")
    st.dataframe(df_input.head())

    # استخراج الخصائص المتوقعة من النموذج
    try:
        prediction = model.predict(df_input)
        prediction_proba = model.predict_proba(df_input)[:, 0]  # احتمال الانتماء للحالة السليمة

        # حساب درجة الانحراف كـ (1 - احتمال السليم)
        df_input["انحراف"] = 1 - prediction_proba

        st.subheader("🔍 نتائج كشف الانحراف")
        st.dataframe(df_input[["انحراف"]].head(10))

        # رسم بياني يوضح الانحراف
        st.subheader("📊 رسم بياني يوضح مستوى الانحراف")

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(df_input["انحراف"].values, marker='o', linestyle='-', color='red', label='درجة الانحراف')
        ax.axhline(y=0.5, color='gray', linestyle='--', label='الحد الفاصل')
        ax.set_title("مستوى انحراف قراءات السيارة", fontsize=14)
        ax.set_xlabel("السجلات", fontsize=12)
        ax.set_ylabel("درجة الانحراف", fontsize=12)
        ax.legend()
        ax.grid(True)

        st.pyplot(fig)

        # رابط تحميل النتائج مع عمود الانحراف
        def convert_df(df):
            return df.to_csv(index=False).encode('utf-8')

        st.download_button(
            label="📥 تحميل النتائج مع الانحراف",
            data=convert_df(df_input),
            file_name="deviation_results.csv",
            mime="text/csv",
        )

    except Exception as e:
        st.error(f"❌ حدث خطأ أثناء التنبؤ: {e}")