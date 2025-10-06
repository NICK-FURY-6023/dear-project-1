#!/bin/bash

# Lost & Found Portal - Automated Setup Script
# This script will automatically install all dependencies and setup the project

echo "🚀 Starting Lost & Found Portal Setup..."
echo "========================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Check if Python is installed
print_info "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
print_success "Python $PYTHON_VERSION found"

# Check if pip is installed
print_info "Checking pip installation..."
if ! command -v pip3 &> /dev/null; then
    print_error "pip is not installed. Installing pip..."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3 get-pip.py
    rm get-pip.py
fi
print_success "pip is installed"

# Create virtual environment
print_info "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_warning "Virtual environment already exists"
fi

# Activate virtual environment
print_info "Activating virtual environment..."
source venv/bin/activate
print_success "Virtual environment activated"

# Upgrade pip
print_info "Upgrading pip..."
pip install --upgrade pip --quiet
print_success "pip upgraded"

# Install system dependencies for Pillow
print_info "Installing system dependencies..."
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if command -v apt-get &> /dev/null; then
        print_info "Detected Debian/Ubuntu system"
        sudo apt-get update -qq
        sudo apt-get install -y libjpeg-dev zlib1g-dev -qq
        print_success "System dependencies installed"
    elif command -v yum &> /dev/null; then
        print_info "Detected RedHat/CentOS system"
        sudo yum install -y libjpeg-devel zlib-devel -q
        print_success "System dependencies installed"
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    print_info "Detected macOS system"
    if command -v brew &> /dev/null; then
        brew install libjpeg zlib
        print_success "System dependencies installed"
    else
        print_warning "Homebrew not found. Please install libjpeg and zlib manually."
    fi
fi

# Install Python dependencies
print_info "Installing Python dependencies from requirements.txt..."
pip install -r requirements.txt --quiet
print_success "Python dependencies installed"

# Create necessary directories
print_info "Creating necessary directories..."
mkdir -p media/lost_items
mkdir -p static/css static/js static/images
mkdir -p logs
print_success "Directories created"

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_info "Creating .env file from template..."
    cat > .env << EOL
# Django Settings
SECRET_KEY=django-insecure-s*y$&q+j(2&8=mbs(!hf1mac6@g0#bo^a#p8%-=fusfi@n2wh-
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Settings (SQLite - Development)
DATABASE_ENGINE=django.db.backends.sqlite3
DATABASE_NAME=db.sqlite3

# Email Settings
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=lostandfound.vpmrzshah@gmail.com
EMAIL_HOST_PASSWORD=olcn hlep cryq bvag

# Base URL
BASE_URL=http://127.0.0.1:8000
EOL
    print_success ".env file created"
else
    print_warning ".env file already exists"
fi

# Run migrations
print_info "Running database migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput
print_success "Database migrations completed"

# Create superuser (optional)
print_info "Creating superuser account..."
echo ""
read -p "Do you want to create a superuser account? (y/n): " create_superuser
if [ "$create_superuser" = "y" ] || [ "$create_superuser" = "Y" ]; then
    python manage.py createsuperuser
fi

# Collect static files
print_info "Collecting static files..."
python manage.py collectstatic --noinput --clear
print_success "Static files collected"

# Display summary
echo ""
echo "========================================"
echo -e "${GREEN}🎉 Setup Complete!${NC}"
echo "========================================"
echo ""
print_success "Virtual environment: activated"
print_success "Dependencies: installed"
print_success "Database: migrated"
print_success "Static files: collected"
echo ""
echo -e "${BLUE}📝 Next Steps:${NC}"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Run development server: python manage.py runserver"
echo "3. Open browser: http://localhost:8000/"
echo ""
echo -e "${BLUE}📚 Admin Panel:${NC}"
echo "URL: http://localhost:8000/admin/"
echo ""
echo -e "${YELLOW}⚠️  Note:${NC}"
echo "- Edit .env file to configure email settings"
echo "- For production, set DEBUG=False in .env"
echo "- Update ALLOWED_HOSTS in .env for production"
echo ""
print_success "Happy coding! 🚀"
