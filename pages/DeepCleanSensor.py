
import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="تنظيف ملف الحساسات", layout="wide")

st.title("تنظيف وتحضير ملف بيانات الحساسات للتدريب")

uploaded_file = st.file_uploader("ارفع ملف الحساسات (Sensor.csv)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("البيانات الأصلية")
    st.dataframe(df.head())

    # ====== تنظيف البيانات ======

    # حذف أي صفوف ناقصة بشكل كامل
    df_clean = df.dropna(how='all')

    # حذف مسافات إضافية في الأعمدة
    df_clean.columns = df_clean.columns.str.strip()

    # تنظيف الخانات: إزالة الرموز مثل % و C و km/h و RPM و kPa و g/s
    def clean_value(val):
        if pd.isnull(val):
            return val
        val = str(val)
        val = re.sub(r'[^\d\.\-]', '', val)  # الاحتفاظ بالأرقام والعلامة السالبة والنقطة فقط
        return val

    for col in df_clean.columns:
        df_clean[col] = df_clean[col].apply(clean_value)

    # تحويل الأعمدة الرقمية فعلاً لأرقام (floats)
    for col in df_clean.columns:
        try:
            df_clean[col] = pd.to_numeric(df_clean[col])
        except:
            pass  # نسيب الأعمدة اللي مش قابلة للتحويل زي ID وغيره

    st.subheader("البيانات بعد التنظيف")
    st.dataframe(df_clean.head())

    # ====== زر لتحميل الملف النهائي ======
    csv = df_clean.to_csv(index=False).encode('utf-8-sig')

    st.download_button(
        label="تحميل ملف الحساسات بعد التنظيف",
        data=csv,
        file_name='Cleaned_Sensor.csv',
        mime='text/csv'
    )
else:
    st.warning("من فضلك ارفع ملف الحساسات أولاً.")

