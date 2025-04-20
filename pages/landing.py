#final project 

import streamlit as st

st.set_page_config(page_title="الصفحة الافتتاحية", layout="wide")

st.markdown(
    """
    <div style='text-align:center; padding:40px; background: linear-gradient(90deg, #e60000, #000); color:white; border-radius:15px;'>
        <h1>مرحباً بك في تطبيق Check by AI</h1>
        <h3>نظام ذكي لتحليل الأعطال والتنبؤ بها باستخدام بيانات الحساسات</h3>
        <br>
        <a href="/?page=diagnosis" style='padding:10px 30px; font-size:20px; background-color:#ff4444; color:white; text-decoration:none; border-radius:10px;'>ابدأ التشخيص</a>
        <br><br>
        <p style='font-size:14px; color:#ccc;'>Developed by Eng. Nabil Almasry - Powered by AI</p>
    </div>
    """,
    unsafe_allow_html=True
)
