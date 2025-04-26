
import pandas as pd
import re

# رفع الملف عبر Streamlit
import streamlit as st

st.title("تنظيف ملف الحساسات وتجهيز البيانات")

uploaded_file = st.file_uploader("ارفع ملف الحساسات (sensor.csv)", type=['csv'])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.success("تم تحميل الملف بنجاح!")

    # قائمة الأعمدة المستهدفة بالتنظيف
    target_columns = df.columns

    # إنشاء نسخ إضافية لحفظ القيم والوحدات
    cleaned_data = pd.DataFrame()

    for col in target_columns:
        cleaned_values = []
        units = []

        for value in df[col].astype(str):
            # استخراج الرقم
            number = re.findall(r"[-+]?\d*\.\d+|\d+", value.replace(',', '.'))
            number = number[0] if number else None

            # استخراج الوحدة
            unit = re.sub(r"[-+]?\d*\.\d+|\d+|[,]|%", "", value).strip()

            cleaned_values.append(float(number) if number is not None else None)
            units.append(unit if unit else None)

        cleaned_data[col] = cleaned_values
        cleaned_data[col + "_unit"] = units

    # عرض أول 5 صفوف للمعاينة
    st.subheader("معاينة أولية للبيانات بعد التنظيف:")
    st.dataframe(cleaned_data.head())

    # حفظ الملف النهائي
    csv = cleaned_data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="تحميل الملف المنظف بصيغة CSV",
        data=csv,
        file_name="Cleaned_Sensor.csv",
        mime='text/csv'
    )

