from django.db import models


class Plugins(models.Model):
    name = models.TextField(default="", unique=True)
    usable_name = models.TextField(default="")


class PluginVariants(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["version", "language", "instance", "is_esl"],
                                    name="unique_variant")
        ]

    instance = models.ForeignKey(Plugins, default=None, on_delete=models.CASCADE)
    version = models.TextField(default="")
    language = models.TextField(default="")
    is_esl = models.BooleanField(default=False)
    plugin_data = models.JSONField(default=dict)
