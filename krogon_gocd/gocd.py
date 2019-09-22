import krogon_gocd.yaml as yaml
import krogon_gocd.file as f
from .generate_agent_templates import generate_agent_pod_template
from .encoding import to_base64
from .gocd_version import gocd_version
from krogon_gocd.hash import hash_text


def gocd(
        root_username: str,
        root_password: str,
        git_id_rsa_b64: str,
        git_id_rsa_pub_b64: str,
        git_known_host: str):

    return DeployGoCDTemplate(
        root_username,
        root_password,
        git_id_rsa_b64,
        git_id_rsa_pub_b64,
        git_known_host
    )


class DeployGoCDTemplate:
    def __init__(self,
                 root_username: str,
                 root_password: str,
                 git_id_rsa_b64: str,
                 git_id_rsa_pub_b64: str,
                 git_known_host: str):

        self.root_username = root_username
        self.root_password = root_password
        self.git_id_rsa_b64 = git_id_rsa_b64
        self.git_id_rsa_pub_b64 = git_id_rsa_pub_b64
        self.git_known_host = git_known_host

    def run(self):
        gocd_template_text = f.read(f.path_rel_to_file('./gocd.yaml', __file__))
        gocd_template_text = \
            _inject_agent_pod_template(
                gocd_template_text,
                generate_agent_pod_template(
                    agent_name='gocd-agent-default',
                    agent_image='gocd/gocd-agent-docker-dind:v'+gocd_version)
            )

        return [
                   _secret_template(
                       name='gocd-passwords-file',
                       secret_data={'passwords.txt': to_base64( _create_password_file( self.root_username, self.root_password))}
                   ),
                   _secret_template(name='gocd-git-ssh',
                                    secret_data={'id_rsa': self.git_id_rsa_b64,
                                                 'id_rsa.pub': self.git_id_rsa_pub_b64,
                                                 'known_hosts': to_base64(self.git_known_host)})
               ] + yaml.load_all(gocd_template_text)


def _create_password_file(root_username: str, root_password: str):
    return "{}:{}\n".format(root_username, hash_text(root_password))


def _inject_agent_pod_template(gocd_template_text: str, agent_template: dict) -> str:
    agent_template = yaml.dump(agent_template).replace("\n", "\\n")
    gocd_template_text = gocd_template_text.replace("<< AGENT_POD_TEMPLATE >>", agent_template)
    return gocd_template_text


def _secret_template(name, secret_data: dict):
    return {
        'apiVersion': 'v1',
        'kind': 'Secret',
        'metadata': {'name': name},
        'type': 'Opaque',
        'data': {key: value for key, value in secret_data.items()}
    }


