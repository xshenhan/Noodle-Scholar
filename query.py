from elasticsearch import Elasticsearch

# query: 要搜索的查询词
# field: 要搜索的特定字段
# param query_type: 查询类型（'match', 'prefix', 'wildcard', 'regexp'）
# return: 匹配结果的字典

class PaperSearch:
    def __init__(self, index_name='papers'):
        host = "http://172.27.88.132:9200"
        self.es = Elasticsearch(hosts=host)
        self.index_name = index_name

    def _search(self, query, field=None, size=20, query_type='match', start_year=None, end_year=None):
        if query_type == 'prefix':
            match_part = {"prefix": {field: query}}
        elif query_type == 'wildcard':
            match_part = {"wildcard": {field: query}}
        elif query_type == 'regexp':
            match_part = {"regexp": {field: query}}
        else:
            if field:
                match_part = {"match": {field: {"query": query, "fuzziness": "AUTO"}}}
            else:
                match_part = {"multi_match": {"query": query, "fields": ["*"], "fuzziness": "AUTO"}}
        
       
        must_clauses = [match_part]
        if start_year and end_year:
            range_clause = {
                "range": {
                    "date": {
                        "gte": f"{start_year}-01-01",
                        "lte": f"{end_year}-12-31",
                        "format": "yyyy-MM-dd"
                    }
                }
            }
            must_clauses.append(range_clause)

        body = {
            "query": {
                "bool": {
                    "must": must_clauses
                }
            },
            "highlight": {
                "fields": {
                    "*": {}
                },
                "pre_tags": ["<strong>"],
                "post_tags": ["</strong>"]
            },
            "_source": True,
            "size": size
        }

        response = self.es.search(index=self.index_name, body=body)

        results = {}
        for hit in response['hits']['hits']:
            id = hit['_source'].get('hash_id')
            highlights = hit.get('highlight', {})
            results[id] = highlights

        return results
    
    def search_by_year_range(self, start_year, end_year, size=20):
        body = {
            "query": {
                "range": {
                    "date": {
                        "gte": f"{start_year}-01-01",
                        "lte": f"{end_year}-12-31",
                        "format": "yyyy-MM-dd"
                    }
                }
            },
            "size": size
        }

        response = self.es.search(index=self.index_name, body=body)

        results = {}
        for hit in response['hits']['hits']:
            id = hit['_source'].get('hash_id')
            results[id] = id

        return results


    def search_all_fields(self, query, field, size, query_type='match', start_year=None, end_year=None):
        return self._search(query, None, size=size, query_type=query_type, start_year=start_year, end_year=end_year)

    def search_specific_field(self, query, field, size, query_type='match', start_year=None, end_year=None):
        return self._search(query, field, size=size, query_type=query_type, start_year=start_year, end_year=end_year)

# 使用示例
if __name__ == "__main__":
    paper_search = PaperSearch("papers")

    # 在所有字段上进行模糊搜索
    fuzzy_search_results = paper_search.search_all_fields('rock', None, 10, query_type='match')
    print("Fuzzy Search Results in All Fields:", fuzzy_search_results)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    # 在标题字段上进行模糊搜索
    fuzzy_title_search_results = paper_search.search_specific_field('rock', 'title', 10, query_type='match')
    print("Fuzzy Search Results in Title Field:", fuzzy_title_search_results)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    # 前缀搜索
    prefix_search_results = paper_search.search_specific_field('rock', 'title', 10, query_type='prefix')
    print("Prefix Search Results in Title Field:", prefix_search_results)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    # 通配符搜索
    wildcard_search_results = paper_search.search_specific_field('rock*', 'title', 10, query_type='wildcard')
    print("Wildcard Search Results in Title Field:", wildcard_search_results)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    # 正则表达式搜索
    regexp_search_results = paper_search.search_specific_field('rock.*', 'title', 10, query_type='regexp')
    print("Regular Expression Search Results in Title Field:", regexp_search_results)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
