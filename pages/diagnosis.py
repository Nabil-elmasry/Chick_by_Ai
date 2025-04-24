

#python
import streamlit as st
import pandas as pd
import re
import os

# دالة تنظيف البيانات (مُحسنة)
def clean_car_data(df):
    """تقوم بتنظيف بيانات السيارات واستخراج أكواد الأعطال"""
    cleaned_data = []
    for _, row in df.iterrows():
        try:
            # استخراج أكواد الأعطال (مثل P0420)
            fault_codes = re.findall(r'P\d{3,4}', str(row))
            
            cleaned_data.append({
                'Sensor': str(row.get('Sensor', row.get('حساس', ''))),
                'Value': str(row.get('Value', row.get('القيمة', ''))),
                'Standard': str(row.get('Standard', row.get('المعيار', ''))),
                'Fault_Codes': '، '.join(fault_codes) if fault_codes else 'لا يوجد عطل'
            })
        except Exception as e:
            continue
    return pd.DataFrame(cleaned_data)

# واجهة Streamlit الرئيسية
def main():
    st.set_page_config(
        page_title="نظام تشخيص الأعطال",
        page_icon="🚗",
        layout="wide"
    )
    
    st.markdown("""
    <div style="text-align:center; background:linear-gradient(to right, #ff4b4b, #3a7bd5); padding:20px; border-radius:15px;">
        <h1 style="color:white;">Check by AI - نظام الذكاء الاصطناعي</h1>
        <h3 style="color:#f0f0f0;">لتنظيف بيانات السيارات وتشخيص الأعطال</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # قسم رفع الملف
    uploaded_file = st.file_uploader(
        "📁 رفع ملف بيانات السيارات (CSV)",
        type="csv",
        help="الرجاء رفع ملف Carset.csv"
    )
    
    if uploaded_file:
        try:
            # قراءة الملف
            df = pd.read_csv(uploaded_file, encoding='utf-8')
            
            # تنظيف البيانات
            with st.spinner('جاري معالجة البيانات... ⏳'):
                cleaned_df = clean_car_data(df)
            
            # عرض النتائج
            st.success("✅ تم تنظيف البيانات بنجاح!")
            st.dataframe(cleaned_df, height=400, use_container_width=True)
            
            # تحميل الملف النظيف
            csv_data = cleaned_df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="💾 حفظ البيانات المنظفة",
                data=csv_data,
                file_name="Cleaned_CarData.csv",
                mime="text/csv",
                help="حفظ الملف على جهازك"
            )
            
        except Exception as e:
            st.error(f"❌ حدث خطأ: {str(e)}")
            st.warning("الرجاء التأكد من صيغة الملف المرفوع")
