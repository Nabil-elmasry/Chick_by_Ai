pages/predict_fault_final.py

import streamlit as st import pandas as pd import numpy as np import matplotlib.pyplot as plt import seaborn as sns import joblib import os

st.set_page_config(page_title="📊 كشف الانحراف وتوقع الأعطال", layout="wide") st.title("📊 توقع الأعطال وتحليل انحراف قراءات الحساسات")

st.markdown("""

🚗 ارفع الملفات المطلوبة

ارفع النموذج المدرب .pkl وملف قراءات الحساسات الفعلية .csv (قد يكون من جهاز Lunch) """)

model_file = st.file_uploader("📥 ارفع ملف النموذج المدرب (.pkl)", type=["pkl"]) data_file = st.file_uploader("📥 ارفع ملف الحساسات الفعلية (.csv)", type=["csv"])

threshold = st.slider("📏 اختر الحد الحرج للانحراف", 0.0, 1.0, 0.5, step=0.01)

if st.button("🚀 تحليل البيانات وتوقع العطل"): if model_file is None or data_file is None: st.error("❌ الرجاء رفع كلا الملفين أولاً") else: try: model = joblib.load(model_file) df = pd.read_csv(data_file) st.success("✅ تم تحميل البيانات") st.dataframe(df.head())

model_features = model.feature_names_in_
        if not all(col in df.columns for col in model_features):
            st.error("⚠️ ملف البيانات لا يحتوي على نفس الأعمدة التي تم تدريب النموذج عليها")
        else:
            df = df[model_features]
            prediction = model.predict_proba(df)[:, 0]
            deviation_scores = 1 - prediction
            avg_deviation = np.mean(deviation_scores)

            st.markdown(f"### 🔍 متوسط درجة الانحراف: **{avg_deviation:.2f}** من 1.0")
            status = "⚠️ يوجد انحراف واضح عن القيم الطبيعية" if avg_deviation > threshold else "✅ القيم ضمن النطاق الطبيعي"
            st.markdown(f"### النتيجة: {status}")

            st.subheader("📉 رسم بياني لانحراف قراءات الحساسات")
            fig, ax = plt.subplots(figsize=(12, 5))
            sns.lineplot(data=deviation_scores, ax=ax, marker="o", color="#FF5733")
            ax.axhline(threshold, color='blue', linestyle='--', label='الحد الحرج')
            ax.set_title("انحراف القيم عن الطبيعي", fontsize=14)
            ax.set_ylabel("درجة الانحراف")
            ax.set_xlabel("القراءة")
            ax.legend()
            st.pyplot(fig)

            st.subheader("📋 القيم المنحرفة بالتفصيل")
            df_with_dev = df.copy()
            df_with_dev["deviation_score"] = deviation_scores
            outliers_df = df_with_dev[df_with_dev["deviation_score"] > threshold]
            st.dataframe(outliers_df)

            st.subheader("🧾 تقرير المقارنة الفردية")
            report_lines = []
            report_lines.append("تقرير التحليل:")
            report_lines.append("متوسط الانحراف: {:.2f}".format(avg_deviation))
            report_lines.append("الحد الحرج: {:.2f}".format(threshold))
            report_lines.append("النتيجة: {}".format(status))
            report_lines.append("\n---\nتفاصيل الحساسات المنحرفة:")

            for i, row in outliers_df.iterrows():
                report_lines.append("- قراءة رقم {}:".format(i+1))
                for col in model_features:
                    report_lines.append("    • {}: {}".format(col, row[col]))
                report_lines.append("    ⚠️ درجة الانحراف: {:.2f}".format(row['deviation_score']))
                report_lines.append("")

            report_text = "\n".join(report_lines)

            # حفظ الملف في مجلد data
            os.makedirs("data", exist_ok=True)
            report_path = "data/fault_report.txt"
            with open(report_path, "w", encoding="utf-8") as f:
                f.write(report_text)

            with open(report_path, "r", encoding="utf-8") as file:
                st.markdown("### 📥 تحميل التقرير النهائي")
                st.download_button(
                    label="⬇️ اضغط هنا لحفظ التقرير على الموبايل",
                    data=file.read(),
                    file_name="fault_report.txt",
                    mime="text/plain"
                )

    except Exception as e:
        st.error("❌ حدث خطأ أثناء التحليل:")
        st.exception(e)

