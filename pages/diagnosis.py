
   ```python
   import streamlit as st
   st.title("🚗 نظام تشخيص الأعطال")
   st.success("تم التشغيل بنجاح! يمكنك الآن رفع ملف CSV")
   uploaded_file = st.file_uploader("اختر ملف Carset.csv")
   if uploaded_file:
       st.write("الملف جاهز للتحليل!")
   ```
