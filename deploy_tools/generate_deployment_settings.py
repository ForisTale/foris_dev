import random
import os
import yaml
from pathlib import Path


secret_key = "".join(random.SystemRandom().choices(
    "abcdefghijklmnopqrstuvwxyz0123456789", k=50
))

cwd = Path().cwd()
base_path = cwd.parents[0]

host = base_path.parts[-1]
database_name = "".join([letter if letter.isalnum() else "_" for letter in host.lower()])

settings = {"SITE_NAME": host,
            "DATABASE_NAME": database_name,
            "DJANGO_SECRET_KEY": secret_key}

destined_file_path = os.path.join(f"{base_path}", "deployment_settings.yaml")

with open(destined_file_path, "w") as yaml_file:
    yaml.dump(settings, yaml_file)
