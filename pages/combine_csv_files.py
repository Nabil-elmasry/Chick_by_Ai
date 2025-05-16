صفحة: دمج ملفات قراءات الحساسات على دفعات (مثلاً 30 ملف)

المسار: pages/merge_sensor_files.py

import streamlit as st import pandas as pd import base64 import os

st.set_page_config(page_title="دمج ملفات الحساسات", page_icon="🗂️", layout="wide") st.title("🗂️ دمج ملفات قراءات الحساسات - دفعة بدفعة")

ملف التخزين المؤقت لتجميع البيانات

TEMP_FILE_PATH = "data/combined_sensor_data.csv" os.makedirs("data", exist_ok=True)

رفع دفعة من الملفات (بحد أقصى 30)

uploaded_files = st.file_uploader("📤 ارفع دفعة من ملفات CSV (بحد أقصى 30)", type=["csv"], accept_multiple_files=True)

if uploaded_files: if len(uploaded_files) > 30: st.error("⚠️ الرجاء رفع 30 ملف كحد أقصى في كل دفعة") else: all_new_data = [] for file in uploaded_files: try: df = pd.read_csv(file) all_new_data.append(df) except Exception as e: st.warning(f"خطأ في الملف {file.name}: {e}")

if all_new_data:
        new_batch = pd.concat(all_new_data, ignore_index=True)
        st.success(f"✅ تم تحميل ودمج {len(uploaded_files)} ملف.")
        st.dataframe(new_batch.head())

        if os.path.exists(TEMP_FILE_PATH):
            existing_df = pd.read_csv(TEMP_FILE_PATH)
            combined_df = pd.concat([existing_df, new_batch], ignore_index=True)
        else:
            combined_df = new_batch

        combined_df.to_csv(TEMP_FILE_PATH, index=False)
        st.success("📁 تم تحديث الملف المجمع بالدفعة الجديدة")

عرض المحتوى الحالي للملف المدموج

if os.path.exists(TEMP_FILE_PATH): st.markdown("---") st.subheader("📦 محتوى الملف المدموج حتى الآن") temp_df = pd.read_csv(TEMP_FILE_PATH) st.write(f"✅ عدد السجلات الحالية: {temp_df.shape[0]}") st.dataframe(temp_df.head())

# زر لتنظيف البيانات وتنزيل الملف النهائي
if st.button("🧹 تنظيف البيانات النهائية"):
    cleaned_df = temp_df.dropna(how='all')
    cleaned_df.drop_duplicates(inplace=True)

    st.success("✅ تم تنظيف البيانات من الصفوف الفارغة والمكررة")
    st.write(f"✅ عدد السجلات بعد التنظيف: {cleaned_df.shape[0]}")

    # إنشاء رابط تحميل
    csv = cleaned_df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="clean_sensor_data.csv">⬇️ تحميل الملف النهائي للتدريب</a>'
    st.markdown("### 📥 حفظ الملف النهائي على الموبايل")
    st.markdown(href, unsafe_allow_html=True)

    # حفظه أيضًا داخليًا للمرحلة التالية (التدريب)
    cleaned_df.to_csv("data/clean_sensor_data.csv", index=False)

