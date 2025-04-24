
```python
# diagnosis.py (النسخة المعدلة)
import streamlit as st
import pdfplumber
import pandas as pd
import re
import os
import shutil
import datetime

# ===== دوال جديدة مضافة =====
def clean_carset(data):
    """دالة تنظيف البيانات الجديدة"""
    cleaned_data = []
    for _, row in data.iterrows():
        fault_codes = re.findall(r'P\d{4}', str(row))
        cleaned_data.append({
            'Sensor': row.get('Sensor', ''),
            'Value': row.get('Value', ''),
            'Standard': row.get('Standard', ''),
            'Fault_Codes': ', '.join(fault_codes) if fault_codes else 'No Code'
        })
    return pd.DataFrame(cleaned_data)

# ===== واجهة Streamlit الأصلية (بدون تغيير) =====
st.set_page_config(page_title="تحليل الحساسات والأكواد", layout="wide")

# ... (كل الكود الأصلي يبقى كما هو حتى نهاية زر الحفظ الأصلي)

# ===== إضافة زر التنظيف الجديد =====
if 'df_matches' in locals() and not df_matches.empty:
    # زر التنظيف الجديد
    st.subheader("5. تنظيف البيانات وتصديرها")
    if st.button("تنظيف البيانات وحفظها"):
        try:
            # استخدم البيانات الموجودة في الذاكرة
            cleaned_df = clean_carset(df_matches)
            
            # حفظ الملف المنظف
            cleaned_df.to_csv("Cleaned_Carset.csv", index=False)
            st.success("تم تنظيف البيانات وحفظها في Cleaned_Carset.csv")
            
            # زر التحميل
            with open("Cleaned_Carset.csv", "rb") as f:
                st.download_button(
                    label="تحميل البيانات المنظفة",
                    data=f,
                    file_name="Cleaned_Carset.csv",
                    mime="text/csv"
                )
        except Exception as e:
            st.error(f"خطأ في التنظيف: {str(e)}")

# ... (بقية الكود الأصلي)
else:
    st.warning("يرجى رفع تقرير الحساسات وتقرير الأعطال للاستمرار.")
```