import bcrypt
from krogon_gocd import gocd
from base64 import b64decode


def test_can_create_default_template():
    root_username = "admin"
    root_password = "password1"
    git_id_rsa_b64 = "gitPrivateHash"
    git_id_rsa_pub_b64 = "gitPublicHash"
    git_known_host = 'someKnownHost'

    template = gocd(
        root_username=root_username,
        root_password=root_password,
        git_id_rsa_b64=git_id_rsa_b64,
        git_id_rsa_pub_b64=git_id_rsa_pub_b64,
        git_known_host=git_known_host)

    result = template.run()

    assert result[0]['metadata']['name'] == 'gocd-passwords-file'
    credentials = b64decode(result[0]['data']['passwords.txt']).decode('utf-8').strip().split(':')
    assert credentials[0] == root_username
    assert bcrypt.checkpw(
        root_password.encode('utf-8'),
        credentials[1].encode('utf-8')), "Password hash invalid"

    assert result[1]['metadata']['name'] == 'gocd-git-ssh'
    assert result[1]['data']['id_rsa'] == git_id_rsa_b64
    assert result[1]['data']['id_rsa.pub'] == git_id_rsa_pub_b64
    assert b64decode(result[1]['data']['known_hosts']).decode('utf-8') == git_known_host

    assert result[2]['metadata']['name'] == 'gocd'



