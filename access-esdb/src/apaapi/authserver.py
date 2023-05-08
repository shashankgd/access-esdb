from opa import OPAClient
from opa.exceptions import PolicyNotFound
import os

from src.common import config


class OpaServerHandler:
    def __init__(self,
                 url: str = config.OPA_SERVER_URL
                 , policy_id: str = None
                 , policy_path: str = None
                 ):
        self.url = url
        self.policy_id = policy_id
        self.policy_path = policy_path
        self._opa_client = None

    @property
    def opa_client(self):
        return self._opa_client

    @opa_client.setter
    def opa_client(self, value):
        self._opa_client = value

    def create_opa_client(self):
        if self.opa_client is None:
            self.opa_client = OPAClient(self.url)
        self.add_policy(
            policy_id=self.policy_id,
            policy_path=self.policy_path,
        )

    def is_policy_present(self,
                          policy_id: str
                          ) -> bool:
        try:
            self.opa_client.get_policy(policy_id)
            return True
        except PolicyNotFound:
            return False

    def add_policy(self,
                   policy_id: str,
                   policy_path: str
                   ):
        if policy_id and not self.is_policy_present(policy_id):
            self._add_policy(
                policy_id=policy_id,
                policy_path=policy_path
            )

    def update_policy(self,
                      policy_id: str,
                      policy_path: str
                      ):
        self._add_policy(
            policy_id=policy_id,
            policy_path=policy_path
        )

    def _add_policy(self,
                    policy_id: str,
                    policy_path: str
                    ):
        with open(policy_path, 'r') as f:
            policy = f.read()
            self.opa_client.save_policy(policy_id, policy)
            assert self.is_policy_present(policy_id)


if __name__ == "__main__":
    current_path = os.path.abspath('.')
    policy_path = os.path.join(current_path, f'{config.POLICY_ID}.rego')
    policy_id = config.POLICY_ID
    opa_client = OpaServerHandler(
        policy_id=policy_id,
        policy_path=policy_path
    )
    opa_client.create_opa_client()
    print(opa_client.opa_client.check_health())
    print(opa_client.opa_client.list_documents())
