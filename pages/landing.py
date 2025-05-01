
import streamlit as st

st.set_page_config(page_title="الصفحة الرئيسية", layout="wide")

# CSS للتأثير والألوان
st.markdown("""
<style>
@keyframes fadeIn {
  from {opacity: 0;}
  to {opacity: 1;}
}
.fade-in {
  animation: fadeIn 2s ease-in;
}

.header {
  color: white;
  background-color: #0078D4;
  padding: 25px;
  border-radius: 12px;
  text-align: center;
  font-size: 32px;
  font-weight: bold;
  box-shadow: 2px 2px 10px #ccc;
}

.section {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 10px;
  margin-top: 20px;
  font-size: 18px;
  color: #333;
  box-shadow: 0px 0px 8px #ddd;
}
</style>
""", unsafe_allow_html=True)

# عنوان متحرك
st.markdown(f"<div class='header fade-in'>مرحبًا بك في مشروع الذكاء الاصطناعي لتشخيص أعطال السيارات</div>", unsafe_allow_html=True)

# تعليمات الاستخدام
st.markdown("""
<div class='section'>
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

# الهيكل التنظيمي
st.markdown("<div class='section'><h4>الهيكل التنظيمي للمشروع:</h4>", unsafe_allow_html=True)

with st.expander("عرض تفاصيل الهيكل"):
    st.markdown("""
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
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

