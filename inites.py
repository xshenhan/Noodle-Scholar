from elasticsearch import Elasticsearch
from pymongo import MongoClient
client = MongoClient("mongodb://172.27.88.132:27017")
db = client["papers"]
collection = db["100pdfs"]
documents = collection.find()

print("connected to mongodb")
es = Elasticsearch()

index_name = "paper_test"  # 替换为您希望使用的索引名称

if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name)

mapping = {
    "properties": {
        "paper_id": {"type": "keyword"},
        "tag": {"type": "keyword"},
        "date": {"type": "date"},
        "ref_paper": {"type": "keyword"},
        "conference": {"type": "keyword"},
        "keywords": {"type": "keyword"},
        "year": {"type": "integer"},
        "author": {
            "properties": {
                "affiliation": {"type": "text"},
                "name": {"type": "text"}
            }
        },
        "last_page": {"type": "integer"},
        "link": {"type": "keyword"},
        "abstract": {"type": "text"},
        "title": {"type": "text"},
        "volume": {"type": "keyword"},
        "update_time": {"type": "date"},
        "journal": {"type": "text"},
        "issn": {"type": "keyword"},
        "first_page": {"type": "integer"},
        "publisher": {"type": "text"},
        "doi": {"type": "keyword"},
        "pdf_address": {"type": "keyword"},
        "pics_address": {"type": "keyword"},
        "csv_address": {"type": "keyword"},
        "table_rendition_address": {"type": "text"}
    
    }
}

es.indices.put_mapping(index=index_name, body=mapping)

for document in documents:
    document.pop("_id")  # 移除 _id 字段
    es.index(index=index_name, body=document)
print("indexed")




       