def template_variables(request):
    return {
        "playable_races": [
            ["Altmer", "altmer_race"], ["Argonian", "argonian_race"],
            ["Bosmer", "bosmer_race"], ["Breton", "breton_race"],
            ["Dunmer", "dunmer_race"], ["Imperial", "imperial_race"],
            ["Khajiit", "khajiit_race"], ["Nord", "nord_race"],
            ["Ork", "ork_race"], ["Redguard", "redguard_race"],
        ],
        "main_categories": ["skills", "items", "spells", "other", "plugins", "commands"],
        "items_categories": ["Weapons", "Armors", "Ammo", "Books", "Ingredients", "Alchemy", "Scrolls", "SoulGems",
                             "Keys", "Miscellaneous"],
    }


ADD_PLUGIN_SUCCESS_MESSAGE = "Plugin was successfully added to database."

ADD_PLUGIN_FILE_ERROR_MESSAGE = "File was incorrect!"

ADD_PLUGIN_PLUGIN_EXIST_ERROR_MESSAGE = "Plugin with this Name, Version and Language already exists."

COMMANDS_SUCCESS_MESSAGE = "Commands are ready on the Commands page."

ITEMS_COMMANDS_POST_EMPTY_MESSAGE = "No items selected!"

ITEMS_CONVERT_POST_ERROR = "Javascript error! Something went wrong! If the error persists, contact Foris."

INCORRECT_LOAD_ORDER = "Load order need to be hex number between 00 and FF for esp files and from FE001 to "\
                       "FEFFF for esl files!"

PLUGINS_ERROR_STRING_IS_EMTPY = "Name cannot be empty!"

PLUGINS_ERROR_NAME_BECOME_EMPTY = "Name cannot consist only from special signs!"

NO_PLUGIN_SELECTED_ERROR_MESSAGE = "Please select plugin before use Items or Spells."

SKILLS_CONSOLE_NAME = [
    'alteration', 'conjuration', 'destruction', 'enchanting',
    'illusion', 'restoration', 'marksman', 'block', 'heavyarmor',
    'onehanded', 'smithing', 'twohanded', 'alchemy', 'lightarmor',
    'lockpicking', 'pickpocket', 'sneak', 'speechcraft'
]

DEFAULT_SKILLS = {
    "Magic": {
        "Alteration": {
            "console_name": "alteration",
            "default_value": 15,
            "desired_value": "",
            "multiplier": False,
            "sim": 2,
            "sio": 0,
            "sum": 3,
        },
        "Conjuration":  {
            "console_name": "conjuration",
            "default_value": 15,
            "desired_value": "",
            "multiplier": False,
            "sim": 2,
            "sio": 0,
            "sum": 2.1,
        },
        "Destruction":  {
            "console_name": "destruction",
            "default_value": 15,
            "desired_value": "",
            "multiplier": False,
            "sim": 2,
            "sio": 0,
            "sum": 1.35,
        },
        "Enchanting":  {
            "console_name": "enchanting",
            "default_value": 15,
            "desired_value": "",
            "multiplier": False,
            "sim": 1,
            "sio": 170,
            "sum": 900,
        },
        "Illusion":  {
            "console_name": "illusion",
            "default_value": 15,
            "desired_value": "",
            "multiplier": False,
            "sim": 2,
            "sio": 0,
            "sum": 4.6,
        },
        "Restoration":  {
            "console_name": "restoration",
            "default_value": 15,
            "desired_value": "",
            "multiplier": False,
            "sim": 2,
            "sio": 0,
            "sum": 2,
        },
    },
    "Combat": {
        "Archery":  {
            "console_name": "marksman",
            "default_value": 15,
            "desired_value": "",
            "multiplier": False,
            "sim": 2,
            "sio": 0,
            "sum": 9.3,
        },
        "Block":  {
            "console_name": "block",
            "default_value": 15,
            "desired_value": "",
            "multiplier": False,
            "sim": 2,
            "sio": 0,
            "sum": 8.1,
        },
        "Heavy Armor":  {
            "console_name": "heavyarmor",
            "default_value": 15,
            "desired_value": "",
            "multiplier": False,
            "sim": 2,
            "sio": 0,
            "sum": 3.8,
        },
        "One-handed":  {
            "console_name": "onehanded",
            "default_value": 15,
            "desired_value": "",
            "multiplier": False,
            "sim": 2,
            "sio": 0,
            "sum": 6.3,
        },
        "Smithing":  {
            "console_name": "smithing",
            "default_value": 15,
            "desired_value": "",
            "multiplier": False,
            "sim": 0.25,
            "sio": 300,
            "sum": 1,
        },
        "Two-handed":  {
            "console_name": "twohanded",
            "default_value": 15,
            "desired_value": "",
            "multiplier": False,
            "sim": 2,
            "sio": 0,
            "sum": 5.95,
        },
    },
    "Stealth": {
        "Alchemy":  {
            "console_name": "alchemy",
            "default_value": 15,
            "desired_value": "",
            "multiplier": False,
            "sim": 1.6,
            "sio": 65,
            "sum": 0.75,
        },
        "Light Armor":  {
            "console_name": "lightarmor",
            "default_value": 15,
            "desired_value": "",
            "multiplier": False,
            "sim": 2,
            "sio": 0,
            "sum": 4,
        },
        "Lockpicking":  {
            "console_name": "lockpicking",
            "default_value": 15,
            "desired_value": "",
            "multiplier": False,
            "sim": 0.25,
            "sio": 300,
            "sum": 45,
        },
        "Pickpocket":  {
            "console_name": "pickpocket",
            "default_value": 15,
            "desired_value": "",
            "multiplier": False,
            "sim": 0.25,
            "sio": 250,
            "sum": 8.1,
        },
        "Sneak":  {
            "console_name": "sneak",
            "default_value": 15,
            "desired_value": "",
            "multiplier": False,
            "sim": 0.5,
            "sio": 120,
            "sum": 11.25,
        },
        "Speech":  {
            "console_name": "speechcraft",
            "default_value": 15,
            "desired_value": "",
            "multiplier": False,
            "sim": 2,
            "sio": 0,
            "sum": 0.36,
        },
    },
}

RACES_EXTRA_SKILLS = {
    "Altmer": {
        10: {"Magic": "Illusion"},
        5: {"Magic": ["Alteration", "Conjuration", "Destruction",
                      "Enchanting", "Restoration"]},
    },
    "Argonian": {
        10: {"Stealth": "Lockpicking"},
        5: {"Magic": ["Alteration", "Restoration"],
            "Stealth": ["Light Armor", "Pickpocket", "Sneak"]},
    },
    "Bosmer": {
        10: {"Combat": "Archery"},
        5: {"Stealth": ["Alchemy", "Light Armor", "Lockpicking",
                        "Pickpocket", "Sneak"]},
    },
    "Breton": {
        10: {"Magic": "Conjuration"},
        5: {"Magic": ["Alteration", "Illusion", "Restoration"],
            "Stealth": ["Alchemy", "Speech"]},
    },
    "Dunmer": {
        10: {"Magic": "Destruction"},
        5: {"Magic": ["Alteration", "Illusion"],
            "Stealth": ["Alchemy", "Light Armor", "Sneak"]},
    },
    "Imperial": {
        10: {"Magic": "Restoration"},
        5: {"Magic": ["Destruction", "Enchanting"],
            "Combat": ["Block", "Heavy Armor", "One-handed"]},
    },
    "Khajiit": {
        10: {"Stealth": "Sneak"},
        5: {"Stealth": ["Alchemy", "Lockpicking", "Pickpocket"],
            "Combat": ["Archery", "One-handed"]},
    },
    "Nord": {
        10: {"Combat": "Two-handed"},
        5: {"Stealth": ["Speech", "Light Armor"],
            "Combat": ["Block", "One-handed", "Smithing"]},
    },
    "Ork": {
        10: {"Combat": "Heavy Armor"},
        5: {"Combat": ["Block", "One-handed", "Smithing", "Two-handed"],
            "Magic": ["Enchanting"]},
    },
    "Redguard": {
        10: {"Combat": "One-handed"},
        5: {"Combat": ["Archery", "Block", "Smithing"],
            "Magic": ["Alteration", "Destruction"]},
    },
}

PLUGIN_TEST_DICT = {
    "isEsl": False,
    "WEAP": [
        {
            "fullName": "Stalowy wielki miecz skwaru",
            "editorId": "DA14DremoraGreatswordFire03",
            "formId": "017288",
            "Weight": 17,
            "Value": 90,
            "Damage": 17,
            "Type": "Two Handed",
            "Description": "Zadaje celowi <mag> pkt. obrażeń od ognia. Płonące cele odnoszą dodatkowe obrażenia.|"
        },
        {
            "fullName": "Daedryczny wielki miecz inferna",
            "editorId": "EnchDaedricGreatswordDremoraFire06",
            "formId": "017009",
            "Weight": 23,
            "Value": 2500,
            "Damage": 24,
            "Type": "Two Handed",
            "Description": ""
        }
    ],
    "ARMO": [
        {
            "fullName": "Buty",
            "editorId": "DremoraBoots",
            "formId": "016FFF",
            "Weight": 1,
            "Value": 4,
            "Armor rating": 0,
            "Armor type": "Clothing",
            "Description": ""
        },
        {
            "fullName": "Elfia tarcza wybitnego blokowania",
            "editorId": "EnchArmorElvenShieldBlock04",
            "formId": "10FC28",
            "Weight": 4,
            "Value": 115,
            "Armor rating": 21,
            "Armor type": "Light Armor",
            "Description": "Tarcza blokuje o <mag>% obrażeń więcej.|"
        }
    ],
    "BOOK": [
        {
            "fullName": "Księga czarów: Przywołanie Władcy Dremor",
            "editorId": "SpellTomeConjureDremoraLord",
            "formId": "10FD60",
            "Weight": 1,
            "Value": 730
        },
        {
            "fullName": "Księga czarów: Piorun",
            "editorId": "SpellTomeThunderbolt",
            "formId": "10F7F5",
            "Weight": 1,
            "Value": 750
        }
    ],
    "INGR": [
        {
            "fullName": "Okoń srebrnoboczny",
            "editorId": "CritterPondFish01Ingredient",
            "formId": "106E1C",
            "Weight": 0.25,
            "Value": 15,
            "Effects": "Przywrócenie kondycji|Osłabienie regeneracji kondycji|Wyniszczenie zdrowia|Odporność na mróz"
        },
        {
            "fullName": "Abecejski długopłetwiak",
            "editorId": "CritterPondFish02Ingredient",
            "formId": "106E1B",
            "Weight": 0.5,
            "Value": 15,
            "Effects": "Podatność na mróz|Premia do skradania|Wrażliwość na trucizny|Premia do przywracania"
        }
    ],
    "ALCH": [
        {
            "fullName": "Miód z owocem jałowca",
            "editorId": "MQ101JuniperMead",
            "formId": "107A8A",
            "Weight": 0,
            "Value": 0,
            "Effects": "Przywrócenie kondycji|Osłabienie regeneracji kondycji"
        },
        {
            "fullName": "Miód",
            "editorId": "FoodHoney",
            "formId": "10394D",
            "Weight": 0,
            "Value": 0,
            "Effects": "Przywrócenie zdrowia"
        }
    ],
    "MISC": [
        {
            "fullName": "Wypaczony klejnot duszy",
            "editorId": "MGRArniel04SoulGem",
            "formId": "10E44B",
            "Weight": 0.5,
            "Value": 0
        },
        {
            "fullName": "Posąg Dibelli",
            "editorId": "TG01HaelgaStatuePost",
            "formId": "10CC6A",
            "Weight": 2,
            "Value": 100
        }
    ],
    "AMMO": [
        {
            "fullName": "Dwemerski bełt",
            "editorId": "DwarvenSphereBolt02",
            "formId": "10EC8C",
            "Weight": 0,
            "Value": 0,
            "Damage": 15
        },
        {
            "fullName": "Żelazna strzała",
            "editorId": "FollowerIronArrow",
            "formId": "10E2DE",
            "Weight": 0,
            "Value": 1,
            "Damage": 8
        }
    ],
    "SCRL": [
        {
            "fullName": "Spostrzeżenia Shalidora: Magia",
            "editorId": "MGR21ScrollMagicka",
            "formId": "1076EC",
            "Weight": 0.5,
            "Value": 50,
            "Effects": "Zwiększa magię o <mag> pkt.|Regeneracja magii przyśpieszona o <mag>% przez <dur> s.|"
        },
        {
            "fullName": "Spostrzeżenia Shalidora: Przywołanie",
            "editorId": "MGR21ScrollConjuration",
            "formId": "1076EB",
            "Weight": 0.5,
            "Value": 50,
            "Effects": "Zwiększa czas trwania i zmniejsza koszt zaklęć przywołania przez <dur> s.|"
        }
    ],
    "SLGM": [
        {
            "fullName": "Klejnot duszy Wylandriah",
            "editorId": "FFRiften14SoulGem",
            "formId": "043E26",
            "Weight": 0,
            "Value": 0
        },
        {
            "fullName": "Uzdatniony klejnot duszy",
            "editorId": "WhiterunSoulGem",
            "formId": "094E40",
            "Weight": 0.2,
            "Value": 25
        }
    ],
    "KEYM": [
        {
            "fullName": "Klucz do skonfiskowanych towarów",
            "editorId": "RiftenConfiscatedGoodsChestKey",
            "formId": "10E7E6",
            "Weight": 0,
            "Value": 0
        },
        {
            "fullName": "Klucz do pokoju Malurila",
            "editorId": "MzinchaleftKey01",
            "formId": "10BEFF",
            "Weight": 0,
            "Value": 0
        }
    ],
    "SPEL": [
        {
            "fullName": "Spalenie",
            "editorId": "IncinerateLeftHand",
            "formId": "10FD5F",
            "Effects": "Wybuch ognia zadaje <mag> pkt. obrażeń. Płonące cele ponoszą dodatkowe obrażenia.|||",
            "Spell Mastery": "Ekspert - zniszczenie"
        },
        {
            "fullName": "Płaszcz Płomieni",
            "editorId": "DragonPriestMaskUltraFlameCloak",
            "formId": "10FC17",
            "Effects": "Przez <dur> s zadaje celom w zasięgu broni do walki wręcz pkt. obrażeń od ognia na sekundę.",
            "Spell Mastery": "Czeladnik - zniszczenie"
        }
    ],
    "WOOP": [
        {
            "fullName": "Nus",
            "editorId": "WordNus",
            "formId": "0602A5",
            "Translation": "Posąg"
        },
        {
            "fullName": "Slen",
            "editorId": "WordSlen",
            "formId": "0602A4",
            "Translation": "Ciało"
        }
    ]
}

PLUGIN_TEST_FILE = '''{
    "isEsl": false,
    "WEAP": [
        {
            "fullName": "Stalowy wielki miecz skwaru",
            "editorId": "DA14DremoraGreatswordFire03",
            "formId": "017288",
            "Weight": 17,
            "Value": 90,
            "Damage": 17,
            "Type": "Two Handed",
            "Description": "Zadaje celowi <mag> pkt. obrażeń od ognia. Płonące cele odnoszą dodatkowe obrażenia.|"
        },
        {
            "fullName": "Daedryczny wielki miecz inferna",
            "editorId": "EnchDaedricGreatswordDremoraFire06",
            "formId": "017009",
            "Weight": 23,
            "Value": 2500,
            "Damage": 24,
            "Type": "Two Handed",
            "Description": ""
        }
    ],
    "ARMO": [
        {
            "fullName": "Buty",
            "editorId": "DremoraBoots",
            "formId": "016FFF",
            "Weight": 1,
            "Value": 4,
            "Armor rating": 0,
            "Armor type": "Clothing",
            "Description": ""
        },
        {
            "fullName": "Elfia tarcza wybitnego blokowania",
            "editorId": "EnchArmorElvenShieldBlock04",
            "formId": "10FC28",
            "Weight": 4,
            "Value": 115,
            "Armor rating": 21,
            "Armor type": "Light Armor",
            "Description": "Tarcza blokuje o <mag>% obrażeń więcej.|"
        }
    ],
    "BOOK": [
        {
            "fullName": "Księga czarów: Przywołanie Władcy Dremor",
            "editorId": "SpellTomeConjureDremoraLord",
            "formId": "10FD60",
            "Weight": 1,
            "Value": 730
        },
        {
            "fullName": "Księga czarów: Piorun",
            "editorId": "SpellTomeThunderbolt",
            "formId": "10F7F5",
            "Weight": 1,
            "Value": 750
        }
    ],
    "INGR": [
        {
            "fullName": "Okoń srebrnoboczny",
            "editorId": "CritterPondFish01Ingredient",
            "formId": "106E1C",
            "Weight": 0.25,
            "Value": 15,
            "Effects": "Przywrócenie kondycji|Osłabienie regeneracji kondycji|Wyniszczenie zdrowia|Odporność na mróz"
        },
        {
            "fullName": "Abecejski długopłetwiak",
            "editorId": "CritterPondFish02Ingredient",
            "formId": "106E1B",
            "Weight": 0.5,
            "Value": 15,
            "Effects": "Podatność na mróz|Premia do skradania|Wrażliwość na trucizny|Premia do przywracania"
        }
    ],
    "ALCH": [
        {
            "fullName": "Miód z owocem jałowca",
            "editorId": "MQ101JuniperMead",
            "formId": "107A8A",
            "Weight": 0,
            "Value": 0,
            "Effects": "Przywrócenie kondycji|Osłabienie regeneracji kondycji"
        },
        {
            "fullName": "Miód",
            "editorId": "FoodHoney",
            "formId": "10394D",
            "Weight": 0,
            "Value": 0,
            "Effects": "Przywrócenie zdrowia"
        }
    ],
    "MISC": [
        {
            "fullName": "Wypaczony klejnot duszy",
            "editorId": "MGRArniel04SoulGem",
            "formId": "10E44B",
            "Weight": 0.5,
            "Value": 0
        },
        {
            "fullName": "Posąg Dibelli",
            "editorId": "TG01HaelgaStatuePost",
            "formId": "10CC6A",
            "Weight": 2,
            "Value": 100
        }
    ],
    "AMMO": [
        {
            "fullName": "Dwemerski bełt",
            "editorId": "DwarvenSphereBolt02",
            "formId": "10EC8C",
            "Weight": 0,
            "Value": 0,
            "Damage": 15
        },
        {
            "fullName": "Żelazna strzała",
            "editorId": "FollowerIronArrow",
            "formId": "10E2DE",
            "Weight": 0,
            "Value": 1,
            "Damage": 8
        }
    ],
    "SCRL": [
        {
            "fullName": "Spostrzeżenia Shalidora: Magia",
            "editorId": "MGR21ScrollMagicka",
            "formId": "1076EC",
            "Weight": 0.5,
            "Value": 50,
            "Effects": "Zwiększa magię o <mag> pkt.|Regeneracja magii przyśpieszona o <mag>% przez <dur> s.|"
        },
        {
            "fullName": "Spostrzeżenia Shalidora: Przywołanie",
            "editorId": "MGR21ScrollConjuration",
            "formId": "1076EB",
            "Weight": 0.5,
            "Value": 50,
            "Effects": "Zwiększa czas trwania i zmniejsza koszt zaklęć przywołania przez <dur> s.|"
        }
    ],
    "SLGM": [
        {
            "fullName": "Klejnot duszy Wylandriah",
            "editorId": "FFRiften14SoulGem",
            "formId": "043E26",
            "Weight": 0,
            "Value": 0
        },
        {
            "fullName": "Uzdatniony klejnot duszy",
            "editorId": "WhiterunSoulGem",
            "formId": "094E40",
            "Weight": 0.2,
            "Value": 25
        }
    ],
    "KEYM": [
        {
            "fullName": "Klucz do skonfiskowanych towarów",
            "editorId": "RiftenConfiscatedGoodsChestKey",
            "formId": "10E7E6",
            "Weight": 0,
            "Value": 0
        },
        {
            "fullName": "Klucz do pokoju Malurila",
            "editorId": "MzinchaleftKey01",
            "formId": "10BEFF",
            "Weight": 0,
            "Value": 0
        }
    ],
    "SPEL": [
        {
            "fullName": "Spalenie",
            "editorId": "IncinerateLeftHand",
            "formId": "10FD5F",
            "Effects": "Wybuch ognia zadaje <mag> pkt. obrażeń. Płonące cele ponoszą dodatkowe obrażenia.|||",
            "Spell Mastery": "Ekspert - zniszczenie"
        },
        {
            "fullName": "Płaszcz Płomieni",
            "editorId": "DragonPriestMaskUltraFlameCloak",
            "formId": "10FC17",
            "Effects": "Przez <dur> s zadaje celom w zasięgu broni do walki wręcz pkt. obrażeń od ognia na sekundę.",
            "Spell Mastery": "Czeladnik - zniszczenie"
        }
    ],
    "WOOP": [
        {
            "fullName": "Nus",
            "editorId": "WordNus",
            "formId": "0602A5",
            "Translation": "Posąg"
        },
        {
            "fullName": "Slen",
            "editorId": "WordSlen",
            "formId": "0602A4",
            "Translation": "Ciało"
        }
    ]
}'''

PLUGIN_TEST_ESL_FILE = '''{
    "isEsl": true,
    "WEAP": [
        {
            "fullName": "Stalowy wielki miecz skwaru",
            "editorId": "DA14DremoraGreatswordFire03",
            "formId": "288",
            "Weight": 17,
            "Value": 90,
            "Damage": 17,
            "Type": "Two Handed",
            "Description": "Zadaje celowi <mag> pkt. obrażeń od ognia. Płonące cele odnoszą dodatkowe obrażenia.|"
        },
        {
            "fullName": "Daedryczny wielki miecz inferna",
            "editorId": "EnchDaedricGreatswordDremoraFire06",
            "formId": "009",
            "Weight": 23,
            "Value": 2500,
            "Damage": 24,
            "Type": "Two Handed",
            "Description": ""
        }
    ],
    "ARMO": [
        {
            "fullName": "Buty",
            "editorId": "DremoraBoots",
            "formId": "FFF",
            "Weight": 1,
            "Value": 4,
            "Armor rating": 0,
            "Armor type": "Clothing",
            "Description": ""
        },
        {
            "fullName": "Elfia tarcza wybitnego blokowania",
            "editorId": "EnchArmorElvenShieldBlock04",
            "formId": "C28",
            "Weight": 4,
            "Value": 115,
            "Armor rating": 21,
            "Armor type": "Light Armor",
            "Description": "Tarcza blokuje o <mag>% obrażeń więcej.|"
        }
    ],
    "BOOK": [
        {
            "fullName": "Księga czarów: Przywołanie Władcy Dremor",
            "editorId": "SpellTomeConjureDremoraLord",
            "formId": "D60",
            "Weight": 1,
            "Value": 730
        },
        {
            "fullName": "Księga czarów: Piorun",
            "editorId": "SpellTomeThunderbolt",
            "formId": "7F5",
            "Weight": 1,
            "Value": 750
        }
    ],
    "INGR": [
        {
            "fullName": "Okoń srebrnoboczny",
            "editorId": "CritterPondFish01Ingredient",
            "formId": "E1C",
            "Weight": 0.25,
            "Value": 15,
            "Effects": "Przywrócenie kondycji|Osłabienie regeneracji kondycji|Wyniszczenie zdrowia|Odporność na mróz"
        },
        {
            "fullName": "Abecejski długopłetwiak",
            "editorId": "CritterPondFish02Ingredient",
            "formId": "E1B",
            "Weight": 0.5,
            "Value": 15,
            "Effects": "Podatność na mróz|Premia do skradania|Wrażliwość na trucizny|Premia do przywracania"
        }
    ],
    "ALCH": [
        {
            "fullName": "Miód z owocem jałowca",
            "editorId": "MQ101JuniperMead",
            "formId": "A8A",
            "Weight": 0,
            "Value": 0,
            "Effects": "Przywrócenie kondycji|Osłabienie regeneracji kondycji"
        },
        {
            "fullName": "Miód",
            "editorId": "FoodHoney",
            "formId": "94D",
            "Weight": 0,
            "Value": 0,
            "Effects": "Przywrócenie zdrowia"
        }
    ],
    "MISC": [
        {
            "fullName": "Wypaczony klejnot duszy",
            "editorId": "MGRArniel04SoulGem",
            "formId": "44B",
            "Weight": 0.5,
            "Value": 0
        },
        {
            "fullName": "Posąg Dibelli",
            "editorId": "TG01HaelgaStatuePost",
            "formId": "C6A",
            "Weight": 2,
            "Value": 100
        }
    ],
    "AMMO": [
        {
            "fullName": "Dwemerski bełt",
            "editorId": "DwarvenSphereBolt02",
            "formId": "C8C",
            "Weight": 0,
            "Value": 0,
            "Damage": 15
        },
        {
            "fullName": "Żelazna strzała",
            "editorId": "FollowerIronArrow",
            "formId": "2DE",
            "Weight": 0,
            "Value": 1,
            "Damage": 8
        }
    ],
    "SCRL": [
        {
            "fullName": "Spostrzeżenia Shalidora: Magia",
            "editorId": "MGR21ScrollMagicka",
            "formId": "6EC",
            "Weight": 0.5,
            "Value": 50,
            "Effects": "Zwiększa magię o <mag> pkt.|Regeneracja magii przyśpieszona o <mag>% przez <dur> s.|"
        },
        {
            "fullName": "Spostrzeżenia Shalidora: Przywołanie",
            "editorId": "MGR21ScrollConjuration",
            "formId": "6EB",
            "Weight": 0.5,
            "Value": 50,
            "Effects": "Zwiększa czas trwania i zmniejsza koszt zaklęć przywołania przez <dur> s.|"
        }
    ],
    "SLGM": [
        {
            "fullName": "Klejnot duszy Wylandriah",
            "editorId": "FFRiften14SoulGem",
            "formId": "E26",
            "Weight": 0,
            "Value": 0
        },
        {
            "fullName": "Uzdatniony klejnot duszy",
            "editorId": "WhiterunSoulGem",
            "formId": "E40",
            "Weight": 0.2,
            "Value": 25
        }
    ],
    "KEYM": [
        {
            "fullName": "Klucz do skonfiskowanych towarów",
            "editorId": "RiftenConfiscatedGoodsChestKey",
            "formId": "7E6",
            "Weight": 0,
            "Value": 0
        },
        {
            "fullName": "Klucz do pokoju Malurila",
            "editorId": "MzinchaleftKey01",
            "formId": "EFF",
            "Weight": 0,
            "Value": 0
        }
    ],
    "SPEL": [
        {
            "fullName": "Spalenie",
            "editorId": "IncinerateLeftHand",
            "formId": "D5F",
            "Effects": "Wybuch ognia zadaje <mag> pkt. obrażeń. Płonące cele ponoszą dodatkowe obrażenia.|||",
            "Spell Mastery": "Ekspert - zniszczenie"
        },
        {
            "fullName": "Płaszcz Płomieni",
            "editorId": "DragonPriestMaskUltraFlameCloak",
            "formId": "C17",
            "Effects": "Przez <dur> s zadaje celom w zasięgu broni do walki wręcz pkt. obrażeń od ognia na sekundę.",
            "Spell Mastery": "Czeladnik - zniszczenie"
        }
    ],
    "WOOP": [
        {
            "fullName": "Nus",
            "editorId": "WordNus",
            "formId": "2A5",
            "Translation": "Posąg"
        },
        {
            "fullName": "Slen",
            "editorId": "WordSlen",
            "formId": "2A4",
            "Translation": "Ciało"
        }
    ]
}'''
