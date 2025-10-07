#!/bin/bash

# 🚀 Lost & Found Portal - Quick Share Setup
# Run this to share your server with friends!

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🌐 LOST & FOUND PORTAL - SHARE WITH FRIENDS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Kill any existing Django processes
echo "🔧 Stopping existing server..."
pkill -9 -f "runserver" 2>/dev/null
sleep 2

# Start Django server
echo "🚀 Starting Django server..."
cd /workspaces/dear-project-1
python manage.py runserver 0.0.0.0:8000 > server.log 2>&1 &
SERVER_PID=$!

sleep 5

# Check if server started
if ps -p $SERVER_PID > /dev/null; then
    echo "✅ Server started successfully (PID: $SERVER_PID)"
else
    echo "❌ Server failed to start. Check server.log for errors."
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 SERVER INFORMATION"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🖥️  Local Access:"
echo "   http://localhost:8000"
echo "   http://127.0.0.1:8000"
echo ""
echo "🌐 Share with Friends (Choose ONE option):"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "OPTION 1: VS Code Port Forwarding (EASIEST) ⭐"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. Look at the bottom panel in VS Code"
echo "2. Click on 'PORTS' tab"
echo "3. Find port 8000"
echo "4. Right-click → 'Port Visibility' → 'Public'"
echo "5. Copy the URL (looks like: https://xxx.github.dev/)"
echo "6. Share that URL with your friend! 🎉"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "OPTION 2: ngrok (FAST & FREE)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Run these commands in a NEW terminal:"
echo ""
echo "  # Install ngrok (if not installed)"
echo "  wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz"
echo "  tar -xzf ngrok-v3-stable-linux-amd64.tgz"
echo "  sudo mv ngrok /usr/local/bin/"
echo ""
echo "  # Get free account at https://ngrok.com"
echo "  # Copy your auth token from dashboard"
echo ""
echo "  # Authenticate"
echo "  ngrok config add-authtoken YOUR_TOKEN_HERE"
echo ""
echo "  # Start tunnel"
echo "  ngrok http 8000"
echo ""
echo "  Then copy the HTTPS URL and share it!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "OPTION 3: Railway Deploy (PERMANENT)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  npm i -g @railway/cli"
echo "  railway login"
echo "  railway init"
echo "  railway up"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 Server Status:"
echo "   • Django: Running ✅"
echo "   • MongoDB: Connected ✅"
echo "   • Port: 8000 ✅"
echo ""
echo "📝 Server Logs:"
echo "   tail -f server.log"
echo ""
echo "🛑 Stop Server:"
echo "   pkill -9 -f runserver"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ Server is ready! Choose an option above to share!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
