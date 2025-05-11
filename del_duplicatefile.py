import streamlit as st
from github import Github

st.title("حذف ملفات من GitHub - مشروع Streamlit")

# إدخال بيانات الوصول
token = st.text_input("GitHub Token", type="password")
repo_name = st.text_input("اسم الريبو (مثال: username/repo)")

# تحديد الملفات المطلوب حذفها (النسختين)
files_to_delete = [
    "pages/Train_modelv2.py",
    "pages/pages/Train_modelv2.py"
]

if st.button("احذف الملفات"):
    try:
        g = Github(token)
        repo = g.get_repo(repo_name)
        deleted = []

        for path in files_to_delete:
            try:
                contents = repo.get_contents(path)
                repo.delete_file(
                    contents.path,
                    f"حذف الملف {path} عبر Streamlit",
                    contents.sha
                )
                deleted.append(path)
            except:
                st.warning(f"لم يتم العثور على الملف: {path}")

        if deleted:
            st.success(f"تم حذف الملفات التالية: {', '.join(deleted)}")
        else:
            st.info("لم يتم حذف أي ملف.")
    except Exception as e:
        st.error(f"حدث خطأ: {e}")