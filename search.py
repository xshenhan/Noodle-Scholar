from sanic import Blueprint
from sanic.response import json, text
from query import PaperSearch
import motor
from bson.objectid import ObjectId

search = Blueprint("search", url_prefix="/api/v1/search")


@search.get("/")
async def searcher(request):
    query_field = request.args.get("field") if request.args.get("field") is not None else "all"
    query_type = request.args.get("type") if request.args.get("type") is not None else "match"
    is_arxiv = request.args.get("arxiv") if request.args.get("arxiv") is not None else "false"
    print(is_arxiv)
    print(type(is_arxiv))
    searcher = PaperSearch() if is_arxiv == "false" else PaperSearch("arxiv")
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
    if is_arxiv == "false":
        collection = client.papers["100pdfs"]
    else:
        collection = client.papers["arxiv"]
    i = 0
    print(type(search_results))
    for k, paper in search_results.items():
        if is_arxiv == "false":
            document = await collection.find_one({"_id": ObjectId(k)})
        else:
            document = await collection.find_one({"id": k})
        tmp_results = {}
        tmp_results["_id"] = str(document["_id"])
        tmp_results["title"] = document["title"] if "title" not in paper else paper["title"]
        tmp_results["abstract"] = document["abstract"] if "abstract" not in paper else paper["abstract"]
        if is_arxiv == "false":
            tmp_results["author"] = document["author"] if "author" not in paper else paper["author"]        
            tmp_results["tag"] = document["tag"] if "tags" not in paper else paper["tags"]
        else:
            print("here")
            tmp_results["author"] = document["authors"] if "authors" not in paper else paper["authors"]
            tmp_results["tag"] = document["categories"] if "tags" not in paper else paper["tags"]
        results[i] = tmp_results
        i += 1     
    return json(results, headers={"Access-Control-Allow-Origin": "*"})
