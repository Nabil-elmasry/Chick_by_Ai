import streamlit as st import pandas as pd from sklearn.model_selection import train_test_split from sklearn.ensemble import RandomForestClassifier from sklearn.metrics import classification_report, accuracy_score import joblib import os

st.set_page_config(page_title="تدريب النموذج", layout="wide") st.title("🚗 تدريب نموذج الذكاء الاصطناعي للتنبؤ بالأعطال")

تحميل البيانات المدمجة

data_path = "data/merged_data.csv" if not os.path.exists(data_path): st.warning("الرجاء رفع ملف البيانات المدموجة أولاً.") uploaded = st.file_uploader("📄 ارفع ملف البيانات المدموجة (CSV)", type=["csv"]) if uploaded is not None: with open(data_path, "wb") as f: f.write(uploaded.read()) st.success("✅ تم حفظ الملف بنجاح!")

بدء التدريب

if os.path.exists(data_path): df = pd.read_csv(data_path)

if "fault_code" not in df.columns:
    st.error("❌ العمود 'fault_code' غير موجود في البيانات. تأكد من الدمج الصحيح")
else:
    if st.button("🚀 ابدأ التدريب"):
        try:
            y = df["fault_code"]
            X = df.drop(columns=["fault_code", "record_id"], errors='ignore')

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            
            y_pred = model.predict(X_test)
            acc = accuracy_score(y_test, y_pred)
            report = classification_report(y_test, y_pred, output_dict=False)

            st.success("✅ تم تدريب النموذج بنجاح")
            st.markdown(f"### الدقة العامة: `{acc:.2f}`")
            st.text("تقرير التصنيف:")
            st.text(report)

            if st.button("💾 احفظ النموذج المدرب"):
                joblib.dump(model, "model/trained_model.pkl")
                st.success("✅ تم حفظ النموذج المدرب داخل مجلد model")
        except Exception as e:
            st.error(f"❌ حدث خطأ أثناء التدريب: {str(e)}")

