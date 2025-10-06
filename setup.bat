@echo off
REM Lost & Found Portal - Windows Setup Script

echo ========================================
echo    Lost & Found Portal - Setup
echo ========================================
echo.

REM Check Python installation
echo [INFO] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)
echo [SUCCESS] Python found

REM Check pip installation
echo [INFO] Checking pip installation...
pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip is not installed. Please install pip.
    pause
    exit /b 1
)
echo [SUCCESS] pip found

REM Create virtual environment
echo [INFO] Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo [SUCCESS] Virtual environment created
) else (
    echo [WARNING] Virtual environment already exists
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip --quiet

REM Install Python dependencies
echo [INFO] Installing Python dependencies...
pip install -r requirements.txt --quiet
echo [SUCCESS] Dependencies installed

REM Create necessary directories
echo [INFO] Creating directories...
if not exist "media\lost_items" mkdir media\lost_items
if not exist "static\css" mkdir static\css
if not exist "static\js" mkdir static\js
if not exist "static\images" mkdir static\images
if not exist "logs" mkdir logs
echo [SUCCESS] Directories created

REM Create .env file if not exists
if not exist ".env" (
    echo [INFO] Creating .env file...
    (
        echo # Django Settings
        echo SECRET_KEY=django-insecure-s*y$^&q+j^(2^&8=mbs^(!hf1mac6@g0#bo^a#p8%%-=fusfi@n2wh-
        echo DEBUG=True
        echo ALLOWED_HOSTS=localhost,127.0.0.1
        echo.
        echo # Database Settings
        echo DATABASE_ENGINE=django.db.backends.sqlite3
        echo DATABASE_NAME=db.sqlite3
        echo.
        echo # Email Settings
        echo EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
        echo EMAIL_HOST=smtp.gmail.com
        echo EMAIL_PORT=587
        echo EMAIL_USE_TLS=True
        echo EMAIL_HOST_USER=lostandfound.vpmrzshah@gmail.com
        echo EMAIL_HOST_PASSWORD=olcn hlep cryq bvag
        echo.
        echo # Base URL
        echo BASE_URL=http://127.0.0.1:8000
    ) > .env
    echo [SUCCESS] .env file created
) else (
    echo [WARNING] .env file already exists
)

REM Run migrations
echo [INFO] Running database migrations...
python manage.py makemigrations
python manage.py migrate
echo [SUCCESS] Database migrated

REM Create superuser
echo [INFO] Create superuser account...
set /p create_super="Do you want to create a superuser? (y/n): "
if /i "%create_super%"=="y" (
    python manage.py createsuperuser
)

REM Collect static files
echo [INFO] Collecting static files...
python manage.py collectstatic --noinput --clear
echo [SUCCESS] Static files collected

echo.
echo ========================================
echo        Setup Complete!
echo ========================================
echo.
echo [SUCCESS] Virtual environment: activated
echo [SUCCESS] Dependencies: installed
echo [SUCCESS] Database: migrated
echo [SUCCESS] Static files: collected
echo.
echo Next Steps:
echo 1. Activate venv: venv\Scripts\activate
echo 2. Run server: python manage.py runserver
echo 3. Open: http://localhost:8000/
echo.
echo Admin Panel: http://localhost:8000/admin/
echo.
echo [NOTE] Edit .env file for configuration
echo.
pause
