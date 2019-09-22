from typing import Callable
import python_either.either as E
from .gocd_api import request
import json


def encrypt_secret(kubectl: Callable[[str, str], E.Either], plain_text: str, username: str, password: str, cluster_name: str):
    return request(kubectl, 'POST', '/go/api/admin/encrypt',
                   {'Accept': 'application/vnd.go.cd.v1+json'},
                   {'value': plain_text},
                   username, password, cluster_name) \
            | E.then | (lambda r: json.loads(r)['encrypted_value'])
