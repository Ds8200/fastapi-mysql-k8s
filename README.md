# 🚀 FastAPI MySQL Kubernetes - מדריך למתחילים

פרויקט מלא להרצת אפליקציית FastAPI עם מסד נתונים MySQL על Kubernetes.  
מדריך זה מיועד למתחילים ומסביר כל שלב בפירוט.

---

## 📋 תוכן עניינים

1. [מה הפרויקט עושה?](#מה-הפרויקט-עושה)
2. [דרישות מוקדמות](#דרישות-מוקדמות)
3. [מבנה הפרויקט](#מבנה-הפרויקט)
4. [הסבר על רכיבי Kubernetes](#הסבר-על-רכיבי-kubernetes)
5. [התקנה והרצה - שלב אחר שלב](#התקנה-והרצה---שלב-אחר-שלב)
6. [גישה לאפליקציה](#גישה-לאפליקציה)
7. [פקודות שימושיות](#פקודות-שימושיות)
8. [מחיקת הפרויקט](#מחיקת-הפרויקט)
9. [פתרון בעיות](#פתרון-בעיות)

---

## 🎯 מה הפרויקט עושה?

הפרויקט מדגים איך להריץ:
- ✅ **FastAPI** - אפליקציית API מודרנית (Python)
- ✅ **MySQL** - מסד נתונים יחסי
- ✅ **Kubernetes** - ניהול containers בקלאסטר
- ✅ **Persistent Storage** - שמירת נתונים גם אחרי restart
- ✅ **Load Balancing** - מספר instances של FastAPI

### מה האפליקציה עושה?

האפליקציה מספקת API endpoints:
- `GET /` - הודעת ברוכים הבאים
- `GET /health` - בדיקת תקינות
- `GET /db/check` - בדיקת חיבור למסד הנתונים
- `GET /db/info` - מידע על מסד הנתונים

---

## 🔧 דרישות מוקדמות

לפני התחלה, ודא שיש לך:

### 1. Docker Desktop
- **למה?** כדי לבנות תמונות Docker ולהריץ Kubernetes
- **איך להתקין:** [הורד Docker Desktop](https://www.docker.com/products/docker-desktop)
- **איך לבדוק:**
  ```bash
  docker --version
  ```

### 2. Kubernetes (דרך Docker Desktop)
- **למה?** כדי להריץ את האפליקציה בקלאסטר
- **איך להפעיל:**
  1. פתח Docker Desktop
  2. לך ל-Settings → Kubernetes
  3. סמן "Enable Kubernetes"
  4. לחץ "Apply & Restart"
  5. המתן עד ש-Kubernetes מוכן (איקון ירוק)

### 3. kubectl (כלי שורת פקודה)
- **למה?** כדי לנהל את הקלאסטר
- **איך לבדוק:**
  ```bash
  kubectl version --client
  ```
- **אם לא מותקן:** Docker Desktop מתקין אותו אוטומטית

### 4. Python 3.11+ (אופציונלי - לפיתוח מקומי)
- **למה?** רק אם אתה רוצה להריץ את האפליקציה מקומית
- **איך לבדוק:**
  ```bash
  python --version
  ```

---

## 📁 מבנה הפרויקט

```
fastapi-mysql-k8s/
│
├── app/                          # קוד האפליקציה
│   ├── main.py                  # FastAPI endpoints
│   └── database.py              # חיבור ל-MySQL
│
├── k8s/                         # קבצי Kubernetes
│   ├── configmap.yaml          # קונפיגורציה (שמות DB, משתמשים)
│   ├── secret.yaml             # סודות (סיסמאות)
│   │
│   ├── mysql/                   # רכיבי MySQL
│   │   ├── pvc.yaml            # Persistent Volume (שמירת נתונים)
│   │   ├── deployment.yaml     # הגדרת MySQL Pod
│   │   └── service.yaml        # Service ל-MySQL
│   │
│   └── api/                     # רכיבי FastAPI
│       ├── deployment.yaml      # הגדרת FastAPI Pods
│       └── service.yaml         # Service ל-FastAPI
│
├── Dockerfile                   # בניית תמונת Docker
├── requirements.txt             # תלויות Python
└── README.md                    # קובץ זה
```

---

## 📚 הסבר על רכיבי Kubernetes

### 1. ConfigMap (`k8s/configmap.yaml`)
**מה זה?** קונפיגורציה לא סודית  
**מה יש שם?** שמות מסד נתונים ומשתמשים  
**למה?** כדי לא להגדיר קשיח בקוד

```yaml
MYSQL_DATABASE: testdb
MYSQL_USER: user
```

### 2. Secret (`k8s/secret.yaml`)
**מה זה?** מידע רגיש (סיסמאות)  
**מה יש שם?** סיסמאות MySQL  
**למה?** אבטחה - Kubernetes מצפין את זה

```yaml
MYSQL_PASSWORD: password
MYSQL_ROOT_PASSWORD: rootpassword
```

⚠️ **חשוב:** בפרודקשן יש להשתמש בסיסמאות חזקות!

### 3. PersistentVolumeClaim (`k8s/mysql/pvc.yaml`)
**מה זה?** דיסק קבוע לשמירת נתונים  
**למה?** כדי שהנתונים לא יאבדו כשהפוד מתחלף  
**גודל:** 5GB

**למה לא volume רגיל?**
- Volume רגיל (`emptyDir`) נמחק כשהפוד נמחק
- PVC נשמר גם אחרי שהפוד מתחלף
- חיוני למסדי נתונים!

### 4. MySQL Deployment (`k8s/mysql/deployment.yaml`)
**מה זה?** מגדיר איך MySQL ירוץ  
**מה יש שם?**
- תמונת Docker: `mysql:8.0`
- Replicas: 1 (רק instance אחד)
- Volume: מחובר ל-PVC
- משתני סביבה: מ-ConfigMap ו-Secret

### 5. MySQL Service (`k8s/mysql/service.yaml`)
**מה זה?** DNS פנימי ל-MySQL  
**למה?** כדי ש-FastAPI יוכל להתחבר ל-MySQL  
**שם:** `mysql-service` (נגיש רק בתוך הקלאסטר)

### 6. FastAPI Deployment (`k8s/api/deployment.yaml`)
**מה זה?** מגדיר איך FastAPI ירוץ  
**מה יש שם?**
- תמונת Docker: `fastapi-mysql:latest` (צריך לבנות)
- Replicas: 2 (2 instances ל-load balancing)
- פורט: 8000
- משתני סביבה: מ-ConfigMap ו-Secret

### 7. FastAPI Service (`k8s/api/service.yaml`)
**מה זה?** נקודת גישה ל-FastAPI  
**למה?** כדי לגשת לאפליקציה מבחוץ  
**פורט:** 80 (חיצוני) → 8000 (פנימי)

---

## 🚀 התקנה והרצה - שלב אחר שלב

### שלב 1: בדיקת התקנות

```bash
# בדיקת Docker
docker --version

# בדיקת Kubernetes
kubectl version --client

# בדיקת חיבור לקלאסטר
kubectl cluster-info
```

אם הכל עובד, המשך לשלב הבא.

### שלב 2: בניית תמונת Docker

```bash
# בניית תמונת FastAPI
docker build -t fastapi-mysql:latest .
```

**מה זה עושה?**
- קורא את ה-Dockerfile
- מתקין את התלויות מ-`requirements.txt`
- בונה תמונה בשם `fastapi-mysql:latest`

**איך לבדוק שהצליח?**
```bash
docker images | findstr fastapi-mysql
```

### שלב 3: הפעלת המשאבים ב-Kubernetes

```bash
# הפעלת כל המשאבים
kubectl apply -f k8s/
kubectl apply -f k8s/api
kubectl apply -f k8s/mysql
```

**מה זה עושה?**
- יוצר ConfigMap ו-Secret
- יוצר PVC (Persistent Volume)
- מפעיל MySQL (Deployment + Service)
- מפעיל FastAPI (Deployment + Service)

**איך לבדוק שהכל רץ?**
```bash
# בדיקת Pods (צריך לראות 3 pods: mysql + 2 fastapi)
kubectl get pods

# בדיקת Services
kubectl get svc

# בדיקת PVC
kubectl get pvc
```

**מתי Pods מוכנים?**
- צריך לראות `STATUS: Running`
- `READY: 1/1` (או `2/2` ל-FastAPI)
- זה יכול לקחת 1-2 דקות

**אם Pod לא רץ:**
```bash
# בדיקת לוגים
kubectl logs <pod-name>

# בדיקת פרטים
kubectl describe pod <pod-name>
```

### שלב 4: בדיקת תקינות

```bash
# בדיקת סטטוס כללי
kubectl get all

# בדיקת לוגים של FastAPI
kubectl logs -l app=fastapi

# בדיקת לוגים של MySQL
kubectl logs -l app=mysql
```

---

## 🌐 גישה לאפליקציה

יש שתי דרכים לגשת לאפליקציה:

### דרך 1: Port Forward (מומלץ למתחילים) ⭐

**למה?** הכי פשוט, לא דורש התקנות נוספות

```bash
# הפעלת Port Forward
kubectl port-forward service/fastapi-service 8000:80
```

**מה זה עושה?**
- מפנה את `localhost:8000` ל-`fastapi-service:80`
- הפקודה רצה עד שמבטלים עם `Ctrl+C`

**איך להשתמש:**
1. הפעל את הפקודה
2. פתח דפדפן: `http://localhost:8000`
3. נסה את ה-endpoints:
   - `http://localhost:8000/` - הודעת ברוכים הבאים
   - `http://localhost:8000/health` - בדיקת תקינות
   - `http://localhost:8000/db/check` - בדיקת חיבור ל-MySQL
   - `http://localhost:8000/db/info` - מידע על מסד הנתונים

**יתרונות:**
- ✅ פשוט ומהיר
- ✅ לא דורש התקנות נוספות
- ✅ עובד מיד

**חסרונות:**
- ❌ עובד רק כל עוד הפקודה רצה
- ❌ לא מתאים לפרודקשן

### דרך 2: Ingress (למתקדמים)

**למה?** גישה דרך דומיין (כמו `http://fastapi.local`)

**דרישות:**
1. התקנת Nginx Ingress Controller
2. עריכת קובץ hosts

**שלבים:**

1. **התקנת Ingress Controller:**
```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml
```

2. **המתן עד ש-Ingress Controller מוכן:**
```bash
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=90s
```

3. **הוספת דומיין ל-hosts:**
   - פתח: `C:\Windows\System32\drivers\etc\hosts` (כמנהל)
   - הוסף שורה:
   ```
   127.0.0.1 fastapi.local
   ```

4. **יצירת Ingress:**
```bash
# אם יש לך קובץ ingress.yaml
kubectl apply -f k8s/api/ingress.yaml
```

5. **גישה:**
   - פתח דפדפן: `http://fastapi.local`

**יתרונות:**
- ✅ גישה דרך דומיין
- ✅ מתאים לפרודקשן
- ✅ תומך ב-HTTPS

**חסרונות:**
- ❌ דורש התקנות נוספות
- ❌ יותר מורכב

---

## 💻 פקודות שימושיות

### ניהול Pods

```bash
# הצגת כל ה-Pods
kubectl get pods

# הצגת Pods עם פרטים נוספים
kubectl get pods -o wide

# בדיקת סטטוס Pod ספציפי
kubectl get pod <pod-name>

# מחיקת Pod (Kubernetes יוצר אחד חדש אוטומטית)
kubectl delete pod <pod-name>
```

### לוגים

```bash
# לוגים של כל ה-Pods של FastAPI
kubectl logs -l app=fastapi

# לוגים של Pod ספציפי
kubectl logs <pod-name>

# לוגים בזמן אמת (follow)
kubectl logs -f <pod-name>

# לוגים של Pod שנמחק
kubectl logs --previous <pod-name>
```

### Services

```bash
# הצגת כל ה-Services
kubectl get svc

# בדיקת Service ספציפי
kubectl describe svc <service-name>
```

### גישה ל-Pods

```bash
# כניסה ל-MySQL Pod
kubectl exec -it deployment/mysql -- bash

# הרצת פקודה ב-MySQL Pod
kubectl exec deployment/mysql -- mysql -u root -prootpassword

# כניסה ל-FastAPI Pod
kubectl exec -it deployment/fastapi -- bash
```

### בדיקת משאבים

```bash
# הצגת כל המשאבים
kubectl get all

# בדיקת ConfigMaps
kubectl get configmap

# בדיקת Secrets
kubectl get secret

# בדיקת PVCs
kubectl get pvc
```

### עדכון

```bash
# עדכון Deployment אחרי שינוי בקוד
kubectl rollout restart deployment/fastapi

# בדיקת סטטוס rollout
kubectl rollout status deployment/fastapi

# היסטוריית rollouts
kubectl rollout history deployment/fastapi
```

---

## 🗑️ מחיקת הפרויקט

### מחיקת כל המשאבים

```bash
# מחיקת כל המשאבים מ-Kubernetes
kubectl delete -f k8s/
kubectl delete -f k8s/api
kubectl delete -f k8s/mysql
```

**מה זה מוחק?**
- ✅ Pods (MySQL + FastAPI)
- ✅ Services
- ✅ Deployments
- ✅ ConfigMap
- ✅ Secret
- ⚠️ **PVC לא נמחק** (הנתונים נשמרים!)

### מחיקת PVC (זהירות - מוחק נתונים!)

```bash
# מחיקת PVC (זה ימחק את כל הנתונים!)
kubectl delete pvc mysql-pvc
```

### מחיקת תמונת Docker

```bash
# מחיקת תמונת FastAPI
docker rmi fastapi-mysql:latest
```

### מחיקת הכל (זהירות!)

```bash
# מחיקת כל המשאבים כולל PVC
kubectl delete -f k8s/
kubectl delete -f k8s/api
kubectl delete -f k8s/mysql
kubectl delete pvc mysql-pvc
docker rmi fastapi-mysql:latest
```

---

## 🔍 פתרון בעיות

### בעיה: Pod לא רץ

**תסמינים:**
- `STATUS: Pending` או `Error` או `CrashLoopBackOff`

**פתרונות:**
```bash
# בדיקת פרטי Pod
kubectl describe pod <pod-name>

# בדיקת לוגים
kubectl logs <pod-name>

# בדיקת events
kubectl get events --sort-by=.metadata.creationTimestamp
```

**סיבות נפוצות:**
- תמונת Docker לא קיימת (צריך לבנות)
- PVC לא נוצר
- שגיאת קונפיגורציה

### בעיה: FastAPI לא מתחבר ל-MySQL

**תסמינים:**
- `/db/check` מחזיר שגיאה
- לוגים מראים "connection refused"

**פתרונות:**
```bash
# בדיקת ש-MySQL רץ
kubectl get pods -l app=mysql

# בדיקת Service של MySQL
kubectl get svc mysql-service

# בדיקת לוגים של FastAPI
kubectl logs -l app=fastapi

# בדיקת ConfigMap ו-Secret
kubectl get configmap mysql-config -o yaml
kubectl get secret mysql-secret -o yaml
```

### בעיה: Port Forward לא עובד

**תסמינים:**
- `Error: unable to forward`

**פתרונות:**
```bash
# בדיקת ש-Service קיים
kubectl get svc fastapi-service

# בדיקת ש-Pods רצים
kubectl get pods -l app=fastapi

# נסה פורט אחר
kubectl port-forward service/fastapi-service 8080:80
```

### בעיה: תמונת Docker לא נמצאת

**תסמינים:**
- `ImagePullBackOff` או `ErrImageNeverPull`

**פתרונות:**
```bash
# בניית תמונה מחדש
docker build -t fastapi-mysql:latest .

# בדיקת שהתמונה קיימת
docker images | findstr fastapi-mysql

# אם צריך, עדכן את imagePullPolicy ל-Never
# (כבר מוגדר ב-deployment.yaml)
```

### בעיה: PVC לא נוצר

**תסמינים:**
- `Pending` ב-`kubectl get pvc`

**פתרונות:**
```bash
# בדיקת פרטי PVC
kubectl describe pvc mysql-pvc

# בדיקת StorageClass
kubectl get storageclass

# אם אין StorageClass, זה יכול להיות בעיה ב-Docker Desktop
# נסה restart ל-Docker Desktop
```

### בעיה: Kubernetes לא עובד

**תסמינים:**
- `kubectl cluster-info` מחזיר שגיאה

**פתרונות:**
1. פתח Docker Desktop
2. לך ל-Settings → Kubernetes
3. ודא ש-Kubernetes מופעל
4. נסה restart ל-Docker Desktop

---

## 📖 מושגים חשובים

### Pod
**מה זה?** Container (או מספר containers) שרצים יחד  
**דוגמה:** Pod של MySQL, Pod של FastAPI

### Deployment
**מה זה?** מנהל Pods - יוצר, מעדכן, ומחליף Pods  
**למה?** כדי להבטיח ש-Pods תמיד רצים

### Service
**מה זה?** DNS פנימי + Load Balancer  
**למה?** כדי לגשת ל-Pods דרך שם קבוע

### PVC (PersistentVolumeClaim)
**מה זה?** דיסק קבוע לשמירת נתונים  
**למה?** כדי שהנתונים לא יאבדו

### ConfigMap
**מה זה?** קונפיגורציה לא סודית  
**למה?** כדי לא להגדיר קשיח בקוד

### Secret
**מה זה?** מידע רגיש (סיסמאות)  
**למה?** אבטחה

---

## 🎓 צעדים הבאים

לאחר שהצלחת להריץ את הפרויקט:

1. **נסה לשנות קוד:**
   - ערוך `app/main.py`
   - בנה תמונה מחדש
   - עדכן Deployment

2. **נסה לשנות קונפיגורציה:**
   - ערוך `k8s/configmap.yaml`
   - עדכן ConfigMap
   - restart Pods

3. **נסה לשנות מספר replicas:**
   - ערוך `k8s/api/deployment.yaml`
   - שנה `replicas: 3`
   - עדכן Deployment

4. **למד על:**
   - Ingress (גישה דרך דומיין)
   - Secrets Management
   - Monitoring ו-Logging
   - CI/CD עם Kubernetes

---

## 📚 משאבים נוספים

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [Docker Documentation](https://docs.docker.com/)

---

## ⚠️ הערות חשובות

1. **סיסמאות:** בפרודקשן יש להשתמש בסיסמאות חזקות!
2. **PVC:** מחיקת PVC מוחקת את כל הנתונים!
3. **תמונות:** תמונת `fastapi-mysql:latest` צריכה להיות מקומית
4. **Port Forward:** עובד רק כל עוד הפקודה רצה

---

**בהצלחה! 🚀**

אם יש שאלות או בעיות, בדוק את הסעיף [פתרון בעיות](#פתרון-בעיות) או פתח issue.

#   f a s t a p i - m y s q l - k 8 s  
 #   f a s t a p i - m y s q l - k 8 s  
 