
import streamlit as st
import os

LOG_FILE = "logs/errors.log"  # تأكد أن المسار صحيح داخل المشروع

st.set_page_config(page_title="Support Log", layout="wide")

st.title("Support / Error Log")
st.caption("هذه الصفحة تعرض سجل الأخطاء أو الرسائل الداعمة التي تم تسجيلها أثناء استخدام النظام.")

# التأكد من وجود ملف السجل
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        log_contents = f.read()
else:
    log_contents = "لا يوجد سجل أخطاء حالياً."

# عرض السجل
st.text_area("تفاصيل السجل", log_contents, height=300)

# زر لمسح السجل
if st.button("مسح السجل"):
    try:
        open(LOG_FILE, "w").close()
        st.success("تم مسح السجل بنجاح.")
    except Exception as e:
        st.error(f"حدث خطأ أثناء المسح: {e}")
else:
    st.info("يمكنك الضغط على زر 'مسح السجل' لإفراغ محتويات الملف.")

# ملاحظة إضافية
st.markdown("---")
st.info("هذا السجل يتم إنشاؤه تلقائيًا من أجزاء مختلفة داخل المشروع عند حدوث خطأ أو إضافة ملاحظات دعم.")

