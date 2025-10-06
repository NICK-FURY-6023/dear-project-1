#!/bin/bash

# Quick Demo Script - Lost & Found Portal
# Run this to see the project in action!

echo "========================================"
echo "   Lost & Found Portal - Quick Demo"
echo "========================================"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}📝 Project Files:${NC}"
echo ""
ls -lh *.md *.sh *.bat 2>/dev/null | awk '{print "   ", $9, "("$5")"}'
echo ""

echo -e "${BLUE}📦 Python Packages Installed:${NC}"
echo ""
pip list | grep -E "Django|channels|Pillow" | awk '{print "   ✅", $1, $2}'
echo ""

echo -e "${BLUE}📂 Directory Structure:${NC}"
echo ""
tree -L 2 -I 'venv|__pycache__|*.pyc|node_modules' . 2>/dev/null || ls -la
echo ""

echo -e "${BLUE}🗄️  Database Tables:${NC}"
echo ""
python manage.py showmigrations 2>/dev/null | head -15
echo ""

echo -e "${BLUE}🌐 Available URLs:${NC}"
echo ""
echo "   ✅ Homepage:     http://localhost:8000/"
echo "   ✅ Login:        http://localhost:8000/login/"
echo "   ✅ Register:     http://localhost:8000/register/"
echo "   ✅ Admin Panel:  http://localhost:8000/admin/"
echo "   ✅ Report Item:  http://localhost:8000/report-found/"
echo "   ✅ View Items:   http://localhost:8000/view-found/"
echo "   ✅ My Items:     http://localhost:8000/my-found-items/"
echo ""

echo -e "${BLUE}🚀 To Run the Server:${NC}"
echo ""
echo "   1. Activate venv:   source venv/bin/activate"
echo "   2. Run server:      python manage.py runserver"
echo "   3. Open browser:    http://localhost:8000/"
echo ""

echo -e "${GREEN}✅ Project is ready to run!${NC}"
echo ""
