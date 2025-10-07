"""
MongoDB Models - Hybrid Approach
Django ORM for User authentication (SQLite)
MongoDB for Found Items and Chat Messages
"""

from datetime import datetime
from lxfpro.mongodb import get_collection
from bson import ObjectId


class MongoFoundItem:
    """MongoDB Model for Found Items"""
    
    collection_name = 'found_items'
    
    @classmethod
    def get_collection(cls):
        return get_collection(cls.collection_name)
    
    @classmethod
    def create(cls, user_id, item_name, description, category, date_found, location, image_path=None):
        """Create a new found item"""
        collection = cls.get_collection()
        if collection is None:
            return None
        
        item = {
            'user_id': user_id,
            'item_name': item_name,
            'description': description,
            'category': category,
            'date_found': date_found,
            'location': location,
            'image_path': image_path,
            'status': 'unclaimed',
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
        }
        
        result = collection.insert_one(item)
        item['_id'] = result.inserted_id
        return item
    
    @classmethod
    def get_all(cls, limit=100):
        """Get all found items"""
        collection = cls.get_collection()
        if collection is None:
            return []
        
        items = list(collection.find().sort('created_at', -1).limit(limit))
        return items
    
    @classmethod
    def get_by_user(cls, user_id):
        """Get items by user ID"""
        collection = cls.get_collection()
        if collection is None:
            return []
        
        items = list(collection.find({'user_id': user_id}).sort('created_at', -1))
        return items
    
    @classmethod
    def get_by_id(cls, item_id):
        """Get item by ID"""
        collection = cls.get_collection()
        if collection is None:
            return None
        
        try:
            return collection.find_one({'_id': ObjectId(item_id)})
        except:
            return None
    
    @classmethod
    def update(cls, item_id, update_data):
        """Update an item"""
        collection = cls.get_collection()
        if collection is None:
            return False
        
        update_data['updated_at'] = datetime.utcnow()
        result = collection.update_one(
            {'_id': ObjectId(item_id)},
            {'$set': update_data}
        )
        return result.modified_count > 0
    
    @classmethod
    def delete(cls, item_id):
        """Delete an item"""
        collection = cls.get_collection()
        if collection is None:
            return False
        
        result = collection.delete_one({'_id': ObjectId(item_id)})
        return result.deleted_count > 0


class MongoChatMessage:
    """MongoDB Model for Chat Messages"""
    
    collection_name = 'chat_messages'
    
    @classmethod
    def get_collection(cls):
        return get_collection(cls.collection_name)
    
    @classmethod
    def create(cls, sender_id, receiver_id, message, thread_id=None):
        """Create a new chat message"""
        collection = cls.get_collection()
        if collection is None:
            return None
        
        msg = {
            'sender_id': sender_id,
            'receiver_id': receiver_id,
            'message': message,
            'thread_id': thread_id,
            'is_read': False,
            'created_at': datetime.utcnow(),
        }
        
        result = collection.insert_one(msg)
        msg['_id'] = result.inserted_id
        return msg
    
    @classmethod
    def get_thread_messages(cls, thread_id, limit=100):
        """Get messages for a thread"""
        collection = cls.get_collection()
        if collection is None:
            return []
        
        messages = list(
            collection.find({'thread_id': thread_id})
            .sort('created_at', 1)
            .limit(limit)
        )
        return messages
    
    @classmethod
    def get_user_conversations(cls, user_id):
        """Get all conversations for a user"""
        collection = cls.get_collection()
        if collection is None:
            return []
        
        # Get unique thread IDs where user is sender or receiver
        pipeline = [
            {
                '$match': {
                    '$or': [
                        {'sender_id': user_id},
                        {'receiver_id': user_id}
                    ]
                }
            },
            {
                '$group': {
                    '_id': '$thread_id',
                    'last_message': {'$last': '$message'},
                    'last_time': {'$last': '$created_at'}
                }
            },
            {'$sort': {'last_time': -1}}
        ]
        
        conversations = list(collection.aggregate(pipeline))
        return conversations
    
    @classmethod
    def mark_as_read(cls, thread_id, user_id):
        """Mark messages as read"""
        collection = cls.get_collection()
        if collection is None:
            return False
        
        result = collection.update_many(
            {
                'thread_id': thread_id,
                'receiver_id': user_id,
                'is_read': False
            },
            {'$set': {'is_read': True}}
        )
        return result.modified_count > 0


class MongoActivityLog:
    """MongoDB Model for Activity Logs"""
    
    collection_name = 'activity_logs'
    
    @classmethod
    def get_collection(cls):
        return get_collection(cls.collection_name)
    
    @classmethod
    def log(cls, user_id, action, details=None):
        """Log user activity"""
        collection = cls.get_collection()
        if collection is None:
            return None
        
        log_entry = {
            'user_id': user_id,
            'action': action,
            'details': details,
            'timestamp': datetime.utcnow(),
        }
        
        result = collection.insert_one(log_entry)
        return result.inserted_id
    
    @classmethod
    def get_user_logs(cls, user_id, limit=50):
        """Get logs for a user"""
        collection = cls.get_collection()
        if collection is None:
            return []
        
        logs = list(
            collection.find({'user_id': user_id})
            .sort('timestamp', -1)
            .limit(limit)
        )
        return logs
