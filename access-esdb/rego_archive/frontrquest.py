import json

import requests

# query = '''
# package authz
#
# allow
# '''
#
# input_data = {
#     "method": "GET",
#     "path": ["users", 1],
#     "user_id": 1
# }
#
# url = "http://localhost:8181/v1/query"
# headers = {"Content-Type": "application/json"}
# data = {"query": query, "input": input_data}
# response = requests.post(url, headers=headers, json=data)
#
# if response.status_code == 200:
#     result = json.loads(response.text)
#     if result["result"]:
#         print("Access granted")
#     else:
#         print("Access denied")
# else:
#     print(f"Failed to evaluate policy: {response.text}")

from elasticsearch import Elasticsearch

es = Elasticsearch("https://3a6e61faae4241a89a88ead8bc7aaf0a.asia-south1.gcp.elastic-cloud.com:443",
                   api_key=("MmJIYTFvY0JQT1YyQkE2NExXMlc6OVpObmdHbzlRcjZkbE81OTQ3YzhSUQ==")
                   )

# # a = es.get(index="movie-summary", Language="Mi-r1ocB6ekKXXTmvC2y")['_source']

query = {
    "query": {
        "bool": {
            "filter": [
                { "term": { "Country": "India" } }
            ]
        }
    }
}
#
a = es.search(index="movie-summary", body=query)
print(a)

# Define the search query with a range filter on the Date field
query = {
    "query": {
        "bool": {
            "must": [
                {
                    "match": {
                        "Language": "Hindi"
                    }
                }
            ],
            "filter": [
                {
                    "range": {
                        "Date": {
                            "gte": "2023-03-01",
                            "lte": "2023-04-30"
                        }
                    }
                }
            ]
        }
    }
}

# Execute the search query
response = es.search(index="movie-summary", body=query)

print(2)
print(response)

print(3)
es_index = "movie-summary"  # ratings

print(es.search(index=es_index))

print(4)
response =es.get(index=es_index, id="Mi-r1ocB6ekKXXTmvC2y")
print(response)
print(5)
movie_id = '27Hc1ocBPOV2BA64Vm1o'
end_point = 'movie_update'
update_data = {"Name": "RandomName1", "Language": "Gujrati1", "Rating": 1 }
print(es.get(index=es_index, id=movie_id))
result = es.update(index=es_index, id=movie_id, doc=update_data)
print(result)
print(es.get(index=es_index, id=movie_id))
print(6)
movie_id = '3LHd1ocBPOV2BA64lG32'
print(es.exists(index=es_index, id=movie_id))
print(es.delete(index=es_index, id=movie_id))

