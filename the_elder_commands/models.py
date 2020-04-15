from django.db import models
from django.urls import reverse
from django.contrib.postgres.fields import JSONField


class Character(models.Model):
    race = models.TextField(default="Nord")
    session_key = models.TextField(default="", unique=True)
    skills = JSONField(default=dict)
    desired_level = models.IntegerField(default=1, null=True)
    priority_multiplier = models.FloatField(default=1.5)
    fill_skills = models.BooleanField(default=False)
    timestamp = models.TimeField(auto_now=True)

    @staticmethod
    def get_absolute_url():
        return reverse("tec:character")


class Plugins(models.Model):
    plugin_name = models.TextField(default="", unique=True)
    plugin_usable_name = models.TextField(default="")


class PluginVariants(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["plugin_version", "plugin_language", "plugin_instance"],
                                    name="unique_variant")
        ]

    plugin_instance = models.ForeignKey(Plugins, default=None, on_delete=models.CASCADE)
    plugin_version = models.TextField(default="")
    plugin_language = models.TextField(default="")
    plugin_data = JSONField(default=dict)
