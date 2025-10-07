"""
SQLite to MongoDB Data Migration Script
Migrates Found Items from Django SQLite to MongoDB Atlas
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, '/workspaces/dear-project-1')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lxfpro.settings')
django.setup()

from found_app.models import FoundItem as SQLiteFoundItem
from lxfpro.mongo_models import MongoFoundItem
from lxfpro.mongodb import test_connection
from datetime import datetime


def migrate_found_items():
    """Migrate found items from SQLite to MongoDB"""
    
    print("\n" + "="*70)
    print("🚀 MIGRATING DATA: SQLite → MongoDB Atlas")
    print("="*70 + "\n")
    
    # Test MongoDB connection
    print("1️⃣  Testing MongoDB connection...")
    if not test_connection():
        print("❌ Migration aborted: MongoDB connection failed")
        return False
    
    print("\n2️⃣  Fetching items from SQLite...")
    try:
        sqlite_items = SQLiteFoundItem.objects.all()
        total_items = sqlite_items.count()
        print(f"✅ Found {total_items} items in SQLite database")
    except Exception as e:
        print(f"❌ Error fetching SQLite data: {e}")
        return False
    
    if total_items == 0:
        print("ℹ️  No items to migrate")
        return True
    
    print(f"\n3️⃣  Migrating {total_items} items to MongoDB...")
    
    migrated = 0
    failed = 0
    
    for item in sqlite_items:
        try:
            # Convert date to datetime if needed
            date_found = item.date_found
            if not isinstance(date_found, datetime):
                date_found = datetime.combine(date_found, datetime.min.time())
            
            # Get image path
            image_path = item.image.url if item.image else None
            
            # Create in MongoDB
            mongo_item = MongoFoundItem.create(
                user_id=item.user.id,
                item_name=item.item_name,
                description=item.description,
                category=item.category,
                date_found=date_found,
                location=item.location,
                image_path=image_path
            )
            
            if mongo_item:
                migrated += 1
                print(f"  ✓ Migrated: {item.item_name} (ID: {item.id} → {mongo_item['_id']})")
            else:
                failed += 1
                print(f"  ✗ Failed: {item.item_name} (ID: {item.id})")
                
        except Exception as e:
            failed += 1
            print(f"  ✗ Error migrating item {item.id}: {e}")
    
    print("\n" + "="*70)
    print("📊 MIGRATION SUMMARY")
    print("="*70)
    print(f"  Total Items:     {total_items}")
    print(f"  ✅ Migrated:     {migrated}")
    print(f"  ❌ Failed:       {failed}")
    print(f"  Success Rate:    {(migrated/total_items*100):.1f}%")
    print("="*70 + "\n")
    
    return failed == 0


def verify_migration():
    """Verify migrated data in MongoDB"""
    
    print("\n" + "="*70)
    print("🔍 VERIFYING MIGRATION")
    print("="*70 + "\n")
    
    # Get counts
    sqlite_count = SQLiteFoundItem.objects.count()
    mongo_items = MongoFoundItem.get_all(limit=1000)
    mongo_count = len(mongo_items)
    
    print(f"SQLite Database:  {sqlite_count} items")
    print(f"MongoDB Database: {mongo_count} items")
    
    if sqlite_count == mongo_count:
        print("\n✅ VERIFICATION PASSED: Counts match!")
        
        # Show sample items
        if mongo_count > 0:
            print("\n📝 Sample Migrated Items:")
            for item in mongo_items[:5]:
                print(f"  • {item['item_name']} - {item['category']} ({item['location']})")
        
        return True
    else:
        print(f"\n⚠️  WARNING: Count mismatch! ({sqlite_count} vs {mongo_count})")
        return False


def show_mongodb_stats():
    """Show MongoDB database statistics"""
    
    print("\n" + "="*70)
    print("📈 MONGODB DATABASE STATISTICS")
    print("="*70 + "\n")
    
    from lxfpro.mongodb import MongoDB
    
    try:
        db = MongoDB.get_database()
        stats = db.command('dbStats')
        
        print(f"Database Name:    {stats['db']}")
        print(f"Collections:      {stats['collections']}")
        print(f"Documents:        {stats['objects']}")
        print(f"Data Size:        {stats['dataSize'] / 1024:.2f} KB")
        print(f"Storage Size:     {stats['storageSize'] / 1024:.2f} KB")
        print(f"Indexes:          {stats['indexes']}")
        
        # List collections
        collections = db.list_collection_names()
        if collections:
            print(f"\n📁 Collections:")
            for coll in collections:
                count = db[coll].count_documents({})
                print(f"  • {coll}: {count} documents")
        
        print("\n" + "="*70)
        
    except Exception as e:
        print(f"❌ Error getting stats: {e}")


if __name__ == '__main__':
    print("\n" + "🔄 "*35)
    print("       SQLite → MongoDB Migration Tool")
    print("🔄 "*35 + "\n")
    
    # Run migration
    success = migrate_found_items()
    
    if success:
        # Verify migration
        verify_migration()
        
        # Show stats
        show_mongodb_stats()
        
        print("\n✅ MIGRATION COMPLETED SUCCESSFULLY! 🎉\n")
    else:
        print("\n❌ MIGRATION FAILED! Please check errors above.\n")
