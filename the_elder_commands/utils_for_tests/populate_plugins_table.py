import copy

from the_elder_commands.inventory import PLUGIN_TEST_DICT_ALTERED_BY_FORM
from the_elder_commands.models import Plugins, PluginVariants, Weapons, Armors, Books, Ingredients, Alchemy, \
    Miscellaneous, Perks, Ammo, SoulsGems, Scrolls, Keys, WordsOfPower, AlterationSpells, ConjurationSpells, \
    DestructionSpells, IllusionSpells, RestorationSpells, OtherSpells


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