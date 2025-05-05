
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


from sklearn.metrics import classification_report, confusion_matrix
import pandas as pd

def evaluate_model(X, y, model=None):
    """
    تقييم النموذج بعد التدريب باستخدام بيانات التدريب نفسها (أو نموذج مخصص).
    
    المعاملات:
    - X: ميزات التدريب
    - y: تسميات التدريب
    - model: إذا لم يتم تمرير نموذج، سيتم تدريب نموذج جديد
    
    العائدات:
    - y_pred: التوقعات
    - report_df: تقرير التصنيف كـ DataFrame
    - cm: مصفوفة الالتباس
    """
    from sklearn.ensemble import RandomForestClassifier

    if model is None:
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X, y)

    y_pred = model.predict(X)

    # تقرير التصنيف
    report_dict = classification_report(y, y_pred, output_dict=True)
    report_df = pd.DataFrame(report_dict).transpose()

    # مصفوفة الالتباس
    cm = confusion_matrix(y, y_pred)

    return y_pred, report_df, cm