import random
import os
import yaml


secret_key = "".join(random.SystemRandom().choices(
    "abcdefghijklmnopqrstuvwxyz0123456789", k=50
))

path = os.getcwd()
path = path[:-13]
host = os.path.basename(path)

settings = {"SITE_NAME": host,
            "DJANGO_SECRET_KEY": secret_key}

with open(f"{path}/deployment_settings.yaml", "w") as yaml_file:
    yaml.dump(settings, yaml_file)
