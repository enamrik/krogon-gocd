
def generate_agent_pod_template(agent_name: str, agent_image: str):
    template = {
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {
            "name": agent_name+"-{{ POD_POSTFIX }}",
            "labels": {"app": agent_name}
        },
        "spec": {
            "serviceAccountName": "default",
            "volumes": [
                {"name": "ssh-secrets", "secret": {"secretName": "gocd-git-ssh"}}
            ],
            "containers": [
                {"name": agent_name+"-{{ CONTAINER_POSTFIX }}",
                 "image": agent_image,
                 "volumeMounts": [
                     {"name": "ssh-secrets",
                      "readOnly": True,
                      "mountPath": "/home/go/.ssh"}
                 ],
                 "securityContext": {"privileged": True}
                 }
            ]
        }
    }
    return template
