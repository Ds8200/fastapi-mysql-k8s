# Dockerfile לבניית תמונת FastAPI
# מבוסס על Python 3.11 slim image

FROM python:3.11-slim

# הגדרת תיקיית עבודה
WORKDIR /app

# העתקת קובץ requirements והתקנת תלויות
# זה נעשה בנפרד כדי לנצל Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# העתקת קוד האפליקציה
COPY app/ ./app/

# חשיפת פורט 8000 (פורט ברירת המחדל של FastAPI)
EXPOSE 8000

# הרצת האפליקציה עם uvicorn
# --host 0.0.0.0 מאפשר גישה מכל רשת
# --port 8000 מגדיר את הפורט
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

