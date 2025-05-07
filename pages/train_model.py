import streamlit as st import pandas as pd import os

st.set_page_config(page_title="صفحة تدريب النموذج", page_icon="🧠") st.title("🧠 تدريب نموذج الذكاء الاصطناعي")

إنشاء مجلد data إذا لم يكن موجودًا

if not os.path.exists("data"): os.makedirs("data")

تحميل ملفات الحساسات و carset

st.subheader("📤 تحميل الملفات") sensor_file = st.file_uploader("➕ حمّل ملف الحساسات", type=["csv"]) carset_file = st.file_uploader("➕ حمّل ملف carset", type=["csv"])

حالة لحفظ الملفات

files_saved = False merge_ready = False merged_file_saved = False

if sensor_file and carset_file: if st.button("📁 إضافة record_id وحفظ الملفات"): sensor_df = pd.read_csv(sensor_file) carset_df = pd.read_csv(carset_file)

# حفظ الملفات داخل مجلد data
    sensor_df.to_csv("data/sensors.csv", index=False)
    carset_df.to_csv("data/carset.csv", index=False)
    st.success("✅ تم حفظ الملفات بنجاح داخل مجلد data")
    files_saved = True

    # حفظ حالة في الجلسة
    st.session_state["files_saved"] = True
    st.session_state["sensor_df"] = sensor_df
    st.session_state["carset_df"] = carset_df

زر دمج الملفات

if st.session_state.get("files_saved"): if st.button("🔗 دمج الملفات"): sensor_df = st.session_state["sensor_df"] carset_df = st.session_state["carset_df"]

try:
        merged_df = pd.merge(sensor_df, carset_df, on="record_id", how="inner")
        merged_df.to_csv("data/merged.csv", index=False)
        st.success("✅ تم دمج الملفات وحفظها باسم merged.csv")
        st.session_state["merge_ready"] = True
    except Exception as e:
        st.error(f"❌ فشل الدمج: {e}")

زر بدء التدريب

if st.session_state.get("merge_ready"): if st.button("🚀 ابدأ التدريب"): try: from preprocessing import prepare_training_data from sklearn.ensemble import RandomForestClassifier from sklearn.model_selection import train_test_split from sklearn.metrics import accuracy_score

merged_df = pd.read_csv("data/merged.csv")
        sensor_df = pd.read_csv("data/sensors.csv")
        carset_df = pd.read_csv("data/carset.csv")

        X, y = prepare_training_data(sensor_df, carset_df)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = RandomForestClassifier()
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        st.success(f"✅ تم تدريب النموذج بنجاح بدقة: {accuracy:.2f}")
    except Exception as e:
        st.error(f"❌ حدث خطأ أثناء التدريب: {e}")

