package auth

runtime := opa.runtime()
env := runtime["env"]


valid_users = [
    {"username": "alice", "password": "alice1", "roles": {"reader", "writer", "admin"}},
    {"username": "james", "password": "james1", "roles": {"reader"}},
    {"username": "kelly", "password": "kelly1", "roles": {"execute"}}
]

api_tokens = {
    "admin": {
        "ratings": {"token": "admin_ratings_token"},
        "movie-summary": {"token": {env.MOVIE_SUMMARY_ADMIN_TOKEN}}
    },
    "reader": {
        "ratings": {"token": "reader_ratings_token"},
        "movie-summary": {"token": {env.MOVIE_SUMMARY_READER_TOKEN}}
    },
    "writer": {
        "ratings": {"token": "writer_ratings_token"},
        "movie-summary": {"token": {env.MOVIE_SUMMARY_WRITER_TOKEN}}
    },
    "execute": {
        "ratings": {"token": "execute_ratings_token"},
        "movie-summary": {"token": {env.MOVIE_SUMMARY_EXECUTE_TOKEN}}
    }
}

allowed_methods = {
    "admin": {"GET", "PUT", "POST", "DELETE"},
    "reader": {"GET"},
    "writer": {"PUT", "POST"},
    "execute": {"GET"}
}

allowed_paths = {
    "admin": {"", "movie-summary"},
    "reader": {"movie-summary"},
    "writer": {"movie-summary"}
}


verify_password = true {
    username = input.username
    password = input.password
    some i
    valid_users[i].username == username
    valid_users[i].password == password
}

get_token = token {
    some i
    valid_users[i].username == input.user
    some role
    valid_users[i].roles[role]
    valid_method_and_path(role)
    token := api_tokens[role][input.path[0]].token
}

valid_method_and_path(role) {
    allowed_methods[role][input.method]
    print(input.path)
    allowed_paths[role][input.path[0]]
}

debug = { "user": input.user, "method": input.method, "path": input.path, "role": role } {
    some i
    valid_users[i].username == input.user
    valid_users[i].password == input.password
    some role
    valid_users[i].roles[role]
}
