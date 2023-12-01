import sanic
from sanic import Sanic, response
from sanic_session import Session
from sanic.response import text, redirect, json, ResponseStream, file_stream, file, html
import motor
import motor.motor_asyncio
from bson.objectid import ObjectId
from sanic_cors import CORS
from auth import protected, add_user_info_cookie
from login import login
from query import PaperSearch
from mycrypt import encrypt, decrypt, DATABASE_KEY
from os.path import isfile, join

app = Sanic("ns")
Session(app)
origins = [
    "*"
]

app.config["CORS_RESOURCES"] = {r"/*": {"origins": origins}}
CORS(app)

app.static('/assets', './dist/assets')

@app.get("/")
async def root(request):
    # '''the root page will be redirect to test page(we will change in future)'''
    return await file("./dist/index.html")
    
@app.get("/test")
async def test(request):
    # ''' just to test that the api server is working
    # ''' 
    return text("Hello world!", headers={"Access-Control-Allow-Origin": "*"})

@app.get("/api/v1/paper/info")
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
    if len(id) != 24:
        return text("id is illegal.", status=416, headers={"Access-Control-Allow-Origin": "*"})
    # client = motor.motor_asyncio.AsyncIOMotorClient('10.80.135.195', 27017)
    client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://172.27.88.132:27017/?replicaSet=rs_noodle')
    collection = client.papers["100pdfs"]
    if collection == None:
        return text("The collection doesn't exists!", status=416, headers={"Access-Control-Allow-Origin": "*"})
    document = await collection.find_one({"_id": ObjectId( id)})
    
    if document == None:
        return text("The paper doesn't exists!, the paper id you asked is {}".format(id), status=416, headers={"Access-Control-Allow-Origin": "*"})    
    # with open("/home/hxs/main/debug/01.txt", "wt") as t:
    #     t.write(request.args.get("id"))
    ans = {
        "id" : id,
        "title" : document["title"],
        "abstract": document["abstract"],
        "doc_type": None,
        "year": document["year"],
        "volume": document["volume"],
        "cite": None,
        "kqi": None,
    }
    return json(ans, headers={"Access-Control-Allow-Origin": "*"})

@app.get("/api/v1/paper/download")
async def download(request):
    token = request.args.get("tk")
    # if token != "u*DD@7eHbs3zE2A#":
    #     return text("no permission")
    id = request.args.get("id")
    if id == None:
        return text("must query with an id", status=416, headers={"Access-Control-Allow-Origin": "*"})
    if len(id) != 24:
        return text("id is illegal.", status=416, headers={"Access-Control-Allow-Origin": "*"})
    client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://172.27.88.132:27017/?replicaSet=rs_noodle')
    collection = client.papers["100pdfs"]
    document = await collection.find_one({"_id": ObjectId(id)})
    # bucket = motor.motor_asyncio.AsyncIOMotorGridFSBucket(client.papers, "fs")
    # grid_out = await bucket.open_download_stream_by_name(document["paper_id"] + ".pdf")
    # print(document["paper_id"] + ".pdf")
    if document == None:
        return text("The paper doesn't exists!, the paper id you asked is {}".format(id), status=416
                    , headers={"Access-Control-Allow-Origin": "*"})
    path = document["pdf_address"]
    
    # return text("not imply")
    return await file_stream(path, filename=document["title"] + ".pdf", 
                             headers={"Access-Control-Allow-Origin": "*"})

@app.get("/api/v1/paper/tables")
async def tables(requests):
    id = requests.args.get("id")
    if id == None:
        return text("must query with an id", status=416, headers={"Access-Control-Allow-Origin": "*"})
    if len(id) != 24:
        return text("id is illegal.", status=416, headers={"Access-Control-Allow-Origin": "*"})
    client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://172.27.88.132:27017/?replicaSet=rs_noodle')
    collection = client.papers["100pdfs"]
    document = await collection.find_one({"_id": ObjectId(id)})
    if document == None:
        return text("The paper doesn't exists!, the paper id you asked is {}".format(id), status=416
                    , headers={"Access-Control-Allow-Origin": "*"})
    table_num = len(document["table_rendition_address"])
    res = {}
    url = "/api/v1/paper/_table"
    for i in range(table_num):
        res[i] = url + f"?id={id}&index={i}"
    return json(res, headers={"Access-Control-Allow-Origin": "*"})

@app.get("/api/v1/paper/_table")
async def _table(requests):
    id = requests.args.get("id")
    index = requests.args.get("index")
    index = int(index)
    index = 0 if index == None else index
    if id == None:
        return text("must query with an id", status=416, headers={"Access-Control-Allow-Origin": "*"})
    if len(id) != 24:
        return text("id is illegal.", status=416, headers={"Access-Control-Allow-Origin": "*"})
    client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://172.27.88.132:27017/?replicaSet=rs_noodle')
    collection = client.papers["100pdfs"]
    document = await collection.find_one({"_id": ObjectId(id)})
    if document == None:
        return text("The paper doesn't exists!, the paper id you asked is {}".format(id), status=416
                    , headers={"Access-Control-Allow-Origin": "*"})
    if index >= len(document["table_rendition_address"]):
        return text("The index is too large!", status=416, headers={"Access-Control-Allow-Origin": "*"})
    return await file(document["table_rendition_address"][index], mime_type="image/png", headers={"Access-Control-Allow-Origin": "*"})
    # return text(document["table_rendition_address"][index])

@app.get("/api/v1/paper/pics")
async def pics(requests):
    id = requests.args.get("id")
    if id == None:
        return text("must query with an id", status=416, headers={"Access-Control-Allow-Origin": "*"})
    if len(id) != 24:
        return text("id is illegal.", status=416, headers={"Access-Control-Allow-Origin": "*"})
    client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://172.27.88.132:27017/?replicaSet=rs_noodle')
    collection = client.papers["100pdfs"]
    document = await collection.find_one({"_id": ObjectId(id)})
    if document == None:
        return text("The paper doesn't exists!, the paper id you asked is {}".format(id), status=416
                    , headers={"Access-Control-Allow-Origin": "*"})
    table_num = len(document["pics_address"])
    res = {}
    url = "/api/v1/paper/_pic"
    for i in range(table_num):
        res[i] = url + f"?id={id}&index={i}"
    return json(res, headers={"Access-Control-Allow-Origin": "*"})

@app.get("/api/v1/paper/_pic")
async def _pic(requests):
    id = requests.args.get("id")
    index = requests.args.get("index")
    index = int(index)
    index = 0 if index == None else index
    if id == None:
        return text("must query with an id", status=416, headers={"Access-Control-Allow-Origin": "*"})
    if len(id) != 24:
        return text("id is illegal.", status=416, headers={"Access-Control-Allow-Origin": "*"})
    client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://172.27.88.132:27017/?replicaSet=rs_noodle')
    collection = client.papers["100pdfs"]
    document = await collection.find_one({"_id": ObjectId(id)})
    if document == None:
        return text("The paper doesn't exists!, the paper id you asked is {}".format(id), status=416
                    , headers={"Access-Control-Allow-Origin": "*"})
    if index >= len(document["pics_address"]):
        return text("The index is too large!", status=416, headers={"Access-Control-Allow-Origin": "*"})
    return await file(document["pics_address"][index], mime_type="image/png", headers={"Access-Control-Allow-Origin": "*"})

# @app.get("/api/v1/paper/lists")
# async def get_lists(requests):
    
@app.get("/api/v1/search")
async def search(request):
    query_field = request.args.get("field") if request.args.get("field") is not None else "all"
    query_type = request.args.get("type") if request.args.get("type") is not None else "match"
    searcher = PaperSearch()
    search_fn = searcher.search_all_fields if query_field == "all" else searcher.search_specific_field
    if query_field not in ["all", "tag","ref_paper","conference","keywords","author","link","abstract","title","volume","journal","issn","publisher","doi"]:
        return text("not imply", status=416, headers={"Access-Control-Allow-Origin": "*"})
    query_size = int(request.args.get("size")) if request.args.get("size") is not None else 20
    # if request.query == None:
    #     return text("must request with a query", status=416, headers={"Access-Control-Allow-Origin": "*"})
    search_results = search_fn(request.args.get("query"), query_field, query_size, query_type=query_type)
    # print(query_size)
    results = {}
    client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://172.27.88.132:27017/?replicaSet=rs_noodle')
    collection = client.papers["100pdfs"]
    i = 0
    print(type(search_results))
    for k, paper in search_results.items():
        document = await collection.find_one({"paper_id": k})
        tmp_results = {}
        tmp_results["_id"] = str(document["_id"])
        tmp_results["title"] = document["title"] if "title" not in paper else paper["title"]
        tmp_results["abstract"] = document["abstract"] if "abstract" not in paper else paper["abstract"]
        tmp_results["author"] = document["author"] if "author" not in paper else paper["author"]
        tmp_results["tag"] = document["tag"] if "tags" not in paper else paper["tags"]
        results[i] = tmp_results
        i += 1
    return json(results, headers={"Access-Control-Allow-Origin": "*"})

@app.get("/secret")
@protected
async def secert(request):
    return text("secret")
    

@app.get("/api/v1/signup")
@add_user_info_cookie
async def signup(request):
    if request.args.get('username') is None:
        return text('You should provide a username', headers={"Access-Control-Allow-Origin": "*"})
    if request.args.get('password') is None:
        return text('You should provide a password', headers={"Access-Control-Allow-Origin": "*"})
    
    username = request.args.get('username')
    password = request.args.get('password')
    response = json({"username": username, "password": password}, headers={"Access-Control-Allow-Origin": "*"})
    
    client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://172.27.88.132:27017/?replicaSet=rs_noodle')
    users = client['users']
    users_collection = users['users']
    
    if await users_collection.find_one({'username': request.args.get('username')}) is not None:
        return text("The user has been signed up!", status=200, headers={"Access-Control-Allow-Origin": "*"})
    
    group = "user" if request.args.get("group") is None else request.args.get("group")
    user = {"username": request.args.get('username'), "password": encrypt(request.args.get('password'), key=DATABASE_KEY), "group": group}
    await users_collection.insert_one(user)
    return response


# 处理前端路由
@app.route('/<path:path>')
async def catch_all(request, path):
    file_path = join('./dist', path)
    # 如果请求的是静态文件，则返回该文件
    if isfile(file_path):
        return await file(file_path)
    # 否则，返回 Vue 应用的 index.html，让 Vue Router 处理路由
    return await file('./dist/index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=11234, dev=True)
