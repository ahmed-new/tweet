
FROM python:3.12.4-slim


WORKDIR /app



COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt


COPY . .


CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000"]
