import streamlit as st
import pandas as pd
import base64
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# إعداد الصفحة
st.set_page_config(page_title="تدريب النموذج - البيانات النظيفة", layout="wide")
st.title("✨ 🛠️ تدريب النموذج على البيانات النظيفة")

# دالة لتحويل التقرير لرابط تحميل
def download_text_file(content, filename):
    b64 = base64.b64encode(content.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">⬇️ اضغط هنا لتحميل تقرير التقييم</a>'
    return href

# 1️⃣ رفع ملف البيانات الجاهز للتدريب
st.subheader("1️⃣ ارفع ملف الحساسات الجاهز للتدريب (CSV)")
clean_data_file = st.file_uploader("اختر ملف البيانات", type="csv")

if clean_data_file:
    df = pd.read_csv(clean_data_file)
    st.success("✅ تم رفع الملف بنجاح")
    st.write("معاينة البيانات:")
    st.dataframe(df.head())

    # تأكد من وجود العمود المستهدف
    target_column = st.selectbox("📌 اختر العمود المستهدف (Target)", df.columns)

    st.subheader("2️⃣ ابدأ تدريب النموذج")
    if st.button("🚀 ابدأ التدريب الآن"):
        try:
            X = df.drop(columns=[target_column])
            y = df[target_column]

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            model = RandomForestClassifier()
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

            report = classification_report(y_test, y_pred)
            st.success("✅ تم التدريب بنجاح")
            st.code(report)

            st.markdown("### 📥 تحميل تقرير التقييم")
            st.markdown(download_text_file(report, "model_evaluation.txt"), unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ حدث خطأ أثناء التدريب: {e}")