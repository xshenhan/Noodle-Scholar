import motor
from config import MONGODB_CONNECTION_STRING

def get_collection(source):
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_CONNECTION_STRING)
    if source == "100pdfs":
        return client.papers["100pdfs"]
    elif source == "arxiv":
        return client.arxiv["arxiv_new"]
    elif source == "arxiv_year":
        return client.arxiv["num_papers_year"]
    else:
        raise Exception("source not imply")