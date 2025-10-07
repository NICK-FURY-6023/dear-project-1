"""
MongoDB Connection Service for Lost & Found Portal
Uses PyMongo directly for MongoDB Atlas connectivity
"""

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import certifi
import logging

logger = logging.getLogger(__name__)

# MongoDB Configuration
MONGODB_CONFIG = {
    'URI': 'mongodb+srv://juned_db_user:DatabaseGODhu123@cluster0.vlx619w.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0',
    'DATABASE': 'lostfound_production',
    'TIMEOUT': 5000,  # 5 seconds
}


class MongoDB:
    """MongoDB Connection Manager"""
    
    _client = None
    _db = None
    
    @classmethod
    def get_client(cls):
        """Get MongoDB client instance (singleton)"""
        if cls._client is None:
            try:
                cls._client = MongoClient(
                    MONGODB_CONFIG['URI'],
                    serverSelectionTimeoutMS=MONGODB_CONFIG['TIMEOUT'],
                    tlsCAFile=certifi.where(),
                    connect=True
                )
                # Test connection
                cls._client.admin.command('ping')
                logger.info("✅ MongoDB connection successful!")
            except (ConnectionFailure, ServerSelectionTimeoutError) as e:
                logger.error(f"❌ MongoDB connection failed: {e}")
                cls._client = None
                raise
        return cls._client
    
    @classmethod
    def get_database(cls):
        """Get database instance"""
        if cls._db is None:
            client = cls.get_client()
            if client is not None:
                cls._db = client[MONGODB_CONFIG['DATABASE']]
        return cls._db
    
    @classmethod
    def close_connection(cls):
        """Close MongoDB connection"""
        if cls._client:
            cls._client.close()
            cls._client = None
            cls._db = None
            logger.info("MongoDB connection closed")


# Convenience functions
def get_collection(collection_name):
    """Get a MongoDB collection"""
    try:
        db = MongoDB.get_database()
        return db[collection_name] if db is not None else None
    except Exception as e:
        logger.error(f"Error getting collection {collection_name}: {e}")
        return None


def test_connection():
    """Test MongoDB connection"""
    try:
        client = MongoDB.get_client()
        # Ping the server
        client.admin.command('ping')
        print("✅ MongoDB Atlas connection successful!")
        
        # Get database info
        db = MongoDB.get_database()
        collections = db.list_collection_names()
        print(f"✅ Database: {MONGODB_CONFIG['DATABASE']}")
        print(f"✅ Collections: {collections if collections else 'None (empty database)'}")
        
        return True
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return False


# Collections mapping
COLLECTIONS = {
    'users': 'auth_user',  # Will sync with Django User model
    'found_items': 'found_items',
    'messages': 'chat_messages',
    'sessions': 'django_sessions',
}


if __name__ == '__main__':
    # Test connection when run directly
    print("Testing MongoDB connection...")
    test_connection()
