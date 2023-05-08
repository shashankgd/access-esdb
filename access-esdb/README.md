# This is a test project for access elastic-search with OPA policy implementation

## Setup
#### Create a virtual env or an conda env with python
#### Install requirements from requirements.txt
#### Install opa according to os
#### copy path of rego file and run below command
'''
    opa run --server --addr 127.0.0.1:8181   .<rego-file-path> &

'''

#### Export required tokens for elastic search
#### run datapi/app.py and you are all set