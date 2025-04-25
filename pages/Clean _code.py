
import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="تنظيف ملف الأكواد", layout="wide")
st.title("تنظيف وتجهيز ملف الأكواد - DTC Codes Cleaner")

uploaded_file = st.file_uploader("ارفع ملف الأكواد (TXT)", type="txt")

if uploaded_file:
    st.success("تم رفع الملف بنجاح. اضغط على زر 'تنظيف الملف' لبدء المعالجة.")

    if st.button("تنظيف الملف"):
        # قراءة النص من الملف
        raw_text = uploaded_file.read().decode('utf-8')

        # استخراج الأكواد والوصف باستخدام regex
        pattern = r'"?(P\d{4})"?[,،\s]*"?(.+?)"?(?=\n|$)'
        matches = re.findall(pattern, raw_text)

        if matches:
            df_codes = pd.DataFrame(matches, columns=["Code", "Description"])
            st.dataframe(df_codes)

            # حفظ الملف
            csv_filename = "Cleaned_Codes.csv"
            df_codes.to_csv(csv_filename, index=False, encoding='utf-8')

            # زر لتحميل الملف
            with open(csv_filename, "rb") as f:
                st.download_button(
                    label="تحميل الملف المنظف",
                    data=f,
                    file_name="Cleaned_Codes.csv",
                    mime="text/csv"
                )
        else:
            st.warning("لم يتم العثور على بيانات مناسبة داخل الملف.")
else:
    st.info("من فضلك ارفع ملف TXT يحتوي على الأكواد.")
