import copy
import os

from the_elder_commands.inventory import DEFAULT_SKILLS, PLUGIN_TEST_DICT_ALTERED_BY_FORM
from the_elder_commands.models import Plugins, PluginVariants, Weapons, WordsOfPower, AlterationSpells, Ammo, Armors, \
    Alchemy, Miscellaneous, RestorationSpells, ConjurationSpells, Scrolls, SoulsGems, OtherSpells, Ingredients, Books, \
    Keys, Perks, DestructionSpells, IllusionSpells


class ManageTestFiles:
    def __init__(self):
        self.test_file_full_path = None

    def create_test_files(self, data_dict):
        local_dir = os.path.dirname(os.path.abspath(__file__))
        key, value = self.unpack_dict(data_dict)
        self.test_file_full_path = os.path.join(local_dir, key)
        with open(os.path.join(local_dir, key), "w+", encoding="utf-8") as file:
            file.write(str(value))

    def delete_test_files(self):
        try:
            os.remove(self.test_file_full_path)
        except (FileNotFoundError, TypeError):
            pass

    @staticmethod
    def unpack_dict(dictionary):
        dict_view = dictionary.items()
        tuples_list = list(dict_view)
        dict_tuple = tuples_list[0]
        return dict_tuple[0], dict_tuple[1]


def check_test_tag(self, tag_string):
    method = getattr(self, self._testMethodName)
    tags = getattr(method, "tags", {})
    if tag_string in tags:
        return True


def select_plugin(self):
    session = self.client.session
    session.update({"selected": [{
            "name": "test 01",
            "usable_name": "test_01",
            "version": "03",
            "language": "english",
            "load_order": "A5",
            "is_esl": False,
        }]})
    session.save()


def populate_plugins_table():
    for index in range(4):
        plugin = Plugins.objects.create(name="test 0" + str(index+1), usable_name="test_0" + str(index+1))
        plugin.save()
        corrected_dict = copy.deepcopy(PLUGIN_TEST_DICT_ALTERED_BY_FORM)
        for num in range(4):
            variant = PluginVariants.objects.create(instance=plugin, version="0" + str(num+1), language="english",
                                                    is_esl=False)
            variant.save()

            Weapons.objects.create(variant=variant, items=corrected_dict.get("WEAP"))
            Armors.objects.create(variant=variant, items=corrected_dict.get("ARMO"))
            Books.objects.create(variant=variant, items=corrected_dict.get("BOOK"))
            Ingredients.objects.create(variant=variant, items=corrected_dict.get("INGR"))
            Alchemy.objects.create(variant=variant, items=corrected_dict.get("ALCH"))
            Miscellaneous.objects.create(variant=variant, items=corrected_dict.get("MISC"))
            Perks.objects.create(variant=variant, perks=corrected_dict.get("PERK"))
            Ammo.objects.create(variant=variant, items=corrected_dict.get("AMMO"))
            SoulsGems.objects.create(variant=variant, items=corrected_dict.get("SLGM"))
            Scrolls.objects.create(variant=variant, items=corrected_dict.get("SCRL"))
            Keys.objects.create(variant=variant, items=corrected_dict.get("KEYM"))
            WordsOfPower.objects.create(variant=variant, words=corrected_dict.get("WOOP"))
            AlterationSpells.objects.create(variant=variant, spells=[corrected_dict.get("SPEL")[0]])
            ConjurationSpells.objects.create(variant=variant, spells=[corrected_dict.get("SPEL")[2]])
            DestructionSpells.objects.create(variant=variant, spells=[corrected_dict.get("SPEL")[1]])
            IllusionSpells.objects.create(variant=variant, spells=[corrected_dict.get("SPEL")[3]])
            RestorationSpells.objects.create(variant=variant, spells=[corrected_dict.get("SPEL")[4]])
            OtherSpells.objects.create(variant=variant, spells=[corrected_dict.get("SPEL")[5]])


def set_up_default_nord():
    skills = copy.deepcopy(DEFAULT_SKILLS)
    skills["Combat"]["twohanded"]["default_value"] += 10
    skills["Stealth"]["speechcraft"]["default_value"] += 5
    skills["Stealth"]["lightarmor"]["default_value"] += 5
    for skill in ["block", "onehanded", "smithing"]:
        skills["Combat"][skill]["default_value"] += 5
    return skills
