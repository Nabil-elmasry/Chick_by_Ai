import streamlit as st
import pandas as pd
import re
from io import StringIO

st.set_page_config(page_title="تنظيف carset_net", layout="wide")
st.title("تنظيف وتنظيم carset_net")

uploaded_file = st.file_uploader("ارفع ملف carset_net.csv", type=["csv"])
if uploaded_file is not None:
    # قراءة الملف
    df = pd.read_csv(uploaded_file, encoding='utf-8')

    st.subheader("البيانات قبل التنظيف")
    st.write(df.head())

    # تنظيف الأعمدة: فصل القيم والوحدات إن وجدت
    for col in df.columns:
        clean_col = col.strip()
        unit_col = clean_col + "_unit"

        def extract_value_and_unit(val):
            if pd.isna(val):
                return pd.NA, pd.NA
            match = re.match(r"([\d\-,\.E+]+)([^\d\s,\.%]+|%)?", str(val).strip())
            if match:
                value = match.group(1).replace(',', '.')
                unit = match.group(2) if match.group(2) else ""
                return value, unit
            return val, ""

        values, units = zip(*df[clean_col].map(extract_value_and_unit))
        df[clean_col] = values
        df[unit_col] = units

    # تحويل الأرقام
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col])
        except:
            pass

    st.subheader("البيانات بعد التنظيف")
    st.write(df.head())

    # تحميل الملف النهائي
    cleaned_csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="تحميل ملف carset_net بعد التنظيف",
        data=cleaned_csv,
        file_name="Cleaned_carset_net.csv",
        mime="text/csv"
    )