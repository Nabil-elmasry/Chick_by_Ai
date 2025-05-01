
import streamlit as st

#  إعداد الصفحة
st.set_page_config(page_title="الصفحة الرئيسية", layout="wide")

# عنوان الصفحة بتأثير لوني
st.markdown(
    "<h1 style='color:white; background-color:#FF8C00; padding:20px; border-radius:12px; text-align:center;'>"
    "Welcome to the AI Project for Vehicle Fault Diagnosis"
    "</h1>", unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

# نبذة مختصرة عن المشروع
with st.expander("Project Summary"):
    st.markdown("""
    <div style='background-color:#fff3cd; border-left:6px solid #ffc107; padding:20px; border-radius:10px; font-size:18px; line-height:1.8; color:#212529;'>
        This project aims to assist vehicle technicians and users in diagnosing faults using Artificial Intelligence. <br><br>
        The system analyzes vehicle data such as fuel trims, sensor values, and error codes to identify potential issues and provide predictions. <br><br>
        It's built using Python and Machine Learning models and allows users to train the model, run predictions, view deviation analysis, and understand model behavior.
    </div>
    """, unsafe_allow_html=True)

# إرشادات التنقل
st.markdown("""
<div style='font-size:18px; background-color:#e9ecef; padding:15px; border-radius:10px;'>
Use the sidebar to navigate between pages such as:
<ul>
<li>Model Training</li>
<li>Prediction</li>
<li>Deviation Analysis</li>
<li>Model Info</li>
<li>Support Log</li>
<li>About</li>
</ul>
</div>
""", unsafe_allow_html=True)
