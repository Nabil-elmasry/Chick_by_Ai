
import streamlit as st
from PIL import Image

st.set_page_config(page_title="الصفحة الرئيسية", layout="wide")

# تنسيق العنوان الرئيسي
st.markdown("""
    <div style='background-color:#0D6EFD;padding:15px;border-radius:10px'>
        <h1 style='color:white;text-align:center;'>مرحبًا بك في مشروع الذكاء الاصطناعي لتشخيص أعطال السيارات</h1>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# عرض التعليمات
st.markdown("""
### من فضلك اختر من القائمة الجانبية للتنقل بين الصفحات المختلفة:
- صفحة تدريب النموذج
- صفحة التوقع
- تحليل الانحراف
- معلومات عن النموذج
- سجل الدعم الفني (Support Log)
- حول المشروع
""", unsafe_allow_html=True)

st.markdown("---")

# عرض الشكل التنظيمي نصيًا
st.subheader("الهيكل التنظيمي للمشروع")

st.markdown("""
<div style='background-color:#F8F9FA; padding:20px; border:1px solid #dee2e6; border-radius:10px; font-family:Arial'>
<ul>
<li><strong>AI_diagnosis_project</strong></li>
<ul>
  <li>main.py</li>
  <li>Carset.csv</li>
  <li><strong>pages/</strong>
    <ul>
      <li>landing.py</li>
      <li>diagnosis.py</li>
      <li>train_model.py</li>
      <li>prediction.py</li>
      <li>model_info.py</li>
      <li>deviation_chart.py</li>
      <li>about.py</li>
      <li>support_log.py</li>
    </ul>
  </li>
  <li><strong>modules/</strong>
    <ul>
      <li>data_loader.py</li>
      <li>preprocessing.py</li>
      <li>viz.py</li>
      <li>load_codes.py</li>
    </ul>
  </li>
  <li><strong>assets/</strong>
    <ul>
      <li>codes_dataset.csv</li>
      <li>normal_stats.csv</li>
    </ul>
  </li>
</ul>
</ul>
</div>
""", unsafe_allow_html=True)

# صورة زخرفية أو شعار إن أردت
# image = Image.open("pages/assets/logo.png")
# st.image(image, width=150)
