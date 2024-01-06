import sanic
from sanic import Blueprint, response
from sanic.response import json, text
import motor
import time
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorCollection
from bson.objectid import ObjectId
from utils import get_collection
from config import MONGODB_CONNECTION_STRING
async def get_documents_in_range(collection: AsyncIOMotorCollection, name: str, start: int, end: int):
    """
    Retrieves documents ranked from 'x' to 'y' (inclusive) based on the specified field 'name'.

    :param collection: The MongoDB collection to query.
    :param name: The field name to sort the documents by.
    :param x: The starting rank (inclusive).
    :param y: The ending rank (inclusive).
    :return: A list of documents.
    """
    if end <= start:
        raise ValueError("y must be greater than x")

    # Calculate the number of documents to skip and the limit
    skip_count = start - 1
    limit_count = end - start + 1

    # Build the query
    cursor = collection.find().sort(name, -1).skip(skip_count).limit(limit_count)

    # Fetch and return the documents
    documents = await cursor.to_list(length=limit_count)
    return documents


visualization = Blueprint("visualization", url_prefix="/api/v1/vis")

@visualization.get("/test")
async def vis_test(request):
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_CONNECTION_STRING)
    collection = client.papers["arxiv"]
    start_time = time.time()
    count = await collection.count_documents({"categories": "math.NT"})
    return json({"count": count}, headers={"Access-Control-Allow-Origin": "*"})


@visualization.get("/author/papers")
async def vis_author_papers(request):
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_CONNECTION_STRING)
    collection = client.arxiv["num_papers_authors"]
    name = "num_papers"
    start = int(request.args.get("start", 0))
    end = int(request.args.get("end", 10))
    cursor = collection.find().sort(name, -1).skip(start).limit(end - start + 1)
    result = {}
    for index, document in enumerate(await cursor.to_list(length=end - start + 1)):
        tmp_result = {}
        tmp_result["author"] = document["author"]
        tmp_result["num_papers"] = document["num_papers"]
        result[start + index] = tmp_result
    return json(result, headers={"Access-Control-Allow-Origin": "*"})

@visualization.get("/subject/papers")
async def vis_subjects_papers(request):
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_CONNECTION_STRING)
    collection = client.arxiv["num_papers_main_subject"]
    name = "num_papers"
    start = int(request.args.get("start", 0))
    end = int(request.args.get("end", 10))
    cursor = collection.find().sort(name, -1).skip(start).limit(end - start + 1)
    result = {}
    for index, document in enumerate(await cursor.to_list(length=end - start + 1)):
        tmp_result = {}
        tmp_result["main_subject"] = document["main_subject"]
        tmp_result["num_papers"] = document["num_papers"]
        result[start + index] = tmp_result
    return json(result, headers={"Access-Control-Allow-Origin": "*"})


@visualization.get("/subsubject/papers")
async def vis_subsubjects_papers(request):
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_CONNECTION_STRING)
    collection = client.arxiv["num_papers_sub_subject"]
    name = "num_papers"
    start = int(request.args.get("start", 0))
    end = int(request.args.get("end", 10))
    cursor = collection.find().sort(name, -1).skip(start).limit(end - start + 1)
    result = {}
    for index, document in enumerate(await cursor.to_list(length=end - start + 1)):
        tmp_result = {}
        tmp_result["sub_subject"] = document["sub_subject"]
        tmp_result["num_papers"] = document["num_papers"]
        result[index + start] = tmp_result
    return json(result, headers={"Access-Control-Allow-Origin": "*"})


@visualization.route('/paper/year', methods=['GET'])
async def count_by_year(request):
    source = request.args.get("source", "arxiv")
    collection = get_collection("arxiv_year")
    start_year = int(request.args.get("start_year", 1990))
    end_year = int(request.args.get("end_year", 2020))
    cursor = collection.find({
        "year": {
            "$gte": start_year,
            "$lte": end_year
        }
    })
    results = {}
    lit = await cursor.to_list(length=20)
    for index, document in enumerate(lit):
        results[document["year"]] = document["num_papers"]
    return json(results, headers={"Access-Control-Allow-Origin": "*"})


