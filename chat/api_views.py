"""
Chat API Views for Notifications and Message Status
"""
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from lxfpro.mongo_models import MongoChatMessage
from chat.models import Thread


@login_required
def get_unread_count(request):
    """Get unread message count for current user"""
    try:
        user_id = request.user.id
        
        # Get unread messages from MongoDB
        collection = MongoChatMessage.get_collection()
        if collection is not None:
            unread_count = collection.count_documents({
                'receiver_id': user_id,
                'is_read': False
            })
        else:
            unread_count = 0
        
        return JsonResponse({
            'success': True,
            'unread_count': unread_count
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
def mark_thread_as_read(request, thread_id):
    """Mark all messages in a thread as read"""
    try:
        user_id = request.user.id
        
        # Update MongoDB messages
        success = MongoChatMessage.mark_as_read(thread_id, user_id)
        
        return JsonResponse({
            'success': success,
            'message': 'Messages marked as read'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
def get_recent_conversations(request):
    """Get recent conversations for user"""
    try:
        user_id = request.user.id
        
        # Get from MongoDB
        conversations = MongoChatMessage.get_user_conversations(user_id)
        
        return JsonResponse({
            'success': True,
            'conversations': conversations
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
def check_new_messages(request):
    """Check if there are new messages (for polling)"""
    try:
        user_id = request.user.id
        last_check = request.GET.get('last_check')  # timestamp
        
        collection = MongoChatMessage.get_collection()
        if collection is not None:
            # Count new messages since last check
            query = {
                'receiver_id': user_id,
                'is_read': False
            }
            
            if last_check:
                from datetime import datetime
                from bson import ObjectId
                query['created_at'] = {'$gt': datetime.fromisoformat(last_check)}
            
            new_count = collection.count_documents(query)
            
            # Get sender info
            if new_count > 0:
                messages = list(collection.find(query).limit(5).sort('created_at', -1))
                senders = [{'sender_id': msg['sender_id'], 'preview': msg['message'][:50]} for msg in messages]
            else:
                senders = []
            
            return JsonResponse({
                'success': True,
                'has_new': new_count > 0,
                'new_count': new_count,
                'senders': senders
            })
        else:
            return JsonResponse({
                'success': True,
                'has_new': False,
                'new_count': 0
            })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
