
import streamlit as st

# إعداد الصفحة
st.set_page_config(page_title="الصفحة الرئيسية", layout="wide")

# عنوان الصفحة بتأثير متدرج وأيقونة
st.markdown("""
    <div style='background: linear-gradient(to right, #ff8c00, #ffa500); padding:20px; border-radius:12px; text-align:center; box-shadow: 2px 2px 12px #aaa;'>
        <h1 style='color:white; font-size:36px;'>
            &#9889; Welcome to the AI Project for Vehicle Fault Diagnosis
        </h1>
    </div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# نبذة مختصرة عن المشروع
with st.expander("Project Summary"):
    st.markdown("""
    <div style='background-color:#fff3cd; border-left:6px solid #ffc107; padding:20px; border-radius:10px; font-size:18px; line-height:1.8; color:#212529; box-shadow: 1px 1px 10px #eee;'>
        This project aims to assist vehicle technicians and users in diagnosing faults using Artificial Intelligence. <br><br>
        The system analyzes vehicle data such as fuel trims, sensor values, and error codes to identify potential issues and provide predictions. <br><br>
        It's built using Python and Machine Learning models and allows users to train the model, run predictions, view deviation analysis, and understand model behavior.
    </div>
    """, unsafe_allow_html=True)

# إرشادات التنقل
st.markdown("""
<div style='font-size:18px; background-color:#ffe6cc; padding:15px; border-radius:10px; box-shadow: 0px 0px 6px #ffad33;'>
<b>Use the sidebar to navigate between pages such as:</b>
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

# الهيكل التنظيمي داخل زرار
with st.expander("Show Project Structure"):
    st.markdown("""
    <div style='background-color:#f8f9fa; padding:20px; border:1px solid #ccc; border-radius:10px; font-family: monospace; box-shadow: 1px 1px 10px #ddd;'>
    <pre style='font-size:16px'>
AI_diagnosis_project/
│
├── main.py
├── Carset.csv
├── pages/
│   ├── landing.py
│   ├── diagnosis.py
│   ├── train_model.py
│   ├── prediction.py
│   ├── model_info.py
│   ├── deviation_chart.py
│   ├── about.py
│   └── support_log.py
│
├── modules/
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── viz.py
│   └── load_codes.py
│
└── assets/
    ├── codes_dataset.csv
    └── normal_stats.csv
    </pre>
    </div>
    """, unsafe_allow_html=True)
