import krogon_gocd.yaml as yaml
import python_either.either as E
import krogon_gocd.file as fs
from .gocd_version import gocd_version
from .generate_agent_pod_template import generate_agent_pod_template


def generate_agent_templates(agent_name: str, agent_folder: str, image_url: str):

    agent_pod_template = generate_agent_pod_template(agent_name, image_url)
    fs.write(fs.path_rel_to_cwd(agent_folder) + '/gocd-agent.yaml', yaml.dump(agent_pod_template))

    empty_docker_template = 'FROM gocd/gocd-agent-ubuntu-18.04:v' + gocd_version
    fs.write(fs.path_rel_to_cwd(agent_folder) + '/Dockerfile', empty_docker_template)

    return E.success()


