import pymysql
import json
from elasticsearch import Elasticsearch

mysql_host = "server.acemap.cn"
mysql_port = 13306
mysql_user = "ieei"
mysql_password = "ieei_2021"
mysql_db = "ieei_web"
mysql_table = "paper"

es_host = "localhost"
es_port = 9200
es_index = "icees"


mysql_conn = pymysql.connect(host=mysql_host, port=mysql_port, user=mysql_user, password=mysql_password, db=mysql_db, charset="utf8")
cursor = mysql_conn.cursor()

#启动es
host = "http://172.27.27.118:9200"
es = Elasticsearch(hosts=host)


mappings_and_settings = {        
    "settings": {
        "analysis": {
            "filter": {
                "english_stop": {
                    "type": "stop",
                    "stopwords": "_english_"
                },
                "english_stemmer": {
                    "type": "stemmer",
                    "language": "english"
                },
                "english_possessive_stemmer": {
                    "type": "stemmer",
                    "language": "possessive_english"
                },
                "synonym_filter": {
                "type": "synonym",
                    "synonyms": [
                        "nlp, natural language processing",
                        "ai, artificial intelligence",
                        "ml, machine learning"
                    ]
                },
                "shingle_filter": {
                    "type": "shingle",
                    "min_shingle_size": 2,
                    "max_shingle_size": 3
                }
            },
            "analyzer": {
                "gh_analyzer": {
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "english_possessive_stemmer",
                        "english_stop",
                        "english_stemmer",
                        "asciifolding",
                        "synonym_filter",
                        "shingle_filter"
                    ]
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "paper_id": {
                "type": "keyword"
            },
            "title": {
                "type": "text",
                "analyzer": "gh_analyzer"
            },
            "authors": {
                "type": "text",
                "analyzer": "gh_analyzer"
            },
            "keywords": {
                "type": "text",
                "analyzer": "gh_analyzer"
            },
            "year": {
                "type": "long"
            },
            "venue": {
                "type": "text",
                "analyzer": "gh_analyzer"
            }
        }
    }
}


# 索引名称
index_name = "icees"

# 创建索引
if es.indices.exists(index_name):
    es.indices.delete(index=index_name)
es.indices.create(index=index_name, body=mappings_and_settings)


# 提取MySQL中的数据并导入Elasticsearch
cursor.execute(f"SELECT paper_id, title, year, authors, keywords, venue FROM {mysql_table}")
for row in cursor.fetchall():
    # 将作者和关键词的 JSON 字符串转换为逗号分隔的字符串
    authors_str = ', '.join(json.loads(row[3])) if row[3] else 'N/A'
    keywords_str = ', '.join(json.loads(row[4])) if row[4] else 'N/A'

    # 创建文档
    doc = {
        "paper_id": row[0],
        "title": row[1],
        "year": row[2],
        "authors": authors_str,
        "keywords": keywords_str,
        "venue": row[5]
    }

    # 将文档插入 Elasticsearch
    try:
        es.index(index=es_index, doc_type="_doc", id=row[0], body=doc)
    except Exception as e:
        print(f"Error processing record {row[0]}: {e}")

# 关闭数据库连接
mysql_conn.close()