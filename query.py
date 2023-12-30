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
    # year_range_results = paper_search.search_by_year_range('2020', '2022', 10)
    # print(year_range_results)
    # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    # search_all_fields_results = paper_search.search_all_fields('a mildly ', 'all', 10, query_type='match')
    # print(search_all_fields_results)

    # match_results_with_year = paper_search._search('cnn', '', 10, 'match', '2002', '2015')
    # print(match_results_with_year)
    # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    # # 使用前缀查询
    # prefix_results = paper_search.search_specific_field('roc', 'title', 10, query_type='prefix')
    # print(prefix_results)
    # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    # # 使用通配符查询
    wildcard_results = paper_search.search_specific_field('rocks in the Mojave Desert, California', 'title', 10)
    print(wildcard_results)
    for key, value in wildcard_results.items():
        print(key, value)
    # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    # # 使用正则表达式查询
    # regexp_results = paper_search.search_specific_field('roc.*', 'title', 10, query_type='regexp')
    # print(regexp_results)