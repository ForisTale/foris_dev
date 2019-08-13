from django.db import models
from django.urls import reverse
from django.contrib.postgres.fields import JSONField


class Character(models.Model):
    race = models.TextField(default="Nord")
    session_key = models.TextField(default="", unique=True)
    skills = JSONField(default=dict)
    desired_level = models.IntegerField(default=1, null=True)
    priority_multiplier = models.FloatField(default=1.5)

    @staticmethod
    def get_absolute_url():
        return reverse("tec:character")
