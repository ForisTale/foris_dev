from the_elder_commands.models import Plugins, PluginVariants


class PluginsService:
    def __init__(self, request):
        self.selected = request.session.get("selected", [])
        self.all_plugins = self.get_all_plugins()

    class Plugin:
        def __init__(self, name, usable_name, selected, load_order, variants):
            self.name = name
            self.usable_name = usable_name
            self.selected = selected
            self.load_order = load_order
            self.variants = variants

    class Variant:
        def __init__(self, language, version, selected, esl):
            self.language = language
            self.version = version
            self.selected = selected
            self.esl = esl

    def get_all_plugins(self):
        plugins = []
        for plugin in Plugins.objects.all():
            variants = self.get_variants(plugin.name)
            if variants:
                plugins.append(self.Plugin(
                    name=plugin.name,
                    usable_name=plugin.usable_name,
                    selected=self.is_plugin_selected(plugin.name),
                    load_order=self.get_load_order(plugin.name),
                    variants=variants
                ))
        return plugins

    def is_plugin_selected(self, plugin_name):
        for selected in self.selected:
            if selected.get("name") == plugin_name:
                return True
        return False

    def get_load_order(self, plugin_name):
        for selected in self.selected:
            if selected.get("name") == plugin_name:
                return selected.get("load_order")
        return ""

    def get_variants(self, plugin_name):
        variants = []
        for variant in PluginVariants.objects.filter(instance__name=plugin_name).order_by("-version", "language"):
            variants.append(self.Variant(language=variant.language, version=variant.version,
                                         selected=self.is_variant_selected(variant), esl=self.get_esl(variant)))
        return variants

    def is_variant_selected(self, variant_instance):
        for selected in self.selected:
            if selected.get("version") == variant_instance.version and \
                    selected.get("language") == variant_instance.language and \
                    variant_instance.instance.name == selected.get("name"):
                return True
        return False

    @staticmethod
    def get_esl(variant):
        return "esl" if variant.is_esl else ""