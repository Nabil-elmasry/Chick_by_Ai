
# pages/load_codes.py

import streamlit as st
from modules.data_loader import load_sensor_data
from modules.preprocessing import calculate_normal_stats
import os

st.set_page_config(page_title="📥 تحميل الأكواد والإحصائيات", layout="wide")
st.title("📥 تحميل ملفات الأكواد وإحصائيات الحساسات")

codes_file = st.file_uploader("1. ارفع ملف الأكواد (codes_dataset.csv)", type="csv")
sensor_file = st.file_uploader("2. ارفع ملف الحساسات لحساب الإحصائيات", type="csv")

if st.button("💾 حفظ الملفات"):
    if codes_file is None or sensor_file is None:
        st.error("❌ تأكد من رفع الملفين.")
    else:
        # حفظ ملف الأكواد
        with open("assets/codes_dataset.csv", "wb") as f:
            f.write(codes_file.getbuffer())

        # حفظ إحصائيات الحساسات
        df = load_sensor_data(sensor_file)
        stats_df = calculate_normal_stats(df)
        stats_df.to_csv("assets/normal_stats.csv", index=False)

        st.success("✅ تم حفظ الملفات في مجلد assets بنجاح.")
