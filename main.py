#final project 

import streamlit as st

st.set_page_config(page_title="تشخيص الأعطال", layout="wide")

st.sidebar.title("قائمة التنقل")
st.sidebar.page_link("pages/landing.py", label="الصفحة الافتتاحية")
st.sidebar.page_link("pages/diagnosis.py", label="التشخيص وتحليل البيانات")

st.markdown("<h1 style='text-align: center;'>مرحبا بك في نظام Check by AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>يرجى اختيار صفحة من القائمة الجانبية</p>", unsafe_allow_html=True)

