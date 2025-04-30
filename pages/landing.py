
# pages/landing.py

import streamlit as st
from graphviz import Digraph
import tempfile
import os

st.set_page_config(page_title="نظام تشخيص الأعطال", layout="wide")
st.title("مرحبًا بك في مشروع الذكاء الاصطناعي لتشخيص أعطال السيارات")
st.markdown("اختر من القائمة الجانبية للتنقل بين الصفحات.")

if st.button("عرض الهيكل التنظيمي للمشروع - نصي"):
    st.code("""
AI_diagnosis_project/
│
├── main.py
├── Carset.csv
│
├── pages/
│   ├── landing.py
│   ├── diagnosis.py
│   ├── train_model.py
│   ├── prediction.py
│   ├── load_codes.py
│   ├── model_info.py
│   ├── deviation_chart.py
│   └── about.py
│
├── modules/
│   ├── data_loader.py
│   ├── preprocessing.py
│   └── viz.py
│
├── assets/
│   ├── codes_dataset.csv
│   └── normal_stats.csv
│
└── backup/
    """, language="bash")

if st.button("عرض الهيكل التنظيمي للمشروع - بياني"):
    dot = Digraph(format="png")

    dot.node("Root", "AI_diagnosis_project")
    dot.edge("Root", "main.py")
    dot.edge("Root", "Carset.csv")

    dot.node("Pages", "pages/")
    dot.edge("Root", "Pages")
    for page in ["landing.py", "diagnosis.py", "train_model.py", "prediction.py", "load_codes.py", "model_info.py", "deviation_chart.py", "about.py"]:
        dot.edge("Pages", page)

    dot.node("Modules", "modules/")
    dot.edge("Root", "Modules")
    for mod in ["data_loader.py", "preprocessing.py", "viz.py"]:
        dot.edge("Modules", mod)

    dot.node("Assets", "assets/")
    dot.edge("Root", "Assets")
    for file in ["codes_dataset.csv", "normal_stats.csv"]:
        dot.edge("Assets", file)

    dot.edge("Root", "backup/")

    st.graphviz_chart(dot)

    # حفظ الصورة مؤقتاً
    with tempfile.TemporaryDirectory() as tmpdirname:
        filepath = os.path.join(tmpdirname, "project_structure.png")
        dot.render(filepath, cleanup=True)
        with open(filepath + ".png", "rb") as f:
            st.download_button(
                label="تحميل صورة الهيكل التنظيمي",
                data=f,
                file_name="AI_project_structure.png",
                mime="image/png"
            )

st.markdown("---")
st.markdown("**تم تنفيذ هذا المشروع باستخدام Python و Streamlit**")

