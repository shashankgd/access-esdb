# import pytest
# from src.access.app import create_app
# from test.config import TestConfig
# from base64 import b64encode
#
#
# def test_list_movies(mocker):
#     # Mock the Elasticsearch response
#     es_response_mock = mocker.patch("elasticsearch.Elasticsearch.search")
#     es_response_mock.return_value = {
#         "hits": {
#             "hits": [{"_source": {"Name": "PS1"}}, {"_source": {"Name": "Avegers"}}],
#             "total": {"value": 2},
#         }
#     }
#
#     # Mock the OPA response
#     opa_response_mock = mocker.patch("requests.post")
#     opa_response_mock.return_value.status_code = 200
#     opa_response_mock.return_value.json.return_value = {"result": "test_token"}
#
#     app, auth = create_app(config='config.TestConfig')
#     client = app.test_client()
#
#     # Set up authentication
#     username = "alice"
#     password = "alice1"
#     auth_string = f"{username}:{password}"
#     auth = b64encode(auth_string.encode("utf-8")).decode("utf-8")
#
#     data = {
#         "user": username,
#         "collection": "movie-summary",
#     }
#
#     response = client.get('/list_movies',
#                           json=data,
#                           auth=(username, password))
#
#     assert response.status_code == 200
#     assert response.get_json() == {
#         "results": [{"Name": "PS1"}, {"Name": "Avegers"}],
#         "startIdx": 0,
#         "nextIdx": 2,
#         "totals": 2,
#     }
#
#     # Assert that the mocks were called
#     opa_response_mock.assert_called_once()
#     es_response_mock.assert_called_once()
