
import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

st.set_page_config(page_title="Model Training", layout="wide")
st.markdown("<h1 style='color:white; background-color:#007acc; padding:20px; border-radius:12px; text-align:center;'>Train the AI Diagnostic Model</h1>", unsafe_allow_html=True)

# تحميل البيانات
data_path = "Carset.csv"
if not os.path.exists(data_path):
    st.error("Carset.csv file not found. Please make sure the dataset is in the main directory.")
else:
    df = pd.read_csv(data_path)

    # عرض عينة من البيانات
    st.subheader("Sample of the dataset:")
    st.dataframe(df.head())

    # اختيار العمود الهدف
    target_column = st.selectbox("Select the target column (the fault column):", df.columns)

    # تجهيز البيانات
    X = df.drop(columns=[target_column])
    y = df[target_column]

    # تقسيم البيانات
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # تدريب النموذج
    if st.button("Train Model"):
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        acc = model.score(X_test, y_test)

        # حفظ النموذج
        joblib.dump(model, "trained_model.pkl")

        st.success(f"Model trained successfully with accuracy: {acc:.2%}")
        st.info("Model saved as 'trained_model.pkl'.")
