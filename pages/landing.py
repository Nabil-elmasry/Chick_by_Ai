
import streamlit as st

st.set_page_config(page_title="الصفحة الافتتاحية", layout="wide")

st.markdown(
    """
    <div style='text-align:center; padding:40px; background: linear-gradient(90deg, #e60000, #000); color:white; border-radius:15px;'>
        <h1 مرحبا   Check by AI</h1>
        <h3>نظام ذكي لتحليل الأعطال والتنبؤ بها باستخدام بيانات الحساسات</h3>
        <br>
        <p style='font-size:20px;'>يمكنك بدء التشخيص من القائمة الجانبية</p>
        <br><br>
        <p style='font-size:14px; color:#ccc;'>Developed by <strong>Eng. Nabil Almasry</strong> - Powered by AI</p>
    </div>
    """,
    unsafe_allow_html=True
)
