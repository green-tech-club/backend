import motor.motor_asyncio
import os


# client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
MONGODB_URL="mongodb+srv://test:greentech@cluster0.114vwuw.mongodb.net/?retryWrites=true&w=majority"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = client.college
