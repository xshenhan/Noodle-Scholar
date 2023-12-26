from sanic import Blueprint
from sanic.response import text
import sanic
from sanic import Sanic, response
from sanic_session import Session
from sanic.response import text, redirect, json, ResponseStream, file_stream, file, html
import motor
import motor.motor_asyncio
from bson.objectid import ObjectId
from sanic_cors import CORS
from auth import protected, add_user_info_cookie
from query import PaperSearch
from mycrypt import encrypt, decrypt, DATABASE_KEY
from os.path import isfile, join
import requests
from utils import get_collection

paper = Blueprint('paper', url_prefix='/api/v1/paper')


@paper.get("/test")
async def paper_test(request):
    client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://172.27.88.132:27017/?replicaSet=rs_noodle')
    source = request.args.get("source", "arxiv")
    # id = ObjectId("6532290bd507ea15ca185e83")
    id = ObjectId("6569d43b2c9d068894c84b8f")
    document  = await get_collection(source).find_one({"_id": id})
    return json({"status": "ok"}, headers={"Access-Control-Allow-Origin": "*"})

@paper.get("/info")
async def get_paper_info(request):
    # """This is used to get the detailed information of a paper.
    # openapi:
    # ---
    # parameters:
    #   - name: id
    #     in: query
    #     description: The id of the paper.
    #     required: true
    #     schema:
    #       type: str[6 char]
    # responses:
    #     - '200':
    #         type: json
    # """
    id = request.args.get("id")
    if id == None:
        return text("must query with an id", status=416, headers={"Access-Control-Allow-Origin": "*"})
    source = request.args.get("source", "100pdfs")
    collection = get_collection(source)
    if collection == None:
        return text("The collection doesn't exists!", status=416, headers={"Access-Control-Allow-Origin": "*"})
    document = await collection.find_one({"_id": ObjectId( id)})
    
    if document == None:
        return text("The paper doesn't exists!, the paper id you asked is {}".format(id), status=416, headers={"Access-Control-Allow-Origin": "*"})    
    # with open("/home/hxs/main/debug/01.txt", "wt") as t:
    #     t.write(request.args.get("id"))
    if source == "arxiv":
        author = document["author"] if "author" in document else document["authors"]
        affiliation = None
        author_all = None
    else:
        author = document["author"]["name"]
        affiliation = document["author"]["affiliation"]
        author_all = {key: value for key, value in zip(author, affiliation)}
    ans = {
        "id" : id,
        "title" : document["title"],
        "abstract": document["abstract"],
        "doc_type": None,
        "year": document["year"] if source == "100pdfs" else None,
        "volume": document["volume"] if source == "100pdfs" else None,
        "cite": None,
        "kqi": None,
        "tag": document["tag"] if source == "100pdfs" else document["categories"],
        "doi" : document["doi"] if "doi" in document else None, 
        "author": author,
        "affiliation": affiliation,
        "author_all": author_all,
        "url": "https://arxiv.org/abs/" + document["id"] if source == "arxiv" else None,
        "keywords": document["keywords"] if source == "100pdfs" else None,
    }
    return json(ans, headers={"Access-Control-Allow-Origin": "*"})

@paper.get("/download")
@protected
async def download(request):
    token = request.args.get("tk")
    # if token != "u*DD@7eHbs3zE2A#":
    #     return text("no permission")
    id = request.args.get("id")
    if id == None:
        return text("must query with an id", status=416, headers={"Access-Control-Allow-Origin": "*"})    
    source = request.args.get("source", "100pdfs")
    collection = get_collection(source)
    document = await collection.find_one({"_id": ObjectId(id)})
    print(source)
    if source == "100pdfs":
        if document == None:
            return text("The paper doesn't exists!, the paper id you asked is {}".format(id), status=416
                        , headers={"Access-Control-Allow-Origin": "*"})
        path = document["pdf_address"]
        
        # return text("not imply")
        return await file_stream(path, filename=document["title"] + ".pdf", 
                                headers={"Access-Control-Allow-Origin": "*"})
    elif source == "arxiv":
        if document == None:
            return text("The paper doesn't exists!, the paper id you asked is {}".format(id), status=416
                        , headers={"Access-Control-Allow-Origin": "*"})
        arxiv_pdf = "https://arxiv.org/pdf/" + document["id"] + ".pdf"
        return redirect(arxiv_pdf, headers={"Access-Control-Allow-Origin": "*"})
    else:
        return text("not imply", status=416, headers={"Access-Control-Allow-Origin": "*"})
@paper.get("/tables/img")
async def tables_img(requests):
    id = requests.args.get("id")
    if id == None:
        return text("must query with an id", status=416, headers={"Access-Control-Allow-Origin": "*"})
    source = requests.args.get("source", "100pdfs")
    collection = get_collection(source)
    document = await collection.find_one({"_id": ObjectId(id)})
    if document == None:
        return text("The paper doesn't exists!, the paper id you asked is {}".format(id), status=416
                    , headers={"Access-Control-Allow-Origin": "*"})
    table_num = len(document["table_rendition_address"])
    res = {}
    url = "/api/v1/paper/table/img"
    for i in range(table_num):
        res[i] = url + f"?id={id}&index={i}"
    return json(res, headers={"Access-Control-Allow-Origin": "*"})

@paper.get("/tables")
async def tables(requests):
    id = requests.args.get("id")
    if id == None:
        return text("must query with an id", status=416, headers={"Access-Control-Allow-Origin": "*"})
    source = requests.args.get("source", "100pdfs")
    collection = get_collection(source)
    document = await collection.find_one({"_id": ObjectId(id)})
    if document == None:
        return text("The paper doesn't exists!, the paper id you asked is {}".format(id), status=416
                    , headers={"Access-Control-Allow-Origin": "*"})
    table_num = len(document["csv_address"])
    res = {}
    url = "/api/v1/paper/table"
    for i in range(table_num):
        res[i] = url + f"?id={id}&index={i}"
    return json(res, headers={"Access-Control-Allow-Origin": "*"})

@paper.get("/table/img")
async def table_img(requests):
    id = requests.args.get("id")
    index = requests.args.get("index")
    index = int(index)
    index = 0 if index == None else index
    if id == None:
        return text("must query with an id", status=416, headers={"Access-Control-Allow-Origin": "*"})
    source = requests.args.get("source", "100pdfs")
    collection = get_collection(source)
    document = await collection.find_one({"_id": ObjectId(id)})
    if document == None:
        return text("The paper doesn't exists!, the paper id you asked is {}".format(id), status=416
                    , headers={"Access-Control-Allow-Origin": "*"})
    if index >= len(document["table_rendition_address"]):
        return text("The index is too large!", status=416, headers={"Access-Control-Allow-Origin": "*"})
    return await file(document["table_rendition_address"][index], mime_type="image/png", headers={"Access-Control-Allow-Origin": "*"})


@paper.get("/table")
async def table(requests):
    id = requests.args.get("id")
    index = requests.args.get("index")
    index = int(index)
    index = 0 if index == None else index
    if id == None:
        return text("must query with an id", status=416, headers={"Access-Control-Allow-Origin": "*"})
    source = requests.args.get("source", "100pdfs")
    collection = get_collection(source)
    document = await collection.find_one({"_id": ObjectId(id)})
    if document == None:
        return text("The paper doesn't exists!, the paper id you asked is {}".format(id), status=416
                    , headers={"Access-Control-Allow-Origin": "*"})
    if index >= len(document["csv_address"]):
        return text("The index is too large!", status=416, headers={"Access-Control-Allow-Origin": "*"})
    path = "/home/share/files/100_PDF_csv/" + document["paper_id"] + "/" + str(index) + ".csv"
    path = document["csv_address"][index]
    return await file_stream(path, mime_type="text/csv", headers={"Access-Control-Allow-Origin": "*"})
 

@paper.get("/pics")
async def pics(requests):
    id = requests.args.get("id")
    if id == None:
        return text("must query with an id", status=416, headers={"Access-Control-Allow-Origin": "*"})
    source = requests.args.get("source", "100pdfs")
    collection = get_collection(source)
    document = await collection.find_one({"_id": ObjectId(id)})
    if document == None:
        return text("The paper doesn't exists!, the paper id you asked is {}".format(id), status=416
                    , headers={"Access-Control-Allow-Origin": "*"})
    table_num = len(document["pics_address"])
    res = {}
    url = "/api/v1/paper/pic"
    for i in range(table_num):
        res[i] = url + f"?id={id}&index={i}"
    return json(res, headers={"Access-Control-Allow-Origin": "*"})

@paper.get("/pic")
async def pic(requests):
    id = requests.args.get("id")
    index = requests.args.get("index")
    index = int(index)
    index = 0 if index == None else index
    if id == None:
        return text("must query with an id", status=416, headers={"Access-Control-Allow-Origin": "*"})
    source = requests.args.get("source", "100pdfs")
    collection = get_collection(source)
    document = await collection.find_one({"_id": ObjectId(id)})
    if document == None:
        return text("The paper doesn't exists!, the paper id you asked is {}".format(id), status=416
                    , headers={"Access-Control-Allow-Origin": "*"})
    if index >= len(document["pics_address"]):
        return text("The index is too large!", status=416, headers={"Access-Control-Allow-Origin": "*"})
    return await file(document["pics_address"][index], mime_type="image/png", headers={"Access-Control-Allow-Origin": "*"})
