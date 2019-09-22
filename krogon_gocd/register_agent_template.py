import python_either.either as E
import krogon_gocd.file as f
from typing import Callable
from .gocd_api import request


def register_agent_template(
        k_ctl: Callable[[str, str], E.Either],
        agent_name: str,
        agent_template_path: str,
        image_url: str,
        username: str,
        password: str,
        cluster_name: str):

    pod_template_text = f.read(f.path_rel_to_cwd(agent_template_path))

    payload = {
        'id': agent_name,
        'plugin_id': 'cd.go.contrib.elasticagent.kubernetes',
        'properties': [
            {'key': 'Image', 'value': image_url},
            {'key': 'PodConfiguration', 'value': pod_template_text},
            {'key': 'SpecifiedUsingPodConfiguration', 'value': 'true'},
            {'key': 'Privileged', 'value': 'true'}
        ]
    }

    return request(k_ctl, 'POST', '/go/api/elastic/profiles',
                   {'Accept': 'application/vnd.go.cd.v1+json'},
                   payload,
                   username, password, cluster_name)


