from motor.motor_asyncio import AsyncIOMotorClient
from app.config.env import ENV
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class MongoDB:
    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.database = None
        self.mongodb_url = ENV.mongodb_url
    
    async def connect(self):
        try:
            self.client = AsyncIOMotorClient(self.mongodb_url)
            # Extract database name from URL or use default
            if '?' in self.mongodb_url:
                db_name = "auth_db"  # Default for cloud connections
            else:
                db_name = self.mongodb_url.split('/')[-1] if '/' in self.mongodb_url else "auth_db"
            
            self.database = self.client[db_name]
            
            # Test the connection
            await self.client.admin.command('ping')
            logger.info(f"Connected to MongoDB: {db_name}")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
    
    async def disconnect(self):
        if self.client:
            self.client.close()
            logger.info("Disconnected from MongoDB")
    
    def get_database(self):
        if self.database is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self.database
    
    @property
    def users(self):
        return self.get_database().users

# Create a global instance
db = MongoDB()

def get_database():
    return db.get_database()