from setuptools import setup, find_packages


def read_file(filename):
    with open(filename) as f:
        return f.read()


setup(
    python_requires="~=3.7",
    name="krogon-gocd",
    version=read_file("./krogon_gocd/VERSION").strip(),
    description="Tool for generating and executing K8s templates",
    long_description=read_file("README.md"),
    author="Kirmanie L Ravariere",
    author_email="enamrik@gmail.com",
    license=read_file("LICENSE"),
    packages=find_packages(exclude=("tests", "outputs")),
    package_data={"krogon_gocd": ["URL", "VERSION", "*.txt", "*.yml", "*.template", "**/*.sh", "*.ini", "bin/**/*"]},
    include_package_data=True,
    install_requires=[
        'ruamel.yaml==0.15.87',
        'click==7.0',
        'bcrypt==3.1.6',
    ],
    extras_require={
        'dev': [
            'pytest',
            'dictdiffer==0.7.1',
            'python-mock@git+ssh://git@github.com/enamrik/python-mock.git'
        ]
    },
)
