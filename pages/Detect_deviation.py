صفحة كشف الانحراف في قراءات الحساسات

import streamlit as st import pandas as pd import numpy as np import joblib import plotly.graph_objects as go

إعداد الصفحة

st.set_page_config(page_title="كشف الانحراف - النموذج المدرب", layout="wide") st.title("🔍 صفحة كشف الانحراف في قراءات الحساسات")

تحميل النموذج المدرب

model = joblib.load("trained_model.pkl")

st.markdown("### 1️⃣ ارفع ملف قراءات الحساسات للسيارة المشكوك في حالتها") anomaly_file = st.file_uploader("ارفع ملف الحساسات (بها عطل متوقع)", type="csv")

if anomaly_file: anomaly_df = pd.read_csv(anomaly_file) st.success("✅ تم رفع البيانات بنجاح") st.dataframe(anomaly_df.head())

# التنبؤ بالقيم المتوقعة من النموذج المدرب
predicted = model.predict(anomaly_df)
predicted_df = pd.DataFrame(predicted, columns=anomaly_df.columns)

# حساب الانحراف
deviation_df = np.abs(anomaly_df - predicted_df)
deviation_df["sensor"] = deviation_df.index

st.markdown("### 2️⃣ جدول الانحراف لكل حساس")
st.dataframe(deviation_df.drop(columns=["sensor"]))

# رسم بياني للانحراف
st.markdown("### 3️⃣ رسم بياني للانحراف")
fig = go.Figure()

for col in anomaly_df.columns:
    fig.add_trace(go.Bar(
        x=[col],
        y=[deviation_df[col].mean()],
        name=col,
        marker_color='crimson' if deviation_df[col].mean() > 0.3 else 'orange' if deviation_df[col].mean() > 0.1 else 'green'
    ))

fig.update_layout(
    title="متوسط الانحراف لكل حساس",
    xaxis_title="اسم الحساس",
    yaxis_title="قيمة الانحراف",
    height=500,
    plot_bgcolor='white',
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# حفظ الانحرافات كملف CSV
st.markdown("### 📥 تحميل جدول الانحراف")
csv = deviation_df.drop(columns=["sensor"]).to_csv(index=False).encode('utf-8')
st.download_button("⬇️ تحميل ملف الانحراف", data=csv, file_name="deviation_report.csv", mime="text/csv")

