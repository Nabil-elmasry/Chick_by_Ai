
import streamlit as st

# إعداد الصفحة
st.set_page_config(page_title="الصفحة الرئيسية", layout="wide")

# CSS للتصميم
st.markdown("""
<style>
.header {
  background-color: #0d6efd;
  color: white;
  padding: 25px;
  border-radius: 10px;
  text-align: center;
  font-size: 32px;
  font-weight: bold;
  box-shadow: 2px 2px 10px #888;
}
.section {
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 10px;
  margin-top: 20px;
  font-size: 18px;
  color: #333;
  box-shadow: 0px 0px 6px #ccc;
}
</style>
""", unsafe_allow_html=True)

# عنوان رئيسي متحرك بسيط
st.markdown("<div class='header'>مرحبًا بك في مشروع الذكاء الاصطناعي لتشخيص أعطال السيارات</div>", unsafe_allow_html=True)

# إرشادات بسيطة
st.markdown("""
<div class='section'>
اختر من القائمة الجانبية للتنقل بين الصفحات المختلفة:
<ul>
<li>تدريب النموذج</li>
<li>تشخيص الأعطال</li>
<li>تحليل الانحراف</li>
<li>معلومات النموذج</li>
<li>حول المشروع</li>
</ul>
</div>
""", unsafe_allow_html=True)

# الهيكل التنظيمي النصي فقط (اختياري)
st.markdown("""
<div class='section'>
<b>الهيكل التنظيمي للمشروع (نصي):</b>
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

