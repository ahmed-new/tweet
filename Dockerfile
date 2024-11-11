# استخدم صورة Python 3.12.4 slim
FROM python:3.12.4-slim

# تحديد مجلد العمل داخل الحاوية
WORKDIR /app



# نسخ متطلبات المشروع إلى الحاوية
COPY requirements.txt .

# تثبيت المتطلبات
RUN pip install --no-cache-dir -r requirements.txt

# نسخ باقي ملفات المشروع إلى الحاوية
COPY . .

# تحديد الأمر لتشغيل الخادم عند بدء الحاوية
CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000"]
