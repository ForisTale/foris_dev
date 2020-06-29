from django.db import models


class Plugins(models.Model):
    name = models.TextField(default="", unique=True)
    usable_name = models.TextField(default="")


class PluginVariants(models.Model):
    instance = models.ForeignKey(Plugins, default=None, on_delete=models.CASCADE)
    version = models.TextField(default="")
    language = models.TextField(default="")
    is_esl = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["version", "language", "instance", "is_esl"],
                                    name="unique_variant")
        ]


class Weapons(models.Model):
    variant = models.ForeignKey(PluginVariants, default=None, on_delete=models.CASCADE)
    items = models.JSONField(default=list, blank=True)


class Armors(models.Model):
    variant = models.ForeignKey(PluginVariants, default=None, on_delete=models.CASCADE)
    items = models.JSONField(default=list, blank=True)


class Books(models.Model):
    variant = models.ForeignKey(PluginVariants, default=None, on_delete=models.CASCADE)
    items = models.JSONField(default=list, blank=True)


class Ingredients(models.Model):
    variant = models.ForeignKey(PluginVariants, default=None, on_delete=models.CASCADE)
    items = models.JSONField(default=list, blank=True)


class Alchemy(models.Model):
    variant = models.ForeignKey(PluginVariants, default=None, on_delete=models.CASCADE)
    items = models.JSONField(default=list, blank=True)


class Miscellaneous(models.Model):
    variant = models.ForeignKey(PluginVariants, default=None, on_delete=models.CASCADE)
    items = models.JSONField(default=list, blank=True)


class Perks(models.Model):
    variant = models.ForeignKey(PluginVariants, default=None, on_delete=models.CASCADE)
    perks = models.JSONField(default=list, blank=True)


class Ammo(models.Model):
    variant = models.ForeignKey(PluginVariants, default=None, on_delete=models.CASCADE)
    items = models.JSONField(default=list, blank=True)


class Scrolls(models.Model):
    variant = models.ForeignKey(PluginVariants, default=None, on_delete=models.CASCADE)
    items = models.JSONField(default=list, blank=True)


class SoulsGems(models.Model):
    variant = models.ForeignKey(PluginVariants, default=None, on_delete=models.CASCADE)
    items = models.JSONField(default=list, blank=True)


class Keys(models.Model):
    variant = models.ForeignKey(PluginVariants, default=None, on_delete=models.CASCADE)
    items = models.JSONField(default=list, blank=True)


class AlterationSpells(models.Model):
    variant = models.ForeignKey(PluginVariants, default=None, on_delete=models.CASCADE)
    spells = models.JSONField(default=list, blank=True)


class DestructionSpells(models.Model):
    variant = models.ForeignKey(PluginVariants, default=None, on_delete=models.CASCADE)
    spells = models.JSONField(default=list, blank=True)


class ConjurationSpells(models.Model):
    variant = models.ForeignKey(PluginVariants, default=None, on_delete=models.CASCADE)
    spells = models.JSONField(default=list, blank=True)


class IllusionSpells(models.Model):
    variant = models.ForeignKey(PluginVariants, default=None, on_delete=models.CASCADE)
    spells = models.JSONField(default=list, blank=True)


class RestorationSpells(models.Model):
    variant = models.ForeignKey(PluginVariants, default=None, on_delete=models.CASCADE)
    spells = models.JSONField(default=list, blank=True)


class OtherSpells(models.Model):
    variant = models.ForeignKey(PluginVariants, default=None, on_delete=models.CASCADE)
    spells = models.JSONField(default=list, blank=True)


class WordsOfPower(models.Model):
    variant = models.ForeignKey(PluginVariants, default=None, on_delete=models.CASCADE)
    spells = models.JSONField(default=list, blank=True)
