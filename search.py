from sanic import Blueprint
from sanic.response import json, text
from query import PaperSearch
import motor
from bson.objectid import ObjectId
import re
search = Blueprint("search", url_prefix="/api/v1/search")
from utils import get_collection

@search.get("/")
async def searcher(request):
    query_field = request.args.get("field") if request.args.get("field") is not None else "all"
    if query_field == "author":
        query_field = "authors" 
    start_year = request.args.get("start_year", None)
    end_year = request.args.get("end_year", None)
    query_type = request.args.get("type") if request.args.get("type") is not None else "match"
    source = request.args.get("source") if request.args.get("source") is not None else "100pdfs"
    print(source)
    print(type(source))
    searcher = PaperSearch() if source == "100pdfs" else PaperSearch("arxiv_new" if source == "arxiv" else source)
    search_fn = searcher.search_all_fields if query_field == "all" else searcher.search_specific_field
    if query_field not in ["all", "tag", "authors","abstract","title","journal","doi"]:
        return text("not imply", status=416, headers={"Access-Control-Allow-Origin": "*"})
    if source == "arxiv":
        query_field = "categories" if query_field == "tag" else query_field
    elif source == "100pdfs":
        query_field = "keywords" if query_field == "tag" else query_field
    query_size = int(request.args.get("size")) if request.args.get("size") is not None else 100
    # if request.query == None:
    # if bool(re.search(r'[^a-zA-Z0-9]', request.args.get("query"))):
    #     return text("must request with a legal query", status=416, headers={"Access-Control-Allow-Origin": "*"})
    #     return text("must request with a query", status=416, headers={"Access-Control-Allow-Origin": "*"})
    search_results = search_fn(request.args.get("query"), query_field, query_size, query_type=query_type, start_year=start_year, end_year=end_year)
    # print(query_size)
    results = {}
    collection = get_collection(source)
    if collection == None:
        return text("source not imply", status=416, headers={"Access-Control-Allow-Origin": "*"})
    i = 0
    print(type(search_results))
    print(len(search_results))
    for k, paper in search_results.items():
        document = await collection.find_one({"_id": ObjectId(k)})
        if document == None:
            continue
        tmp_results = {}
        tmp_results["_id"] = str(document["_id"])
        tmp_results["title"] = document["title"] if "title" not in paper else paper["title"][0]
        tmp_results["abstract"] = [document["abstract"]] if "abstract" not in paper else paper["abstract"]
        tmp_results["doi"] = document["doi"] if "doi" not in paper else paper["doi"]
        tmp_results["author"] = document["author"]
        tmp_results["keywords"]= document["keywords"] if source == "100pdfs" else None
        if source == "100pdfs":
            tmp_results["tag"] = document["tag"] if "tags" not in paper else paper["tags"]
            table_num = len(document["pics_address"])
            pics = {}
            url = "/api/v1/paper/pic"
            tmp_results["pic_num"] = table_num
            for i in range(table_num):
                pics[i] = url + f"?id={k}&index={i}"
            tmp_results["pics"] = pics
        else:
            tmp_results["tag"] = document["categories"] if "tags" not in paper else paper["tags"]
            tmp_results["pics"] = {}
            tmp_results["pic_num"] = 0
        tmp_results["url"] = "https://arxiv.org/abs/" + document["id"] if source == "arxiv" else "https://doi.org/" + document["doi"],
        tmp_results["year"] = int(document["date"].split("-")[0]) if "year" not in paper else paper["year"]
        results[i] = tmp_results
        i += 1
    return json(results, headers={"Access-Control-Allow-Origin": "*"})


@search.route("/autocomplete", methods=["GET", "POST"])
async def autocomplete(request):
    if request.method == "GET":
        query_field = request.args.get("field") if request.args.get("field") is not None else "all"
        query_type = request.args.get("type") if request.args.get("type") is not None else "match"
        source = request.args.get("source") if request.args.get("source") is not None else "100pdfs"
        query = request.args.get("query")
    else:
        query_field = request.data.get("field") if request.data.get("field") is not None else "all"
        query_type = request.data.get("type") if request.data.get("type") is not None else "match"
        source = request.data.get("source") if request.data.get("source") is not None else "100pdfs"
        query = request.data.get("query")
    print(source)
    print(type(source))
    searcher = PaperSearch() if source == "100pdfs" else PaperSearch("arxiv")
    search_fn = searcher.search_all_fields if query_field == "all" else searcher.search_specific_field
    if query_field not in ["all", "tag","ref_paper","conference","keywords","author","link","abstract","title","volume","journal","issn","publisher","doi"]:
        return text("not imply", status=416, headers={"Access-Control-Allow-Origin": "*"})
    query_size = 7
    # if request.query == None:
    #     return text("must request with a query", status=416, headers={"Access-Control-Allow-Origin": "*"})
    search_results = search_fn(query, query_field, query_size, query_type=query_type)
    # print(query_size)
    results = []
    i = 0
    for k, paper in search_results.items():
        # tem_results["_id"] = k
        # for key, value in paper.items():
        #     tem_results[key] = value
        # results[i] = tem_results
        results.append(paper[query_field if query_field != "all" else "title"][0])
        i += 1
    return json(results, headers={"Access-Control-Allow-Origin": "*"})