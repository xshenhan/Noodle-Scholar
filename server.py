import sanic
from sanic import Sanic, response
from sanic.response import text, redirect, json, ResponseStream, file_stream, file
import motor
import motor.motor_asyncio
from bson.objectid import ObjectId
from sanic_cors import CORS
from auth import protected
from login import login
from query import search_documents
app = Sanic("ns")
app.config.SECRET = "GhFANncWqTJhFXKGP7r/NYzvmMMpHnNH$kFYQBpkmgZna]deCBFjMu6thbnpgrAZh3NZ"
app.blueprint(login)

origins = [
    "*"
]

app.config["CORS_RESOURCES"] = {r"/*": {"origins": origins}}
CORS(app)
@app.get("/")
async def root(request):
    # '''the root page will be redirect to test page(we will change in future)'''
    return redirect("/test")
    
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
    
@app.get("/search")
async def search(request):
    query_type = request.args.get("type") if request.args.get("type") is not None else "title"
    if query_type not in ["tag","ref_paper","conference","keywords","author","link","abstract","title","volume","journal","issn","publisher","doi"]:
        return text("not imply", status=416, headers={"Access-Control-Allow-Origin": "*"})
    query_size = int(request.args.get("size")) if request.args.get("size") is not None else 20
    # if request.query == None:
    #     return text("must request with a query", status=416, headers={"Access-Control-Allow-Origin": "*"})
    search_results = search_documents(request.args.get("query"), query_type, query_size)
    # print(query_size)
    results = {}
    client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://172.27.88.132:27017/?replicaSet=rs_noodle')
    collection = client.papers["100pdfs"]
    for i in search_results:
        document = await collection.find_one({"paper_id": i})
        results[i] = {
            "_id": str(document["_id"]),
            "title": document["title"],
        }
    return json(results, headers={"Access-Control-Allow-Origin": "*"})

@app.get("/secret")
@protected
async def secert(request):
    return text("secret")
    
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=11234, dev=True)
