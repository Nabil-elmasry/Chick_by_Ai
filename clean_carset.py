#### الكود المطلوب (`clean_carset.py`):
```python
import pandas as pd
import re

def clean_carset(input_file, output_file):
    # 1. قراءة الملف (مع التعامل مع الأسطر غير المنتظمة)
    df = pd.read_csv(input_file, encoding='latin1', on_bad_lines='skip')
    
    # 2. استخراج الأعمدة الأساسية
    cleaned_data = []
    for _, row in df.iterrows():
        # مثال لاستخراج القيم (تعديل حسب هيكل ملفك الفعلي)
        sensor = row.get('Sensor', '')
        value = row.get('Value', '')
        fault_codes = re.findall(r'P\d{4}', str(row))  # استخراج أكواد الأعطال
        
        if sensor or value or fault_codes:
            cleaned_data.append({
                'Sensor': sensor,
                'Value': value,
                'Fault_Codes': ', '.join(fault_codes) if fault_codes else 'No Code'
            })
    
    # 3. حفظ البيانات المنظفة
    pd.DataFrame(cleaned_data).to_csv(output_file, index=False)
    print(f"تم تنظيف البيانات وحفظها في {output_file}")

# استخدام الملف
clean_carset("Carset (10).csv", "Cleaned_Carset.csv"