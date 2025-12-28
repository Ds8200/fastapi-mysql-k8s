"""
מודול חיבור למסד הנתונים MySQL
משתמש ב-SQLAlchemy לחיבור דינמי למסד הנתונים
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# קריאת משתני סביבה מ-ConfigMap ו-Secret
# משתנים אלה מוגדרים ב-Kubernetes ומזריקים אוטומטית ל-Pod
DB_USER = os.getenv("MYSQL_USER")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
DB_NAME = os.getenv("MYSQL_DATABASE")
# שם ה-Service של MySQL ב-Kubernetes (DNS פנימי)
DB_HOST = os.getenv("MYSQL_HOST")

# בניית כתובת חיבור למסד הנתונים
# פורמט: mysql+pymysql://user:password@host:port/database
DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}"
)

# יצירת Engine - מנהל החיבור למסד הנתונים
engine = create_engine(DATABASE_URL)

# יצירת Session Factory - מפעל ליצירת sessions
SessionLocal = sessionmaker(bind=engine)

