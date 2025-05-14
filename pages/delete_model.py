
import streamlit as st
import os

st.set_page_config(page_title="حذف النموذج المدرب", page_icon="🗑️", layout="centered")
st.title("🗑️ حذف النموذج المدرب")

if st.button("⚠️ حذف ملف trained_model.pkl"):
    if os.path.exists("trained_model.pkl"):
        os.remove("trained_model.pkl")
        st.success("✅ تم حذف النموذج بنجاح")
    else:
        st.warning("⚠️ لا يوجد ملف trained_model.pkl لحذفه")
