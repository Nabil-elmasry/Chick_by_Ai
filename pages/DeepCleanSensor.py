
import pandas as pd
import re

# رفع الملف عن طريق streamlit مثلا:
import streamlit as st

st.title("تنظيف ملف الحساسات مع استخراج الوحدات")

uploaded_file = st.file_uploader("ارفع ملف الحساسات بصيغة CSV", type=["csv"])

if uploaded_file is not None:
    # قراءة الملف
    df = pd.read_csv(uploaded_file)

    # دالة لفصل القيم الرقمية عن الوحدة
    def split_value_unit(value):
        if pd.isna(value):
            return value, None
        match = re.match(r"([-+]?[0-9]*\.?[0-9]+)\s*([a-zA-Z%/]+)?", str(value))
        if match:
            number = match.group(1)
            unit = match.group(2)
            return number, unit
        else:
            return value, None

    # تطبيق الدالة على كل الأعمدة
    cleaned_df = pd.DataFrame()
    for col in df.columns:
        cleaned_df[col] = df[col].apply(lambda x: split_value_unit(x)[0])
        cleaned_df[col + "_unit"] = df[col].apply(lambda x: split_value_unit(x)[1])

    # عرض البيانات بعد التنظيف
    st.dataframe(cleaned_df)

    # حفظ الملف الجديد
    csv = cleaned_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="تحميل الملف بعد التنظيف بصيغة CSV",
        data=csv,
        file_name="cleaned_sensor_file.csv",
        mime='text/csv',
    )

