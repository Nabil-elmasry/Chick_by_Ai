
modules/data_loader.py

import pandas as pd

def load_sensor_data(file):
    """
    تحميل بيانات الحساسات من ملف CSV.
    """
    try:
        df = pd.read_csv(file)
        df.dropna(inplace=True)  # حذف أي صفوف تحتوي على بيانات ناقصة
        return df
    except Exception as e:
        raise ValueError(f"خطأ أثناء تحميل بيانات الحساسات: {e}")

def load_carset(file):
    """
    تحميل بيانات Carset التي تحتوي على رموز الأعطال.
    """
    try:
        df = pd.read_csv(file)
        df.dropna(inplace=True)  # حذف أي صفوف تحتوي على بيانات ناقصة
        return df
    except Exception as e:
        raise ValueError(f"خطأ أثناء تحميل ملف Carset: {e}")

