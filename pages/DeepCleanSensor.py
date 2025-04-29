
import streamlit as st
import pandas as pd
import re
from io import StringIO

st.title("تنظيف وتنظيم بيانات الحساسات")

uploaded_file = st.file_uploader("ارفع ملف sensor.csv", type=["csv"])
if uploaded_file is not None:
    # قراءة الملف الأصلي
    df = pd.read_csv(uploaded_file, encoding='utf-8')

    st.subheader("البيانات قبل التنظيف")
    st.write(df.head())

    # تنظيف الأعمدة: فصل القيم عن الوحدات والنسب
    new_columns = {}
    for col in df.columns:
        new_value_col = col.strip()
        unit_col = new_value_col + "_unit"

        def extract_value_and_unit(val):
            if pd.isna(val):
                return pd.NA, pd.NA
            match = re.match(r"([\d\-,\.E+]+)([^\d\s,\.%]+|%)?", str(val).strip())
            if match:
                value = match.group(1).replace(',', '.')
                unit = match.group(2) if match.group(2) else ""
                return value, unit
            return val, ""

        values, units = zip(*df[new_value_col].map(extract_value_and_unit))
        df[new_value_col] = values
        df[unit_col] = units
        new_columns[new_value_col] = new_value_col
        new_columns[unit_col] = unit_col

    # تحويل القيم الرقمية إلى float
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col])
        except:
            continue

    st.subheader("البيانات بعد التنظيف")
    st.write(df.head())

    # حفظ الملف للتنزيل
    cleaned_csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="تحميل الملف بعد التنظيف (CSV)",
        data=cleaned_csv,
        file_name="Cleaned_Sensor.csv",
        mime="text/csv"
    )
