pages/predict_fault_final.py

import streamlit as st import pandas as pd import numpy as np import matplotlib.pyplot as plt import seaborn as sns import joblib import base64

st.set_page_config(page_title="📊 كشف الانحراف وتوقع الأعطال", layout="wide") st.title("📊 توقع الأعطال وتحليل انحراف قراءات الحساسات")

st.markdown("""

🚗 ارفع الملفات المطلوبة

ارفع النموذج المدرب .pkl وملف قراءات الحساسات الفعلية .csv (قد يكون من جهاز Lunch) """)

model_file = st.file_uploader("📥 ارفع ملف النموذج المدرب (.pkl)", type=["pkl"]) data_file = st.file_uploader("📥 ارفع ملف الحساسات الفعلية (.csv)", type=["csv"])

threshold = st.slider("📏 اختر الحد الحرج للانحراف", 0.0, 1.0, 0.5, step=0.01)

if st.button("🚀 تحليل البيانات وتوقع العطل"): if model_file is None or data_file is None: st.error("❌ الرجاء رفع كلا الملفين أولاً") else: try: # تحميل النموذج model = joblib.load(model_file)

# تحميل البيانات
        df = pd.read_csv(data_file)
        st.success("✅ تم تحميل البيانات")
        st.dataframe(df.head())

        # التأكد من الأعمدة المطلوبة
        model_features = model.feature_names_in_
        if not all(col in df.columns for col in model_features):
            st.error("⚠️ ملف البيانات لا يحتوي على نفس الأعمدة التي تم تدريب النموذج عليها")
        else:
            df = df[model_features]
            prediction = model.predict_proba(df)[:, 0]
            deviation_scores = 1 - prediction
            avg_deviation = np.mean(deviation_scores)

            # تقرير عام
            st.markdown(f"### 🔍 متوسط درجة الانحراف: **{avg_deviation:.2f}** من 1.0")
            if avg_deviation > threshold:
                status = "⚠️ يوجد انحراف واضح عن القيم الطبيعية"
            else:
                status = "✅ القيم ضمن النطاق الطبيعي"
            st.markdown(f"### النتيجة: {status}")

            # رسم بياني للانحراف
            st.subheader("📉 رسم بياني لانحراف قراءات الحساسات")
            fig, ax = plt.subplots(figsize=(12, 5))
            sns.lineplot(data=deviation_scores, ax=ax, marker="o", color="#FF5733")
            ax.axhline(threshold, color='blue', linestyle='--', label='الحد الحرج')
            ax.set_title("انحراف القيم عن الطبيعي", fontsize=14)
            ax.set_ylabel("درجة الانحراف")
            ax.set_xlabel("القراءة")
            ax.legend()
            st.pyplot(fig)

            # جدول الحساسات المنحرفة
            st.subheader("📋 القيم المنحرفة بالتفصيل")
            df_with_dev = df.copy()
            df_with_dev["deviation_score"] = deviation_scores
            outliers_df = df_with_dev[df_with_dev["deviation_score"] > threshold]
            st.dataframe(outliers_df)

            # تقرير المقارنة الفردية
            st.subheader("🧾 تقرير المقارنة الفردية")
            compare_lines = []
            for i, row in outliers_df.iterrows():
                entry = f"- قراءة رقم {i+1}:\n"
                for col in model_features:
                    entry += f"    • {col}: {row[col]}\n"
                entry += f"    ⚠️ درجة الانحراف: {row['deviation_score']:.2f}\n"
                compare_lines.append(entry)
            compare_summary = "\n".join(compare_lines)
            st.code(compare_summary, language="text")

            # تقرير نصي وتحميله
            report_text = f"تقرير التحليل:\nمتوسط الانحراف: {avg_deviation:.2f}\nالحد الحرج: {threshold}\nالنتيجة: {status}\n\n---\nتفاصيل الحساسات المنحرفة:\n{compare_summary}"
            b64 = base64.b64encode(report_text.encode()).decode()
            href = f'<a href="data:file/txt;base64,{b64}" download="fault_report.txt">⬇️ تحميل التقرير على الموبايل</a>'
            st.markdown("### 📥 تحميل التقرير النهائي")
            st.markdown(href, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ حدث خطأ أثناء التحليل: {e}")

