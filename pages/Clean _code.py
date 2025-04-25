
import streamlit as st
import pandas as pd
import re

st.title("تنظيف وتنظيم ملف الأكواد")

uploaded_file = st.file_uploader("ارفع ملف الأكواد (TXT)", type=["txt"])

if uploaded_file is not None:
    raw_text = uploaded_file.read().decode("utf-8")

    # استخراج الأكواد والوصف
    pattern = r'"?(P\d{4})"?,"?([^"]+)"?'
    matches = re.findall(pattern, raw_text)

    if matches:
        df = pd.DataFrame(matches, columns=["Code", "Description"])
        st.success("تم استخراج الأكواد وتنظيفها بنجاح!")
        st.dataframe(df)

        # حفظ الملف بصيغة CSV مباشرة
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="تحميل الملف بصيغة CSV",
            data=csv,
            file_name="Cleaned_Codes.csv",
            mime="text/csv"
        )
    else:
        st.error("تعذر استخراج البيانات. تأكد من أن تنسيق الملف صحيح.")
