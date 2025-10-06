# 📦 Complete Installation Guide

## 🚀 Quick Start (Automated - Recommended)

### One-Command Installation:

**Linux/Mac:**
```bash
git clone https://github.com/NICK-FURY-6023/dear-project-1.git
cd dear-project-1
chmod +x setup.sh
./setup.sh
```

**Windows:**
```cmd
git clone https://github.com/NICK-FURY-6023/dear-project-1.git
cd dear-project-1
setup.bat
```

✅ **Done! Your application is ready to use.**

---

## 📋 What Gets Installed

The automated script installs and configures:

1. ✅ Python virtual environment
2. ✅ All required Python packages
3. ✅ System dependencies (JPEG, zlib)
4. ✅ Database (SQLite)
5. ✅ Environment variables (.env)
6. ✅ Static files
7. ✅ Media directories
8. ✅ Admin account (optional)

---

## 🔧 Manual Installation

<details>
<summary>Click for detailed manual steps</summary>

### Requirements:
- Python 3.8+
- pip
- Git

### Steps:

1. **Clone & Navigate:**
```bash
git clone https://github.com/NICK-FURY-6023/dear-project-1.git
cd dear-project-1
```

2. **Virtual Environment:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate      # Windows
```

3. **Install Dependencies:**
```bash
pip install -r requirements.txt
```

4. **Database Setup:**
```bash
python manage.py migrate
```

5. **Create Admin:**
```bash
python manage.py createsuperuser
```

6. **Run Server:**
```bash
python manage.py runserver
```

</details>

---

## 🌐 Access Your Application

After installation:
- **Website:** http://localhost:8000/
- **Admin:** http://localhost:8000/admin/

---

## ❓ Need Help?

See [README.md](README.md) for complete documentation.
