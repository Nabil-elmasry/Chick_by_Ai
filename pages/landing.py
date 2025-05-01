import streamlit as st
import os
from PIL import Image
import base64

# إعدادات الصفحة
st.set_page_config(
    page_title="AI Diagnosis for Cars",
    page_icon="\U0001F697",
    layout="wide",
    initial_sidebar_state="expanded",
)

# تنسيق CSS لتجميل الصفحة
st.markdown("""
    <style>
    .title {
        font-size:50px;
        font-weight:bold;
        color:#4CAF50;
        text-align: center;
        margin-top: 30px;
    }
    .subtitle {
        font-size:22px;
        color:#555;
        text-align: center;
    }
    .button {
        display: flex;
        justify-content: center;
        margin: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# العنوان الرئيسي
st.markdown('<div class="title">مرحبًا بك في مشروع الذكاء الاصطناعي لتشخيص أعطال السيارات</div>', unsafe_allow_html=True)

# الوصف التعريفي
st.markdown('<div class="subtitle">اختر من القائمة الجانبية للتنقل بين الصفحات.</div>', unsafe_allow_html=True)

# زر عرض الهيكل التنظيمي
with st.container():
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("عرض الهيكل التنظيمي - نصي"):
            with st.expander("الهيكل التنظيمي النصي للمشروع"):
                st.code("""
AI_diagnosis_project/
├── main.py
├── Carset.csv
├── codes_dataset.csv
├── normal_stats.csv
├── Pages/
│   ├── landing.py
│   ├── train_model.py
│   ├── prediction.py
│   ├── model_info.py
│   ├── deviation_chart.py
│   ├── about.py
│   ├── support_log.py
├── modules/
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── viz.py
│   ├── load_codes.py
├── assets/
│   └── backup/
                """)

    with col2:
        if st.button("عرض الهيكل التنظيمي - بياني"):
            from streamlit.components.v1 import html
            html("""
            <iframe width="100%" height="500" src="https://dreampuf.github.io/GraphvizOnline/#digraph%20G%20%7B%0A%20%20main%20-%3E%20train_model%0A%20%20main%20-%3E%20prediction%0A%20train_model%20-%3E%20model_info%0A%20train_model%20-%3E%20preprocessing%0A%20train_model%20-%3E%20data_loader%0A%20prediction%20-%3E%20deviation_chart%0A%20prediction%20-%3E%20viz%0A%20prediction%20-%3E%20load_codes%0A%20main%20-%3E%20about%0A%20main%20-%3E%20support_log%0A%7D" frameborder="0"></iframe>
            """, height=520)

# معلومات إضافية أو شعارات مستقبلًا
st.markdown("---")
st.markdown("تم تطوير هذا المشروع باستخدام Python وStreamlit لتوفير تشخيص ذكي وفوري لأعطال السيارات بناءً على بيانات الحساسات.")


