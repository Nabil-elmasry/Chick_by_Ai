import os

# المسار للمجلد اللي فيه الصفحات
pages_dir = "pages"

# جمع كل أسماء الملفات داخل المجلد
files = os.listdir(pages_dir)

# عمل قائمة بالملفات اللي فيها نفس الاسم "train_model_v2"
duplicates = [f for f in files if f.startswith("train_model_v2") and f.endswith(".py")]

# لو فيه أكتر من ملف بنفس الاسم
if len(duplicates) > 1:
    # نحذف كل الملفات ما عدا أول واحد
    for file in duplicates[1:]:
        file_path = os.path.join(pages_dir, file)
        try:
            os.remove(file_path)
            print(f"تم حذف الملف: {file_path}")
        except Exception as e:
            print(f"خطأ أثناء الحذف: {e}")
else:
    print("لا يوجد ملفات مكررة.")