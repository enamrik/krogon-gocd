import krogon_gocd.either as E
import click
from .pipelines_cli import pipelines
from .agents_cli import agents
from .encrypt_secret import encrypt_secret


@click.group()
def gocd():
    pass


gocd.add_command(pipelines)
gocd.add_command(agents)


@gocd.command()
@click.option('--plain-text', required=True, help='Plain text to encrypt')
@click.option('--username', required=True, help='GoCD username')
@click.option('--password', required=True, help='GoCD password')
@click.option('--cluster-name', required=True, help='Cluster where GoCD is hosted')
@click.pass_obj
def encrypt(ctx: dict, plain_text: str, username: str, password: str, cluster_name: str):
    kubectl = ctx['kubectl']

    E.on(
        encrypt_secret(kubectl, plain_text, username, password, cluster_name),
        dict(success=lambda r: print('DONE: \n\nENCRYPTED TEXT: {}'.format(r)),
             failure=lambda e: print('FAILED: {}'.format(e)))
    )


def main():
    gocd()


if __name__ == "__main__":
    gocd()
