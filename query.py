from elasticsearch import Elasticsearch

def querypart(index, field, query_text, size=10):
    es = Elasticsearch("http://172.27.27.118:9200")

    if field in ["year", "paper_id"]:
        # 对于数字类型（year and paper_id）使用 term 查询
        query_body = {
            "size": size,
            "query": {
                "term": {
                    field: query_text
                }
            }
        }
    else:
        # 对于其他类型（如文本类型）使用 match 查询
        query_body = {
            "size": size,
            "query": {
                "match": {
                    field: {
                        "query": query_text,
                        "fuzziness": "AUTO"
                    }
                }
            }
        }

    response = es.search(index=index, body=query_body)

    results = []
    for hit in response['hits']['hits']:
        doc_id = hit['_id']
        score = hit['_score']
        source = hit['_source']
        title = source.get('title', 'N/A')
        authors = source.get('authors', [])
        keywords = source.get('keywords', [])
        year = source.get('year', [])
        venue = source.get('venue', 'N/A')
        results.append([doc_id, score, title, year, authors, keywords, venue])

    return results


def queryAll(index, query_text, size=10):
    es = Elasticsearch("http://172.27.27.118:9200")

    query = {
        "query": {
            "multi_match": {
                "query": query_text,
                "fields": ["*"],
                "fuzziness": "AUTO"
            }
        },
        "size": size
    }

    response = es.search(index="icees", body=query)

    results = []
    for hit in response['hits']['hits']:
        doc_id = hit['_id']
        score = hit['_score']
        source = hit['_source']
        title = source.get('title', 'N/A')
        authors = source.get('authors', [])
        keywords = source.get('keywords', [])
        year = source.get('year', [])
        venue = source.get('venue', 'N/A')
        results.append([doc_id, score, title, year, authors, keywords, venue])

    return results

if __name__ == "__main__":
    print("Type which field you want to query, 0 for all, 1 for paper_id, 2 for title, 3 for year, 4 for authors, 5 for keywords, 6 for venue")
    fieldint = int(input())
    if(fieldint == 0):field = "all"
    elif(fieldint == 1): field = "paper_id"
    elif(fieldint == 2): field = "title"
    elif(fieldint == 3): field = "year"
    elif(fieldint == 4): field = "authors"
    elif(fieldint == 5): field = "keywords"
    elif(fieldint == 6): field = "venue"
    else: print("wrong input")    

    print("Type the word or sentence you want to query")
    word = input()
    print("Type the size of the result you want to show (default 10)")
    x = input()
    try:
        size = int(x)
    except ValueError:
        size = 10

    if field == "all":
        result = queryAll(index="icees", query_text=word, size=size)
    else:
        result = querypart(index="icees", field=field, query_text=word, size=size)
    
    if(result == []): print("no result")
    if(field == "all"):
        for i in range(len(result)):
          print(f"paper_id: {result[i][0]}\n Score: {result[i][1]}\n Title: {result[i][2]}\n Year: {result[i][3]}\n Authors: {result[i][4]}\n keywords: {result[i][5]}\n Venue: {result[i][6]}")
          print()
    elif(field == "paper_id"):
        for i in range(len(result)):
          print(f"paper_id: {result[i][0]} \n Score: {result[i][1]}\n")
    else:        
        for i in range(len(result)):
          print(f"paper_id: {result[i][0]} \n Score: {result[i][1]}\n {field}: {result[i][fieldint]}\n")