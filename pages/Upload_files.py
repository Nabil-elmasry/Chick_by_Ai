
import streamlit as st
import pandas as pd

st.set_page_config(page_title="تحميل ملفات المشروع", layout="wide")
st.title("تحميل ملفات CSV وTXT و Word")

file = st.file_uploader("ارفع ملف (csv أو txt أو word)", type=["csv", "txt", "docx"])

if file:
    file_name = file.name
    st.write(f"**تم تحميل الملف:** {file_name}")

    if file_name.endswith(".csv"):
        df = pd.read_csv(file)
        st.subheader("معاينة محتوى CSV:")
        st.dataframe(df)

    elif file_name.endswith(".txt"):
        text = file.read().decode("utf-8")
        st.subheader("محتوى ملف TXT:")
        st.text_area("نص الملف:", value=text, height=300)

    elif file_name.endswith(".docx"):
        import docx
        doc = docx.Document(file)
        fullText = "\n".join([para.text for para in doc.paragraphs])
        st.subheader("محتوى ملف Word:")
        st.text_area("نص الملف:", value=fullText, height=300)

