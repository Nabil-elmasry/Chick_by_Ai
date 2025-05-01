
import pandas as pd

def prepare_training_data(sensor_df: pd.DataFrame, carset_df: pd.DataFrame):
    """
    يدمج بيانات الحساسات مع بيانات الأعطال حسب العمود المشترك، ثم يجهز بيانات التدريب.
    """
    # تأكد أن عندك عمود مشترك مثل "record_id" أو "id"
    merged_df = pd.merge(sensor_df, carset_df, on="record_id", how="inner")

    # نفترض أن العمود اللي فيه العطل اسمه "fault_code"
    y = merged_df["fault_code"]
    X = merged_df.drop(columns=["fault_code", "record_id"])  # استبعد الأعمدة غير المفيدة

    return X, y
