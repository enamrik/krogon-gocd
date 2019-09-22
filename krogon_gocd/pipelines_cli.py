import click
import python_either.either as E
from .register_pipeline import register_pipeline
from .generate_pipeline import generate_pipeline


@click.group()
def pipelines(): pass


@pipelines.command()
@click.option('--app-name', required=True, help='Name of app. Can also be the name of the git repo')
@click.option('--git-url', required=True, help='Git url of repository')
@click.option('--username', required=True, help='GoCD username')
@click.option('--password', required=True, help='GoCD password')
@click.option('--cluster-name', required=True, help='Cluster where GoCD is hosted')
@click.pass_obj
def register(ctx: dict,
             app_name: str,
             git_url: str,
             username: str,
             password: str,
             cluster_name: str):
    kubectl = ctx['kubectl']

    register_pipeline(kubectl, app_name, git_url, username, password, cluster_name) \
    | E.on | dict(success=lambda r: print('DONE: {}'.format(r)),
                  failure=lambda e: print('FAILED: {}'.format(e)))


@pipelines.command()
@click.option('--app-name', required=True, help='Name of app. Can also be the name of the git repo')
@click.option('--git-url', required=True, help='Git url of repository')
@click.option('--python-agent-name', required=True, help='elastic profile id of a GoCD agent has pipenv installed. '
                                                         'Used to run krogon command')
@click.option('--krogon-file', required=True, help='Krogon file')
@click.option('--username', required=True, help='GoCD username')
@click.option('--password', required=True, help='GoCD password')
@click.option('--cluster-name', required=True, help='Cluster where GoCD is hosted')
@click.pass_obj
def generate(ctx: dict,
             app_name: str,
             git_url: str,
             python_agent_name: str,
             krogon_file: str,
             username: str,
             password: str,
             cluster_name: str):
    kubectl = ctx['kubectl']
    project_id = ctx['project_id']
    service_account_b64 = ctx['service_account_b64']
    krogon_install_url = ctx['krogon_install_url']

    generate_pipeline(kubectl,
                      project_id,
                      service_account_b64,
                      app_name,
                      git_url,
                      python_agent_name,
                      krogon_file,
                      krogon_install_url,
                      username,
                      password,
                      cluster_name) \
    | E.on | dict(success=lambda r: print('DONE: {}'.format(r)),
                  failure=lambda e: print('FAILED: {}'.format(e)))
