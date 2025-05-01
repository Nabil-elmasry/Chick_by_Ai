
# pages/train_model.py

import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

st.set_page_config(page_title="📊 تدريب النموذج", layout="wide")

st.title("📊 تدريب نموذج تنبؤ الأعطال")
st.write(
    """
    في هذه الصفحة يمكنك رفع ملف قراءات الحساسات للتدريب وملف Carset لاستخراج العلامات (Fault Codes)،
    ثم تدريب نموذج الـ Random Forest وحفظه تلقائيًا.
    """
)

# رفع ملفات CSV
sensor_file = st.file_uploader(
    "1. ارفع ملف الحساسات (sensor dataset)", type=["csv"], key="sensor_file"
)
carset_file = st.file_uploader(
    "2. ارفع ملف Carset (carset.csv)", type=["csv"], key="carset_file"
)

if st.button("🚀 ابدأ التدريب"):
    if sensor_file is None or carset_file is None:
        st.error("❌ الرجاء رفع كلا الملفين قبل البدء بالتدريب.")
    else:
        try:
            with st.spinner("⏳ جاري تحميل وتنظيف البيانات..."):
                sensor_df = pd.read_csv(sensor_file)
                carset_df = pd.read_csv(carset_file)

                if 'id' not in sensor_df.columns or 'id' not in carset_df.columns:
                    st.error("❌ الملفات يجب أن تحتوي على عمود 'id'. يرجى معالجتها في صفحة الدمج أولاً.")
                    st.stop()

                # الدمج على أساس id
                merged_df = pd.merge(sensor_df, carset_df, on="id")
            st.success("✅ تم تحميل ودمج البيانات بنجاح.")

            st.subheader("🧮 حدد الأعمدة للتدريب")
            input_features = st.multiselect("🔧 اختر الخصائص (features)", merged_df.columns.tolist())
            target_column = st.selectbox("🎯 اختر عمود الهدف (target)", merged_df.columns.tolist())

            if input_features and target_column:
                with st.spinner("⏳ جاري تجهيز البيانات..."):
                    X = merged_df[input_features]
                    y = merged_df[target_column]
                    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

                with st.spinner("⏳ جاري تدريب النموذج..."):
                    model = RandomForestClassifier()
                    model.fit(X_train, y_train)
                    y_pred = model.predict(X_test)

                st.success("🎉 تم تدريب النموذج بنجاح.")
                st.subheader("📈 تقرير الأداء")
                st.text(classification_report(y_test, y_pred))

                # حفظ النموذج
                import joblib
                joblib.dump(model, "fault_model.pkl")
                st.success("💾 تم حفظ النموذج في `fault_model.pkl`.")

            else:
                st.warning("⚠️ يرجى اختيار الخصائص والهدف.")

        except Exception as e:
            st.error(f"❌ حدث خطأ أثناء التدريب: {e}")


# زر لتحميل النموذج
                with open("fault_model.pkl", "rb") as f:
                    st.download_button(
                        label="⬇️ تحميل النموذج المدرب",
                        data=f,
                        file_name="fault_model.pkl",
                        mime="application/octet-stream"
                    )

