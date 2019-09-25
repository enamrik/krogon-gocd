import krogon_gocd.either as E
import json
from typing import Callable
from .gocd_api import request


def encrypt_secret(kubectl: Callable[[str, str], E.Either], plain_text: str, username: str, password: str, cluster_name: str):
    return E.then(
        request(kubectl, 'POST', '/go/api/admin/encrypt',
                {'Accept': 'application/vnd.go.cd.v1+json'},
                {'value': plain_text},
                username, password, cluster_name),
        (lambda r: json.loads(r)['encrypted_value'])
    )
