from src.opa.server import OpaServerHandler
import os

current_path = os.path.abspath('.')
policy_path = os.path.join(current_path, 'example.rego')
policy_id = "example"

if __name__ == "__main__":
    opa_client = OpaServerHandler(
        policy_id=policy_id,
        policy_path=policy_path
    )
    opa_client.create_opa_client()
    print(opa_client.opa_client.check_health())
    print(opa_client.opa_client.list_documents())
    opa_client.update_policy(
        policy_id=policy_id,
        policy_path=policy_path
    )
    print(opa_client.opa_client.list_documents())
