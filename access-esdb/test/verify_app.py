# Note these are not unit tests

import pytest
import requests

base_url = 'http://localhost:8082'

users = [
    {"username": "alice", "password": "alice1", "roles": {"reader", "writer", "admin"}},
    # {"username": "james", "password": "james1", "roles": {"reader"}},
    # {"username": "kelly", "password": "kelly1", "roles": {"execute"}}
]

movie_id = {'movies': [
    {'id': 'Mi-r1ocB6ekKXXTmvC2y', 'name': 'PS1'},
    {'id': 'My-r1ocB6ekKXXTmvC2y', 'name': 'Avegers'},
    {'id': 'NC-r1ocB6ekKXXTmvC2y', 'name': 'K3g'},
    {'id': 'NS-r1ocB6ekKXXTmvC2y', 'name': 'Bahubali'},
    {'id': 'Ni-r1ocB6ekKXXTmvC2y', 'name': 'Panjabhi Film'},
    {'id': '27Hc1ocBPOV2BA64Vm1o', 'name': None},
    {'id': '3LHd1ocBPOV2BA64lG32', 'name': None}
]}


def test_hello_world():
    for user in users:
        print('')
        response = requests.get(f'{base_url}/hello_world', auth=(user["username"], user["password"]))
        print("User: ", user)

        if response.status_code == 200:
            print('200-ok')
        else:
            print(f'200-nook-{response.status_code}')


def test_list_movies():
    for user in users:
        data = {
            "user": user["username"],
            "collection": "movie-summary",
        }

        response = requests.get(f'{base_url}/list_movies',
                                json=data,
                                auth=(user["username"], user["password"]))

        if response.status_code == 200:
            print(response.json())
        else:
            print(f'200-nook-{response.status_code}')
            print(response.json())


def test_movie_detail():

    for user in users:
        data = {
            "user": user["username"],
            "collection": "movie-summary",
        }
        response = requests.get(f'{base_url}/movie_detail/Mi-r1ocB6ekKXXTmvC2y',
                                json=data,
                                auth=(user["username"], user["password"]))

        if response.status_code == 200:
            print(response.json())
        else:
            print(f'200-nook-{response.status_code}')
            print(response.json())


def test_movie_update():
    for user in users:
        movie_id = '27Hc1ocBPOV2BA64Vm1o'
        end_point = 'movie_update'
        update_data = {
            "user": user["username"],
            "collection": "movie-summary",
            "Name": "RandomName",
            "Rating": 9
        }

        response = requests.put(f'{base_url}/{end_point}/{movie_id}',
                                json=update_data,
                                auth=(user["username"], user["password"]))

        if response.status_code == 200:
            print(response.json())
        else:
            print(f'200-nook-{response.status_code}')
            print(response.json())


def test_movie_delete():
    movie_id = '3LHd1ocBPOV2BA64lG32'
    end_point = 'delete_movie'

    for user in users:
        data = {
            "user": user["username"],
            "collection": "movie-summary",
        }
        response = requests.delete(f'{base_url}/{end_point}/{movie_id}',
                                   json=data,
                                   auth=(user["username"], user["password"]))

        if response.status_code == 200:
            print(response.json())
        else:
            print(f'200-nook-{response.status_code}')
            print(response.json())


queries = [
    "Rating:>5",
    'Language:"English"',
    'Country:"India" AND Rating:>7',
    'URL:"www.tiktok.com"',
    'Name:"Film"',
    '*:*'

]
def test_search_es_all():
    for query in queries:
        for user in users:
            end_point = 'search_es'
            api_url = f'{base_url}/{end_point}'
            data = {
                "user": user["username"],
                "collection": "movie-summary",
                "query": query
            }
            auth = (user["username"],
                    user["password"]
                    )
            print('')
            print(f'{user}-{query}')
            response = requests.post(api_url,
                                     json=data,
                                     auth=auth
                                     )
            if response.status_code == 200:
                print(response.json())
            else:
                print(f'200-nook-{response.status_code}')
                print(response.json())


def test_search_es_specific_field():
    for user in users:
        end_point = 'search_es'
        data = {
            "user": user["username"],
            "password": user["password"],
            "collection": "movie-summary",
            "query": 'Language:"Hindi"'
        }
        response = requests.post(f'{base_url}/{end_point}',
                                 json=data,
                                 auth=(user["username"], user["password"]))

        if response.status_code == 200:
            print(response.json())
        else:
            print(f'200-nook-{response.status_code}')
            print(response.json())


if __name__ == '__main__':
    test_list_movies()
    # Call other test functions here
