from typing import Callable
import krogon_gocd.either as E
from .gocd_api import request


def register_pipeline(k_ctl: Callable[[str, str], E.Either],
                      app_name: str,
                      git_url: str,
                      username: str,
                      password: str,
                      cluster_name: str):

    return E.then(
        _delete_repo_registration(k_ctl, app_name, username, password, cluster_name),
        (lambda secret:  _register_repo(k_ctl, app_name, git_url, username, password, cluster_name))
    )


def _delete_repo_registration(k_ctl: Callable[[str, str], E.Either],
                              app_name: str,
                              username: str,
                              password: str,
                              cluster_name: str):

    return E.catch_error(
        request(k_ctl, 'DELETE', '/go/api/admin/config_repos/' + app_name,
                {'Accept': 'application/vnd.go.cd.v1+json'},
                None,
                username, password, cluster_name),
        (lambda _: E.success())
    )


def _register_repo(k_ctl: Callable[[str, str], E.Either],
                   app_name: str,
                   git_url: str,
                   username: str,
                   password: str,
                   cluster_name: str):

    payload = {
        "id": app_name,
        "plugin_id": "yaml.config.plugin",
        "material": {
            "type": "git",
            "attributes": {
                "url": git_url,
                "branch": "master",
                "auto_update": True
            }
        }
    }

    return request(k_ctl, 'POST', '/go/api/admin/config_repos',
                   {'Accept': 'application/vnd.go.cd.v1+json'},
                   payload,
                   username, password, cluster_name)


