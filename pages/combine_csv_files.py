import streamlit as st
import pandas as pd
import base64

st.set_page_config(page_title="دمج ملفات قراءات الحساسات", page_icon="🗂️", layout="wide")
st.title("🗂️ دمج وتنظيف ملفات قراءات الحساسات (CSV)")

uploaded_files = st.file_uploader("📤 ارفع ملفات CSV الخاصة بالحساسات (يمكنك رفع عدة ملفات)", type=["csv"], accept_multiple_files=True)

if uploaded_files:
    dfs = []
    for file in uploaded_files:
        try:
            df = pd.read_csv(file)
            dfs.append(df)
        except Exception as e:
            st.warning(f"⚠️ حدث خطأ أثناء قراءة الملف {file.name}: {e}")

    if dfs:
        st.success(f"✅ تم تحميل {len(dfs)} ملف بنجاح")
        combined_df = pd.concat(dfs, ignore_index=True)

        st.markdown("### 🧹 تنظيف البيانات")
        st.write(f"عدد الصفوف قبل التنظيف: {combined_df.shape[0]}")

        # إزالة الصفوف التي كلها NaN
        combined_df.dropna(how='all', inplace=True)

        # إزالة التكرار
        combined_df.drop_duplicates(inplace=True)

        st.write(f"عدد الصفوف بعد التنظيف: {combined_df.shape[0]}")
        st.dataframe(combined_df.head(10))

        # زر تحميل الملف النهائي
        csv = combined_df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="clean_sensor_data.csv">⬇️ تحميل الملف النهائي بعد الدمج</a>'
        st.markdown("### 📥 تحميل الملف النهائي")
        st.markdown(href, unsafe_allow_html=True)