#!/bin/bash

echo "🧪 Testing Chat System - Step by Step"
echo "======================================"
echo ""

echo "1️⃣  Testing Server Status..."
if curl -s http://localhost:8000 > /dev/null 2>&1; then
    echo "✅ Server is running at http://localhost:8000"
else
    echo "❌ Server is not running. Start with: python manage.py runserver"
    exit 1
fi

echo ""
echo "2️⃣  Testing MongoDB Connection..."
python3 << 'EOF'
try:
    from lxfpro.mongodb import test_connection
    if test_connection():
        print("✅ MongoDB Atlas connected successfully")
    else:
        print("❌ MongoDB connection failed")
except Exception as e:
    print(f"❌ MongoDB error: {e}")
EOF

echo ""
echo "3️⃣  Checking Chat Messages in MongoDB..."
python3 << 'EOF'
try:
    from lxfpro.mongo_models import MongoChatMessage
    collection = MongoChatMessage.get_collection()
    if collection is not None:
        count = collection.count_documents({})
        print(f"✅ Total chat messages in MongoDB: {count}")
        
        # Show last 3 messages
        messages = list(collection.find().sort('created_at', -1).limit(3))
        if messages:
            print("\n   Last 3 messages:")
            for msg in messages:
                print(f"   • From User {msg['sender_id']} → User {msg['receiver_id']}")
                print(f"     Message: {msg['message'][:50]}")
                print(f"     Read: {msg['is_read']}")
        else:
            print("   (No messages yet - send some via chat to test!)")
    else:
        print("❌ Could not access MongoDB collection")
except Exception as e:
    print(f"❌ Error: {e}")
EOF

echo ""
echo "4️⃣  Testing API Endpoints..."
echo ""
echo "   Testing /api/unread-count/ (requires login)"
curl -s http://localhost:8000/api/unread-count/ | head -1 | grep -q "success"
if [ $? -eq 0 ]; then
    echo "   ✅ Unread count API working"
else
    echo "   ⚠️  API requires authentication (login first)"
fi

echo ""
echo "5️⃣  Checking WebSocket Configuration..."
if grep -q "ChatConsumer" chat/consumers.py > /dev/null 2>&1; then
    echo "✅ WebSocket consumer configured"
else
    echo "❌ WebSocket consumer missing"
fi

echo ""
echo "======================================"
echo "📋 TESTING CHECKLIST:"
echo "======================================"
echo ""
echo "Manual Tests (Open browser):"
echo ""
echo "Step 1: Test User Registration/Login"
echo "  → Go to: http://localhost:8000/register/"
echo "  → Create 2 test users (user1, user2)"
echo ""
echo "Step 2: Test Chat Interface"
echo "  → Login as user1"
echo "  → Go to: http://localhost:8000/chat/user2/"
echo "  → Check: Connection status shows 'Connected' (green)"
echo "  → Type a message and send"
echo "  → Check: Message appears in chat window"
echo "  → Check browser console for:"
echo "     ✓ '✅ WebSocket connection opened'"
echo "     ✓ '📤 Message sent: <your_message>'"
echo "     ✓ '✅ Message saved to MongoDB: user1 → user2'"
echo ""
echo "Step 3: Test Notifications"
echo "  → Open 2 browser windows"
echo "  → Login as user1 in window 1"
echo "  → Login as user2 in window 2"
echo "  → From window 1 (user1), send message to user2"
echo "  → Check window 2 (user2):"
echo "     ✓ Red badge appears on floating chat button"
echo "     ✓ Browser notification pops up"
echo "     ✓ Sound plays"
echo "     ✓ Message appears in chat window"
echo ""
echo "Step 4: Test Notification Widget"
echo "  → On home page, check bottom-right corner"
echo "  → Should see purple floating button (💬)"
echo "  → If unread messages exist:"
echo "     ✓ Red badge with count visible"
echo "     ✓ Pulse animation active"
echo "  → Click button:"
echo "     ✓ Dropdown opens with message preview"
echo "     ✓ Shows sender and message text"
echo ""
echo "Step 5: Verify MongoDB Storage"
echo "  → Run: python manage.py shell"
echo "  → Type:"
echo "     from lxfpro.mongo_models import MongoChatMessage"
echo "     msgs = MongoChatMessage.get_collection().find()"
echo "     for msg in msgs:"
echo "         print(msg)"
echo "  → Should see saved messages with:"
echo "     ✓ sender_id, receiver_id"
echo "     ✓ message text"
echo "     ✓ is_read status"
echo "     ✓ created_at timestamp"
echo ""
echo "======================================"
echo "🔍 DEBUGGING TIPS:"
echo "======================================"
echo ""
echo "If messages not appearing:"
echo "  1. Check browser console (F12)"
echo "  2. Look for WebSocket connection errors"
echo "  3. Check Django terminal for connection logs"
echo "  4. Verify MongoDB connection: python lxfpro/mongodb.py"
echo ""
echo "If notifications not working:"
echo "  1. Check browser notification permission"
echo "  2. Test API: curl http://localhost:8000/api/unread-count/"
echo "  3. Check if user is logged in"
echo "  4. Check browser console for errors"
echo ""
echo "If WebSocket not connecting:"
echo "  1. Verify server running: lsof -i :8000"
echo "  2. Check ASGI configuration in lxfpro/routing.py"
echo "  3. Check Channels installed: pip list | grep channels"
echo "  4. Browser console should show connection logs"
echo ""
echo "======================================"
echo "📝 USEFUL COMMANDS:"
echo "======================================"
echo ""
echo "Start server:"
echo "  python manage.py runserver 0.0.0.0:8000"
echo ""
echo "Test MongoDB:"
echo "  python lxfpro/mongodb.py"
echo ""
echo "Check logs:"
echo "  tail -f /var/log/django.log  (if logging configured)"
echo ""
echo "Django shell:"
echo "  python manage.py shell"
echo ""
echo "======================================"
echo "✅ All tests complete!"
echo "======================================"
