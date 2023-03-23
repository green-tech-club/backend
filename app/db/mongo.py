import motor.motor_asyncio
from config import config


# client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])

db_user = config.db_username
db_password = config.db_password
db_cluster = config.db_cluster

MONGODB_URL=f"mongodb+srv://{db_user}:{db_password}@{db_cluster}vwuw.mongodb.net/?retryWrites=true&w=majority"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = client.college
