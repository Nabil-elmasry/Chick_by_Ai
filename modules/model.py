
# model.py
import joblib
from sklearn.ensemble import RandomForestClassifier  # استخدام نموذج RandomForest للتدريب

def train_and_save_model(X_train, y_train, model_path='fault_model.pkl'):
    """
    تقوم هذه الدالة بتدريب نموذج RandomForest باستخدام بيانات التدريب (X_train و y_train)
    ثم حفظ النموذج المدرب في ملف باستخدام joblib.

    :param X_train: بيانات التدريب (المميزات)
    :param y_train: البيانات المستهدفة (الفئات)
    :param model_path: اسم الملف الذي سيتم حفظ النموذج فيه (افتراضيًا "fault_model.pkl")
    :return: النموذج المدرب
    """
    # تدريب نموذج RandomForest
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # حفظ النموذج المدرب
    joblib.dump(model, model_path)
    print(f"تم حفظ النموذج في الملف {model_path}")

    return model
