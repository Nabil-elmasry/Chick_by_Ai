
import streamlit as st

# Page config
st.set_page_config(page_title="Home Page", layout="wide")

# Styling with CSS
st.markdown("""
<style>
.header {
  background: linear-gradient(90deg, #dc3545, #0d6efd);
  color: white;
  padding: 25px;
  border-radius: 12px;
  text-align: center;
  font-size: 30px;
  font-weight: bold;
  box-shadow: 2px 2px 12px #888;
  animation: fadeIn 2s ease-in;
}
.section {
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 12px;
  font-size: 17px;
  color: #333;
  box-shadow: 0px 0px 10px #bbb;
}
ul li {
  padding-bottom: 6px;
}
@keyframes fadeIn {
  from {opacity: 0;}
  to {opacity: 1;}
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("<div class='header'>Welcome to the AI Car Fault Diagnosis Project</div>", unsafe_allow_html=True)

# Instruction section in expander
with st.expander("Click to show project navigation guide"):
    st.markdown("""
    <div class='section'>
    Choose from the sidebar to navigate between pages:
    <ul>
    <li>Train the model</li>
    <li>Diagnose vehicle faults</li>
    <li>Deviation analysis</li>
    <li>Model information</li>
    <li>Project overview</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# Organizational structure in expander
with st.expander("Click to show project structure"):
    st.markdown("""
    <div class='section'>
    <pre>
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
│   └── about.py
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

