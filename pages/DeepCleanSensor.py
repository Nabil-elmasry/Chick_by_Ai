
import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="تنظيف ملف الحساسات", layout="wide")
st.title("تنظيف وتنظيم بيانات ملف الحساسات - Sensor Data Cleaning")

# رفع ملف الحساسات
uploaded_file = st.file_uploader("ارفع ملف الحساسات (Sensor.csv)", type=["csv"])

if uploaded_file:
    # قراءة البيانات
    df = pd.read_csv(uploaded_file)

    st.subheader("البيانات الأصلية")
    st.dataframe(df.head())

    # تنظيف الأعمدة: إزالة الفراغات والعلامات غير المرغوبة
    df.columns = [col.strip() for col in df.columns]

    # تنظيف القيم داخل الجدول
    def clean_value(val):
        if isinstance(val, str):
            val = val.replace(",", ".")  # استبدال الفاصلة العشرية
            val = re.sub(r'[^\d\.-]', '', val)  # إزالة أي حروف أو رموز باستثناء الأرقام والنقطة والسالب
        return val

    # تطبيق التنظيف
    df_cleaned = df.applymap(clean_value)

    st.subheader("البيانات بعد التنظيف")
    st.dataframe(df_cleaned.head())

    # حفظ الملف
    cleaned_filename = "Cleaned_Sensor.csv"
    df_cleaned.to_csv(cleaned_filename, index=False, encoding='utf-8')

    # زر تحميل الملف
    with open(cleaned_filename, "rb") as f:
        st.download_button(
            label="تحميل ملف الحساسات المنظف (CSV)",
            data=f,
            file_name="Cleaned_Sensor.csv",
            mime="text/csv"
        )
else:
    st.warning("من فضلك ارفع ملف الحساسات أولاً بصيغة CSV.")


---