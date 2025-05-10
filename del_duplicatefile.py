import requests

# بيانات المستودع
OWNER = "اسم_المستخدم_بتاعك"
REPO = "اسم_المشروع"
FILE_PATH = "pages/train_model_v2 (1).py"  # غيّره حسب اسم الملف اللي عايز تمسحه
TOKEN = "ghp_xxxxxxxxxxxxxxxxxxxxxxxxx"  # ضع التوكن هنا

# Get file SHA (مهم لحذف الملف)
url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{FILE_PATH}"
headers = {"Authorization": f"token {TOKEN}"}
res = requests.get(url, headers=headers)
if res.status_code == 200:
    sha = res.json()["sha"]

    # حذف الملف
    delete_url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{FILE_PATH}"
    delete_data = {
        "message": "delete duplicate file",
        "sha": sha,
        "branch": "main"  # غيّرها لو الفرع اسمه غير كده
    }
    delete_res = requests.delete(delete_url, headers=headers, json=delete_data)
    if delete_res.status_code == 200:
        print("تم حذف الملف بنجاح.")
    else:
        print("فشل الحذف:", delete_res.json())
else:
    print("لم يتم العثور على الملف:", res.json())