import yaml


def load_yaml(filename):
    with open(filename) as f:
        return yaml.safe_load(f)
