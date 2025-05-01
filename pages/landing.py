
import streamlit as st
import time

# إعداد الصفحة
st.set_page_config(page_title="الصفحة الرئيسية", layout="wide")

# تأثير متحرك للترحيب
welcome_text = "مرحبًا بك في مشروع الذكاء الاصطناعي لتشخيص أعطال السيارات"
st.markdown(
    f"<h1 style='color:#ffffff;background-color:#0d6efd;padding:20px;border-radius:10px;text-align:center;'>{welcome_text}</h1>",
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True)

# إرشادات التنقل
st.markdown("""
<div style='font-size:18px; background-color:#f1f1f1; padding:20px; border-radius:10px;'>
اختر من القائمة الجانبية للتنقل بين الصفحات المختلفة:
<ul>
<li>صفحة تدريب النموذج</li>
<li>صفحة التوقع</li>
<li>تحليل الانحراف</li>
<li>معلومات عن النموذج</li>
<li>سجل الدعم الفني</li>
<li>حول المشروع</li>
</ul>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# عرض الهيكل التنظيمي النصي
st.subheader("الهيكل التنظيمي للمشروع")

with st.expander("عرض تفاصيل الهيكل"):
    st.markdown("""
    <div style='background-color:#f8f9fa; padding:20px; border:1px solid #ccc; border-radius:10px'>
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

