from elasticsearch import Elasticsearch
from pymongo import MongoClient
client = MongoClient("mongodb://172.27.88.132:27017")
db = client["arxiv"]
collection = db["arxiv_new"]
documents = collection.find()

print("connected to mongodb")
host = "http://172.27.88.132:9200"
es = Elasticsearch(hosts=host)

print(es.ping())

index_name = "arxiv_new"  # 替换为您希望使用的索引名称

if  es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)


mapping = {
    "mappings":{
        "properties": {
            "paper_id": {"type": "keyword"},
            "hash_id": {"type": "keyword"}, 
            "tag": {"type": "keyword"},
            "date": {"type": "date"},
            "authors" :{"type": "text"},
            "ref_paper": {"type": "text"},
            "conference": {"type": "text"},
            "keywords": {"type": "text"},
            "categories": {"type": "text"},
            "year": {"type": "integer"},
            # "author": {
            #     "properties": {
            #         "affiliation": {"type": "text"},
            #         "name": {"type": "text"}
            #     }
            # },
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
}

es.indices.create(index=index_name,body=mapping)
# es.indices.put_mapping(index=index_name, body=mapping, doc_type=)

for document in documents:
    hash_id = str(document["_id"])  # Convert ObjectId to string
    document["hash_id"] = hash_id  # Add 'hash_id' field to the document
    document.pop("_id")  # Remove the original '_id' field

    # Index the document in Elasticsearch
    es.index(index=index_name, doc_type='_doc', body=document)
print("indexed")




       