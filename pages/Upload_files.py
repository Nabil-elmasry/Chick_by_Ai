
import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="تنظيف وتحويل ملف الأكواد", layout="centered")
st.title("تحميل وتنظيف ملف الأكواد - TXT")

uploaded_file = st.file_uploader("ارفع ملف الأكواد (txt)", type="txt")

if uploaded_file is not None:
    content = uploaded_file.read().decode('utf-8')
    
    # استخراج البيانات باستخدام regex
    pattern = r'"(P\d{4})","([^"]+)"'
    matches = re.findall(pattern, content)

    if matches:
        df = pd.DataFrame(matches, columns=["Code", "Description"])
        st.success(f"تم استخراج {len(df)} كود بنجاح")
        st.dataframe(df)

        # حفظ الملف
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="تحميل ملف الأكواد المنظف",
            data=csv_data,
            file_name="Cleaned_Codes.csv",
            mime="text/csv"
        )
    else:
        st.error("لم يتم العثور على أكواد في الملف. تأكد من تنسيقه.")
else:
    st.info("يرجى رفع ملف .txt لبدء التنظيف.")
