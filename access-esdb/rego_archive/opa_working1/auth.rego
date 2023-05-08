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
    role == "admin"
    input.method == "GET"
    input.path == [""]
} {
    role == "reader"
    input.method == "GET"
    input.path == ["read"]
} {
    role == "writer"
    input.method == "PUT"
    input.path == ["write"]
} {
    role == "writer"
    input.method == "POST"
    input.path == ["write"]
}
