from django.db import models
from django.contrib.postgres.fields import JSONField


class Character(models.Model):
    race = models.TextField(default="Nord")
    session_key = models.TextField(default="", unique=True)
    default_skills = JSONField(default=dict)
    desired_skills = JSONField(default=dict)
