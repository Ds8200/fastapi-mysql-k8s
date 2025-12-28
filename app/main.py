"""
FastAPI Application - אפליקציית FastAPI ראשית
מספקת API endpoints לחיבור עם מסד הנתונים MySQL
"""
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import SessionLocal

# יצירת אפליקציית FastAPI
app = FastAPI(
    title="FastAPI MySQL Kubernetes",
    description="אפליקציית FastAPI המחוברת ל-MySQL ב-Kubernetes",
    version="1.0.0"
)


def get_db():
    """
    Dependency function - מספק session למסד הנתונים
    מבטיח סגירה אוטומטית של החיבור לאחר השימוש
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    """
    Endpoint ראשי - בדיקת תקינות האפליקציה
    """
    return {
        "message": "ברוכים הבאים ל-FastAPI MySQL Kubernetes",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint - בדיקת תקינות האפליקציה
    """
    return {"status": "healthy"}


@app.get("/db/check")
async def check_database(db: Session = Depends(get_db)):
    """
    בדיקת חיבור למסד הנתונים
    מבצע שאילתה פשוטה לוודא שהחיבור עובד
    """
    try:
        # ביצוע שאילתת בדיקה
        result = db.execute(text("SELECT 1"))
        return {
            "status": "connected",
            "message": "חיבור למסד הנתונים תקין",
            "database": "MySQL"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"שגיאה בחיבור למסד הנתונים: {str(e)}"
        )


@app.get("/db/info")
async def database_info(db: Session = Depends(get_db)):
    """
    קבלת מידע על מסד הנתונים
    מחזיר את שם מסד הנתונים הנוכחי
    """
    try:
        # קבלת שם מסד הנתונים הנוכחי
        result = db.execute(text("SELECT DATABASE()"))
        db_name = result.scalar()
        return {
            "database_name": db_name,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"שגיאה בקבלת מידע: {str(e)}"
        )

