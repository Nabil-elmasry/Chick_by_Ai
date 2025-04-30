
# pages/deviation_chart.py

import streamlit as st
import pandas as pd
import os
from modules.viz import plot_sensor_deviations

st.set_page_config(page_title="📊 انحرافات الحساسات", layout="wide")
st.title("📊 رسم يوضح انحراف قيم الحساسات عن الطبيعي")

uploaded_file = st.file_uploader("ارفع ملف بيانات حساس واحد بصيغة CSV", type="csv")

if uploaded_file:
    try:
        sensor_df = pd.read_csv(uploaded_file)
        stats_path = "assets/normal_stats.csv"

        if not os.path.exists(stats_path):
            st.error("⚠️ ملف normal_stats.csv غير موجود في مجلد assets.")
        else:
            stats_df = pd.read_csv(stats_path)

            st.subheader("الرسوم البيانية:")
            figs = plot_sensor_deviations(sensor_df, stats_df)
            for fig in figs:
                st.pyplot(fig)

    except Exception as e:
        st.error(f"حدث خطأ أثناء المعالجة: {e}")
