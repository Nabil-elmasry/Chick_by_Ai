import os

# اسم الملف اللي عايز تحذفه (بدقة)
file_to_delete = "pages/train_model_v2 (1).py"

try:
    os.remove(file_to_delete)
    print(f"{file_to_delete} تم حذفه بنجاح.")
except FileNotFoundError:
    print(f"{file_to_delete} غير موجود.")
except Exception as e:
    print(f"حدث خطأ: {e}")