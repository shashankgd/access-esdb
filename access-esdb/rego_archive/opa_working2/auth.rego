package auth

valid_users = [
    {"username": "alice", "password": "alice1", "roles": {"reader", "writer", "admin"}},
    {"username": "james", "password": "james1", "roles": {"reader"}},
    {"username": "kelly", "password": "kelly1", "roles": {"execute"}}
]

api_tokens = {
    "reader": {"token": {"reader1"}},
    "writer": {"token": {"writer1"}},
    "admin": {"token": {"admin1"}},
    "execute": {"token": {"execute1"}}
}

allowed_methods = {
    "admin": {"GET", "PUT", "POST", "DELETE"},
    "reader": {"GET"},
    "writer": {"PUT", "POST"},
    "execute": {"GET"}
}

allowed_paths = {
    "admin": {"", "ratings"},
        "reader": {"read", "reviews", "ratings"},
        "writer": {"write", "reviews", "ratings"},
}

get_token = token {
    some i
    valid_users[i].username == input.user
    valid_users[i].password == input.password
    some role
    valid_users[i].roles[role]
    valid_method_and_path(role)
    token := api_tokens[role].token[_]
}

valid_method_and_path(role) {
    allowed_methods[role][input.method]
    allowed_paths[role][input.path[0]]
}

debug = { "user": input.user, "method": input.method, "path": input.path, "role": role } {
    some i
    valid_users[i].username == input.user
    valid_users[i].password == input.password
    some role
    valid_users[i].roles[role]
}
