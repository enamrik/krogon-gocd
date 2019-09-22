import click
import python_either.either as E
from .register_agent_template import register_agent_template
from .generate_agent_templates import generate_agent_templates


@click.group()
@click.pass_obj
def agents(): pass


@agents.command()
@click.option('--agent-name', required=True, help='GoCD agent\'s elastic profile id')
@click.option('--image-url', required=True, help='Docker fully qualified image name on which agent is based')
@click.option('--out-dir', required=True, help='Directory where Dockerfile should be stored')
def generate_agent(agent_name: str, out_dir: str, image_url: str):

    generate_agent_templates(agent_name, out_dir, image_url) \
    | E.on | dict(success=lambda r: print('DONE: {}'.format(r)),
                  failure=lambda e: print('FAILED: {}'.format(e)))


@agents.command()
@click.option('--agent-name', required=True, help='GoCD agent\'s elastic profile id')
@click.option('--agent-template-path', required=True, help='file path and name where template was stored')
@click.option('--image-url', required=True, help='Docker fully qualified image name on which agent is based')
@click.option('--cluster-name', required=True, help='Name of cluster where GoCD is hosted')
@click.option('--username', required=True, help='GoCD username')
@click.option('--password', required=True, help='GoCD password')
@click.pass_obj
def register_agent(ctx: dict, agent_name: str, agent_template_path: str, image_url,
                   username: str, password: str, cluster_name: str):
    kubectl = ctx['kubectl']

    register_agent_template(kubectl, agent_name, agent_template_path,
                            image_url, username, password, cluster_name) \
    | E.on | dict(success=lambda r: print('DONE: {}'.format(r)),
                  failure=lambda e: print('FAILED: {}'.format(e)))
