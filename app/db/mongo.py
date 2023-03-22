import motor.motor_asyncio
from config import Config


# client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])

db_user = Config.db_username
db_password = Config.db_password
db_cluster = Config.db_cluster

MONGODB_URL=f"mongodb+srv://{db_user}:{db_password}@{db_cluster}vwuw.mongodb.net/?retryWrites=true&w=majority"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = client.college
