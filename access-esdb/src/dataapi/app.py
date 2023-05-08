from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_httpauth import HTTPBasicAuth
from elasticsearch import Elasticsearch
import requests
import json
import logging

from common.configurelog import configure_logging
from src.common import config


def create_app(config, testing=False):
    app = Flask(__name__)
    app.config.from_object(config)  # Import configuration properties from config.py

    configure_logging(app)

    # Set the TESTING configuration key if testing is True
    if testing:
        app.config['TESTING'] = True

    global opa_server_url, elastic_url
    opa_server_url = app.config['OPA_SERVER_URL']

    es_host = app.config['ELASTICSEARCH_HOST']
    es_port = app.config['ELASTICSEARCH_PORT']
    elastic_url = f"{es_host}:{es_port}"

    api = Api(app)
    api.add_resource(HelloWorld, '/hello_world')
    api.add_resource(ListMovies, '/list_movies')
    api.add_resource(MovieDetail, '/movie_detail/<string:movie_id>')
    api.add_resource(MovieUpdate, '/movie_update/<string:movie_id>')
    api.add_resource(DeleteMovie, '/delete_movie/<string:movie_id>')
    api.add_resource(ElasticsearchQuery, '/search_es')
    return app, auth


# Define the verify function
def verify(username, password):
    payload = json.dumps({
        "input": {
            "username": username,
            "password": password
        }
    })

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(opa_server_url + "/verify_password", headers=headers, data=payload)

    if response.status_code == 200 and 'result' in response.json():
        app.logger.info(f'{username} Authorized')
        return response.json()['result']
    app.logger.warning(f'{username} NotAuthorized')
    return None


# Add this line to create an authentication object
auth = HTTPBasicAuth()
# Set the verify function as the password verification function for the HTTPBasicAuth object
auth.verify_password(verify)


class MovieAccess(Resource):

    @staticmethod
    def get_token(user, method, path):
        if not isinstance(path, list):
            path = [path]

        payload = json.dumps({
            "input": {
                "user": user,
                "method": method,
                "path": path
            }
        })

        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(opa_server_url + "/get_token", headers=headers, data=payload)
        if response.status_code == 200:
            token = response.json().get('result')[0]
            if token is None:
                app.logger.warning(f'Received None token for {user}-{method}-{path}')
            return token
        else:
            app.logger.warning(f'Received {response.status_code} for {user}-{method}-{path}')
            return response

    @staticmethod
    def get_es_client(token):
        es = Elasticsearch(elastic_url, api_key=(token))
        return es

    @staticmethod
    def get_collection(request):
        data = request.get_json()
        collection = data.get("collection")
        return collection

    @staticmethod
    def get_query(request):
        data = request.get_json()
        query = data.get("query")
        return query


class HelloWorld(MovieAccess):
    @auth.login_required
    def get(self):
        app.logger.info("Hello World")
        return "Hello World"


class ListMovies(MovieAccess):
    @auth.login_required
    def get(self):
        user = auth.username()
        method = request.method
        collection = self.get_collection(request)
        path = collection

        token = self.get_token(user, method, path)

        if token:
            return self.get_movies(token, collection)
        else:
            print(user, method, path)
            return {"message": "Unauthorized"}, 401

    def get_movies(self, token, collection):
        es = self.get_es_client(token)

        movies = es.search(index=collection).body.get('hits').get('hits')
        # Extract 'id and 'Name' field for each movie
        movie_names_and_ids = [{"id": movie.get('_id'),
                                "name": movie.get('_source').get('Name')} for movie in movies]

        # Return the list of movie names as the response
        return jsonify({"movies": movie_names_and_ids})


class MovieDetail(MovieAccess):
    @auth.login_required
    def get(self, movie_id):
        user = auth.username()
        method = request.method
        collection = self.get_collection(request)
        path = collection
        token = self.get_token(user, method, path)
        if token:
            es = self.get_es_client(token)
            result = es.get(index=collection, id=movie_id).get('_source')
            return jsonify(result)
        else:
            return {"message": "Unauthorized"}, 401


class MovieUpdate(MovieAccess):
    @auth.login_required
    def put(self, movie_id):
        user = auth.username()
        method = request.method
        collection = self.get_collection(request)
        path = collection

        token = self.get_token(user, method, path)
        if token:
            es = self.get_es_client(token)
            doc = request.get_json()
            es.update(index=collection, id=movie_id, doc=doc)
            return {"message": "Document Updated"}, 200
        else:
            return {"message": "Unauthorized"}, 401


class DeleteMovie(MovieAccess):
    @auth.login_required
    def delete(self, movie_id):
        user = auth.username()
        method = request.method
        collection = self.get_collection(request)
        path = collection
        token = self.get_token(user, method, path)
        if token:
            es = self.get_es_client(token)
            _is_exist = es.exists(index=collection, id=movie_id)
            if _is_exist:
                result = es.delete(index=collection, id=movie_id)
                return jsonify(result)
            return {"message": "Document does not exist"}, 404
        else:
            return {"message": "Unauthorized"}, 401


class ElasticsearchQuery(MovieAccess):
    @auth.login_required
    def post(self):
        user = auth.username()
        method = request.method
        collection = self.get_collection(request)
        path = [collection]
        query = self.get_query(request)

        if not all([user, collection, query]):
            return {"message": "All fields are required"}, 400
        token = self.get_token(user, method, path)

        if token:
            # Perform the Elasticsearch query
            results, start_idx, next_idx, total = self.search_es(token, collection, query)

            return {
                "results": results,
                "startIdx": start_idx,
                "nextIdx": next_idx,
                "totals": total
            }
        else:
            return {"message": "Unauthorized"}, 401

    def search_es(self, token, collection, query, start_idx=0, page_size=10):
        es = self.get_es_client(token)
        search_result = es.search(
            index=collection,
            body={
                "query": {
                    "query_string": {
                        "query": query
                    }
                },
                "from": start_idx,
                "size": page_size
            }
        )

        results = [hit["_source"] for hit in search_result["hits"]["hits"]]
        total = search_result["hits"]["total"]["value"]
        next_idx = start_idx + page_size if start_idx + page_size < total else -1

        return results, start_idx, next_idx, total


if __name__ == '__main__':
    app, auth = create_app(config)
    app.run(debug=True, host='localhost', port=8082)
