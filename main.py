#update not approved 
import streamlit as st

st.set_page_config(page_title="تشخيص الأعطال", layout="wide")

# ======= تصميم العنوان والواجهة =======
st.markdown("""
    <div style="text-align:center; padding: 30px; background: linear-gradient(to right, #f8cdda, #1fc8db); border-radius: 15px;">
        <h1 style="color:#4B0082;">نظام Check by AI لتشخيص أعطال السيارات</h1>
        <h3 style="color:#2f2f2f;">اختر الصفحة التي تريد الانتقال إليها من القائمة الجانبية</h3>
    </div>
""", unsafe_allow_html=True)

# ======= توقيع أسفل الصفحة =======
st.markdown("""
    <br><hr style="border-top: 1px solid #bbb;">
    <div style="text-align:center; font-size:18px; color:#FF1493;">
        تنفيذ: Eng. Nabil Almasry &nbsp; | &nbsp; Powered by AI
    </div>
""", unsafe_allow_html=True)

# ======= القائمة الجانبية =======
st.sidebar.title("قائمة التنقل")
st.sidebar.page_link("pages/landing.py", label="الصفحة الافتتاحية", icon="🏁")
st.sidebar.page_link("pages/diagnosis.py", label="التشخيص وتحليل البيانات", icon="🧠")
