from elasticsearch import Elasticsearch
from pymongo import MongoClient

port = "9200"
host = "http://172.27.27.118:9200"

es = Elasticsearch(hosts=host)
index_name = "papers"  # 替换为您希望使用的索引名称

def search_documents(query, type, size):
    body = {
        "query": {
            "multi_match": {
                "query": query,
                # "tag","date","ref_paper","conference","keywords","year","author","last_page","link","abstract","title","volume","update_time","journal","issn","publisher","doi"
                # "fields": ["title", "abstract"],
                "fields": [type],
                "fuzziness": "AUTO"
            }
        },
        "size" : size
    }

    response = es.search(index=index_name, body=body)
    hits = response["hits"]["hits"]
    results = [hit["_source"]["paper_id"] for hit in hits]
    return results

if __name__ == "__main__":
    search_results = search_documents("rock", "title", 20)
    print(len(search_results))
    print(type(search_results))
    for result in search_results:
        print(result)
    print("searched")