from dotenv import load_dotenv # type: ignore
import os 

load_dotenv()  # Load .env values into environment variables

class Env:
    def __init__(self):
        self.mongodb_url = os.getenv('MONGODB_URL', 'mongodb://localhost:27017/auth_db')
        self.redis_host = os.getenv('REDIS_HOST', 'localhost')
        self.redis_port = int(os.getenv('REDIS_PORT', '6379'))
        self.redis_db = int(os.getenv('REDIS_DB', '0'))
        self.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')
        self.debug = os.getenv('DEBUG', 'False').lower() == 'true'
        self.access_token_expire_minutes = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '30'))
        self.algorithm = os.getenv('ALGORITHM', 'HS256')

ENV = Env()