import motor


def get_collection(source):
    client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://172.27.88.132:27017/?replicaSet=rs_noodle')
    if source == "100pdfs":
        return client.papers["100pdfs"]
    elif source == "arxiv":
        return client.arxiv["arxiv_new"]
    elif source == "arxiv_year":
        return client.arxiv["num_papers_year"]
    else:
        raise Exception("source not imply")