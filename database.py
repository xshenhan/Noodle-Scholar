import motor
import motor.motor_asyncio
from bson.objectid import ObjectId
import uvloop

client = motor.motor_asyncio.AsyncIOMotorClient('172.27.88.132', 27017)

collection = client.papers["100pdfs"]

# collection:motor.MotorCollection

async def test():
    res = await collection.find_one({"_id": ObjectId("6532290ad507ea15ca185e7f")})
uvloop.run(test())