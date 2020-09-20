def template_variables(request):
    return {
        "playable_races": ["altmer", "argonian", "bosmer", "breton", "dunmer", "imperial", "khajiit", "nord",
                           "ork", "redguard"],
        "main_categories": ["home", "skills", "items", "spells", "other", "plugins", "commands"],
        "items_categories": ["weapons", "armors", "ammo", "books", "ingredients", "alchemy", "scrolls", "soul gems",
                             "keys", "miscellaneous"],
        "spells_categories": ["alteration", "conjuration", "destruction", "illusion", "restoration", "other"],
        "other_categories": ["variety", "words of power", "perks"],
        "locations": [
            {"location": "", "url": ""},
            {"location": "Whiterun", "url": "https://elderscrolls.fandom.com/wiki/Whiterun_(Skyrim)"},
            {"location": "Solitude", "url": "https://elderscrolls.fandom.com/wiki/Solitude_(Skyrim)"},
            {"location": "Windhelm", "url": "https://elderscrolls.fandom.com/wiki/Windhelm_(Skyrim)"},
            {"location": "Markarth", "url": "https://elderscrolls.fandom.com/wiki/Markarth_(Skyrim)"},
            {"location": "Riften", "url": "https://elderscrolls.fandom.com/wiki/Riften_(Skyrim)"},
            {"location": "Morthal", "url": "https://elderscrolls.fandom.com/wiki/Morthal_(Skyrim)"},
            {"location": "Dawnstar", "url": "https://elderscrolls.fandom.com/wiki/Dawnstar_(Skyrim)"},
            {"location": "Winterhold", "url": "https://elderscrolls.fandom.com/wiki/Winterhold_(Skyrim_City)"},
            {"location": "Falkreath", "url": "https://elderscrolls.fandom.com/wiki/Falkreath_(Skyrim)"},
            {"location": "Riverwood", "url": "https://elderscrolls.fandom.com/wiki/Riverwood_(Skyrim)"},
            {"location": "Dragon Bridge", "url": "https://elderscrolls.fandom.com/wiki/Dragon_Bridge_(Skyrim)"},
            {"location": "Karthwasten", "url": "https://elderscrolls.fandom.com/wiki/Karthwasten_(Skyrim)"},
            {"location": "Ivarstead", "url": "https://elderscrolls.fandom.com/wiki/Ivarstead_(Skyrim)"},
            {"location": "Helgen", "url": "https://elderscrolls.fandom.com/wiki/Helgen"},
            {"location": "Shor's Stone", "url": "https://elderscrolls.fandom.com/wiki/Shor%27s_Stone_(Skyrim)"},
            {"location": "The Atronach Stone", "url": "https://elderscrolls.fandom.com/wiki/The_Atronach_Stone_(Skyrim)"},
            {"location": "The Lady Stone", "url": "https://elderscrolls.fandom.com/wiki/The_Lady_Stone_(Skyrim)"},
            {"location": "The Lord Stone", "url": "https://elderscrolls.fandom.com/wiki/The_Lord_Stone_(Skyrim)"},
            {"location": "The Lover Stone", "url": "https://elderscrolls.fandom.com/wiki/The_Lover_Stone_(Skyrim)"},
            {"location": "The Mage Stone", "url": "https://elderscrolls.fandom.com/wiki/The_Mage_Stone_(Skyrim)"},
            {"location": "The Ritual Stone", "url": "https://elderscrolls.fandom.com/wiki/The_Ritual_Stone_(Skyrim)"},
            {"location": "The Serpent Stone", "url": "https://elderscrolls.fandom.com/wiki/The_Serpent_Stone_(Skyrim)"},
            {"location": "The Shadow Stone", "url": "https://elderscrolls.fandom.com/wiki/The_Shadow_Stone_(Skyrim)"},
            {"location": "The Steed Stone", "url": "https://elderscrolls.fandom.com/wiki/The_Steed_Stone_(Skyrim)"},
            {"location": "The Thief Stone", "url": "https://elderscrolls.fandom.com/wiki/The_Thief_Stone_(Skyrim)"},
            {"location": "The Tower Stone", "url": "https://elderscrolls.fandom.com/wiki/The_Tower_Stone_(Skyrim)"},
            {"location": "The Warrior Stone", "url": "https://elderscrolls.fandom.com/wiki/The_Warrior_Stone_(Skyrim)"},
            {"location": "The Apprentice Stone", "url": "https://elderscrolls.fandom.com/wiki/The_Apprentice_Stone_(Skyrim)"},
            {"location": "Rorikstead", "url": "https://elderscrolls.fandom.com/wiki/Rorikstead"},
            {"location": "Eldergleam Sanctuary", "url": "https://elderscrolls.fandom.com/wiki/Eldergleam_Sanctuary"},
            {"location": "Mixwater Mill", "url": "https://elderscrolls.fandom.com/wiki/Mixwater_Mill"},
            {"location": "Mzulft", "url": "https://elderscrolls.fandom.com/wiki/Mzulft_(Skyrim)"},
            {"location": "Sacellum of Boethiah", "url": "https://elderscrolls.fandom.com/wiki/Sacellum_of_Boethiah"},
            {"location": "Darkwater Crossing", "url": "https://elderscrolls.fandom.com/wiki/Darkwater_Crossing_(Skyrim)"},
            {"location": "Kynesgrove", "url": "https://elderscrolls.fandom.com/wiki/Kynesgrove_(Skyrim)"},
            {"location": "Narzulbur", "url": "https://elderscrolls.fandom.com/wiki/Narzulbur"},
            {"location": "Lakeview Manor", "url": "https://elderscrolls.fandom.com/wiki/Lakeview_Manor"},
            {"location": "Forgotten Vale", "url": "https://elderscrolls.fandom.com/wiki/Forgotten_Vale"},
            {"location": "Mor Khazgur", "url": "https://elderscrolls.fandom.com/wiki/Mor_Khazgur_(Skyrim)"},
            {"location": "Stonehills", "url": "https://elderscrolls.fandom.com/wiki/Stonehills_(Skyrim)"},
            {"location": "Raven Rock", "url": "https://elderscrolls.fandom.com/wiki/Raven_Rock_(Dragonborn)"},
            {"location": "Skaal Village", "url": "https://elderscrolls.fandom.com/wiki/Skaal_Village_(Dragonborn)"},
            {"location": "Soul Cairn", "url": "https://elderscrolls.fandom.com/wiki/Soul_Cairn_(Dawnguard)"},
            {"location": "Sovngarde", "url": "https://elderscrolls.fandom.com/wiki/Sovngarde_(Location)"},
            {"location": "Blackreach", "url": "https://elderscrolls.fandom.com/wiki/Blackreach_(Skyrim)"},
            {"location": "Anga's Mill", "url": "https://elderscrolls.fandom.com/wiki/Anga%27s_Mill"},
            {"location": "Dushnikh Yal", "url": "https://elderscrolls.fandom.com/wiki/Dushnikh_Yal"},
            {"location": "Largashbur", "url": "https://elderscrolls.fandom.com/wiki/Largashbur"},
        ]
    }


ADD_PLUGIN_SUCCESS_MESSAGE = "Plugin was successfully added to database."

ADD_PLUGIN_ERROR_FILE = "File was incorrect!"

ADD_PLUGIN_ERROR_PLUGIN_EXIST = "Plugin with this Name, Version and Language already exists."

COMMANDS_SUCCESS_MESSAGE = "Commands are ready on the Commands page."

ITEMS_COMMANDS_POST_EMPTY_MESSAGE = "No items selected!"

SPELLS_COMMANDS_POST_EMPTY_MESSAGE = "No spells selected!"

OTHER_COMMANDS_POST_EMTPY_MESSAGE = "Nothing was chosen!"

INCORRECT_LOAD_ORDER = "Load order need to be hex number between 00 and FF for esp files and from FE001 to "\
                       "FEFFF for esl files!"

SELECTED_PLUGINS_SUCCESS = "Plugins have been successfully selected."

NO_PLUGIN_SELECTED = "No plugin selected!"

PLUGINS_ERROR_NAME_IS_EMTPY = "Name cannot be empty!"

PLUGINS_ERROR_NAME_BECOME_EMPTY = "Name cannot consist only from special signs!"

NO_PLUGIN_SELECTED_ERROR_MESSAGE = "Please select plugin before use Items or Spells."

SKILLS_ERROR_NEW_VALUE_BIGGER = "New value of {skill} must be bigger than a value!"

SKILLS_ERROR_DESIRED_LEVEL_RANGE = "Desired level need to be a integer between 1 and 81."

SKILLS_ERROR_DESIRED_LEVEL = "Desired level need to be integer!"

SKILLS_ERROR_MULTIPLIER = "Priority multiplier need to be number!"

SKILLS_ERROR_BASE_SKILL = "Skill {skill} need to be a integer between 15 and 100!"

SKILLS_ERROR_DESIRED_SKILL = "Desired skill {skill} need to be a integer between 15 and 100 or empty!"

SKILLS_CONSOLE_NAME = [
    'alteration', 'conjuration', 'destruction', 'enchanting',
    'illusion', 'restoration', 'marksman', 'block', 'heavyarmor',
    'onehanded', 'smithing', 'twohanded', 'alchemy', 'lightarmor',
    'lockpicking', 'pickpocket', 'sneak', 'speechcraft'
]

DEFAULT_SKILL_POST = {
    'alteration_base': "15",
    'conjuration_base': "15",
    'destruction_base': "15",
    'enchanting_base': "15",
    'illusion_base': "15",
    'restoration_base': "15",
    'marksman_base': "15",
    'block_base': "15",
    'heavyarmor_base': "15",
    'onehanded_base': "15",
    'smithing_base': "15",
    'twohanded_base': "15",
    'alchemy_base': "15",
    'lightarmor_base': "15",
    'lockpicking_base': "15",
    'pickpocket_base': "15",
    'sneak_base': "15",
    'speechcraft_base': "15",
    'alteration_new': "",
    'conjuration_new': "",
    'destruction_new': "",
    'enchanting_new': "",
    'illusion_new': "",
    'restoration_new': "",
    'marksman_new': "",
    'block_new': "",
    'heavyarmor_new': "",
    'onehanded_new': "",
    'smithing_new': "",
    'twohanded_new': "",
    'alchemy_new': "",
    'lightarmor_new': "",
    'lockpicking_new': "",
    'pickpocket_new': "",
    'sneak_new': "",
    'speechcraft_new': "",
}

DEFAULT_SKILLS = {
    "Magic": {
        "alteration": {
            "name": "Alteration",
            "console_name": "alteration",
            "default_value": 15,
            "desired_value": "",
            "multiplier": False,
            "sim": 2,
            "sio": 0,
            "sum": 3,
        },
        "conjuration":  {
            "name": "Conjuration",
            "console_name": "conjuration",
            "default_value": 15,
            "desired_value": "",
            "multiplier": False,
            "sim": 2,
            "sio": 0,
            "sum": 2.1,
        },
        "destruction":  {
            "name": "Destruction",
            "console_name": "destruction",
            "default_value": 15,
            "desired_value": "",
            "multiplier": False,
            "sim": 2,
            "sio": 0,
            "sum": 1.35,
        },
        "enchanting":  {
            "name": "Enchanting",
            "console_name": "enchanting",
            "default_value": 15,
            "desired_value": "",
            "multiplier": False,
            "sim": 1,
            "sio": 170,
            "sum": 900,
        },
        "illusion":  {
            "name": "Illusion",
            "console_name": "illusion",
            "default_value": 15,
            "desired_value": "",
            "multiplier": False,
            "sim": 2,
            "sio": 0,
            "sum": 4.6,
        },
        "restoration":  {
            "name": "Restoration",
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
        "marksman":  {
            "name": "Archery",
            "console_name": "marksman",
            "default_value": 15,
            "desired_value": "",
            "multiplier": False,
            "sim": 2,
            "sio": 0,
            "sum": 9.3,
        },
        "block":  {
            "name": "Block",
            "console_name": "block",
            "default_value": 15,
            "desired_value": "",
            "multiplier": False,
            "sim": 2,
            "sio": 0,
            "sum": 8.1,
        },
        "heavyarmor":  {
            "name": "Heavy Armor",
            "console_name": "heavyarmor",
            "default_value": 15,
            "desired_value": "",
            "multiplier": False,
            "sim": 2,
            "sio": 0,
            "sum": 3.8,
        },
        "onehanded":  {
            "name": "One-handed",
            "console_name": "onehanded",
            "default_value": 15,
            "desired_value": "",
            "multiplier": False,
            "sim": 2,
            "sio": 0,
            "sum": 6.3,
        },
        "smithing":  {
            "name": "Smithing",
            "console_name": "smithing",
            "default_value": 15,
            "desired_value": "",
            "multiplier": False,
            "sim": 0.25,
            "sio": 300,
            "sum": 1,
        },
        "twohanded":  {
            "name": "Two-handed",
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
        "alchemy":  {
            "name": "Alchemy",
            "console_name": "alchemy",
            "default_value": 15,
            "desired_value": "",
            "multiplier": False,
            "sim": 1.6,
            "sio": 65,
            "sum": 0.75,
        },
        "lightarmor":  {
            "name": "Light Armor",
            "console_name": "lightarmor",
            "default_value": 15,
            "desired_value": "",
            "multiplier": False,
            "sim": 2,
            "sio": 0,
            "sum": 4,
        },
        "lockpicking":  {
            "name": "Lockpicking",
            "console_name": "lockpicking",
            "default_value": 15,
            "desired_value": "",
            "multiplier": False,
            "sim": 0.25,
            "sio": 300,
            "sum": 45,
        },
        "pickpocket":  {
            "name": "Pickpocket",
            "console_name": "pickpocket",
            "default_value": 15,
            "desired_value": "",
            "multiplier": False,
            "sim": 0.25,
            "sio": 250,
            "sum": 8.1,
        },
        "sneak":  {
            "name": "Sneak",
            "console_name": "sneak",
            "default_value": 15,
            "desired_value": "",
            "multiplier": False,
            "sim": 0.5,
            "sio": 120,
            "sum": 11.25,
        },
        "speechcraft":  {
            "name": "Speech",
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
    "altmer": {
        10: {"Magic": "illusion"},
        5: {"Magic": ["alteration", "conjuration", "destruction",
                      "enchanting", "restoration"]},
    },
    "argonian": {
        10: {"Stealth": "lockpicking"},
        5: {"Magic": ["alteration", "restoration"],
            "Stealth": ["lightarmor", "pickpocket", "sneak"]},
    },
    "bosmer": {
        10: {"Combat": "marksman"},
        5: {"Stealth": ["alchemy", "lightarmor", "lockpicking",
                        "pickpocket", "sneak"]},
    },
    "breton": {
        10: {"Magic": "conjuration"},
        5: {"Magic": ["alteration", "illusion", "restoration"],
            "Stealth": ["alchemy", "speechcraft"]},
    },
    "dunmer": {
        10: {"Magic": "destruction"},
        5: {"Magic": ["alteration", "illusion"],
            "Stealth": ["alchemy", "light Armor", "sneak"]},
    },
    "imperial": {
        10: {"Magic": "restoration"},
        5: {"Magic": ["destruction", "enchanting"],
            "Combat": ["block", "heavyarmor", "onehanded"]},
    },
    "khajiit": {
        10: {"Stealth": "sneak"},
        5: {"Stealth": ["alchemy", "lockpicking", "pickpocket"],
            "Combat": ["marksman", "onehanded"]},
    },
    "nord": {
        10: {"Combat": "twohanded"},
        5: {"Stealth": ["speechcraft", "lightarmor"],
            "Combat": ["block", "onehanded", "smithing"]},
    },
    "ork": {
        10: {"Combat": "heavyarmor"},
        5: {"Combat": ["block", "onehanded", "smithing", "twohanded"],
            "Magic": ["enchanting"]},
    },
    "redguard": {
        10: {"Combat": "onehanded"},
        5: {"Combat": ["marksman", "block", "smithing"],
            "Magic": ["alteration", "destruction"]},
    },
}

PLUGIN_TEST_EMPTY_DICT = {
    "isEsl": False,
    "WEAP": [],
    "ARMO": [],
    "BOOK": [],
    "INGR": [],
    "ALCH": [],
    "MISC": [],
    "AMMO": [],
    "SCRL": [],
    "SLGM": [],
    "KEYM": [],
    "SPEL": [],
    "WOOP": [],
    "PERK": [],
}

PLUGIN_TEST_EMPTY_DATA = '''{
    "isEsl": false
}'''

PLUGIN_TEST_ESCAPE_FILE = '''{    
    "isEsl": false,
    "WEAP": [
        {
            "fullName": "<strong>Stalowy</strong> wielki miecz skwaru",
            "editorId": "&DA14DremoraGreatswordFire03",
            "formId": "017288",
            "Weight": 17,
            "Value": 90,
            "Damage": 17,
            "Type": "Two Handed",
            "Description": "Zadaje celowi <mag> pkt. obrażeń od ognia. Płonące cele odnoszą dodatkowe obrażenia.|"
        }
    ],
    "ARMO": [],
    "BOOK": [],
    "INGR": [],
    "ALCH": [],
    "MISC": [],
    "AMMO": [],
    "SCRL": [],
    "SLGM": [],
    "KEYM": [],
    "SPEL": [],
    "WOOP": [],
    "PERK": []
}'''

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
            "fullName": "Alternation Spell",
            "editorId": "DragonPriest",
            "formId": "000001",
            "Effects": "obrażeń od ognia na sekundę.",
            "Category": "Alteration",
            "Mastery": "Expert"
        },
        {
            "fullName": "Destruction Spell",
            "editorId": "IncinerateLeftHand",
            "formId": "10FD5F",
            "Effects": "Wybuch ognia zadaje <mag> pkt. obrażeń. Płonące cele ponoszą dodatkowe obrażenia.|||",
            "Category": "Destruction",
            "Mastery": "Adept"
        },
        {
            "fullName": "Conjuration Spell",
            "editorId": "SomeId",
            "formId": "000002",
            "Effects": "obrażeń od lodu na sekundę.",
            "Category": "Conjuration",
            "Mastery": "Expert"
        },
        {
            "fullName": "Illusion Spell",
            "editorId": "Priest",
            "formId": "000003",
            "Effects": "obrażeń sekundę.",
            "Category": "Illusion",
            "Mastery": "Expert"
        },
        {
            "fullName": "Restoration Spell",
            "editorId": "Dragon",
            "formId": "000004",
            "Effects": "od ognia na sekundę.",
            "Category": "Restoration",
            "Mastery": "Expert"
        },
        {
            "fullName": "Other Spell",
            "editorId": "OtherId",
            "formId": "000005",
            "Effects": "sekundę.",
            "Category": "",
            "Mastery": ""
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
    ],
    "PERK": [
        {
          "fullName": "Dopasowane blachy",
          "editorId": "DBWellFitted",
          "formId": "01711C",
          "Description": "Premia +25 do pancerza, jeśli nosisz całą zbroję mroku."
        },
        {
          "fullName": "Przeszywające pioruny",
          "editorId": "AugmentedShock60",
          "formId": "10FCFA",
          "Description": "Czary porażeniowe zadają obrażenia większe o 50%."
        }
    ]
}

PLUGIN_TEST_DICT_ALTERED_BY_FORM = {
    "WEAP": [
        {
            "name": "Stalowy wielki miecz skwaru",
            "editor_id": "DA14DremoraGreatswordFire03",
            "form_id": "017288",
            "weight": "17",
            "value": "90",
            "damage": "17",
            "type": "Two Handed",
            "description": "Zadaje celowi &lt;mag&gt; pkt. obrażeń od ognia. Płonące cele odnoszą dodatkowe obrażenia.|"
        },
        {
            "name": "Daedryczny wielki miecz inferna",
            "editor_id": "EnchDaedricGreatswordDremoraFire06",
            "form_id": "017009",
            "weight": "23",
            "value": "2500",
            "damage": "24",
            "type": "Two Handed",
            "description": ""
        }
    ],
    "ARMO": [
        {
            "name": "Buty",
            "editor_id": "DremoraBoots",
            "form_id": "016FFF",
            "weight": "1",
            "value": "4",
            "armor_rating": "0",
            "armor_type": "Clothing",
            "description": ""
        },
        {
            "name": "Elfia tarcza wybitnego blokowania",
            "editor_id": "EnchArmorElvenShieldBlock04",
            "form_id": "10FC28",
            "weight": "4",
            "value": "115",
            "armor_rating": "21",
            "armor_type": "Light Armor",
            "description": "Tarcza blokuje o &lt;mag&gt;% obrażeń więcej.|"
        }
    ],
    "BOOK": [
        {
            "name": "Księga czarów: Przywołanie Władcy Dremor",
            "editor_id": "SpellTomeConjureDremoraLord",
            "form_id": "10FD60",
            "weight": "1",
            "value": "730"
        },
        {
            "name": "Księga czarów: Piorun",
            "editor_id": "SpellTomeThunderbolt",
            "form_id": "10F7F5",
            "weight": "1",
            "value": "750"
        }
    ],
    "INGR": [
        {
            "name": "Okoń srebrnoboczny",
            "editor_id": "CritterPondFish01Ingredient",
            "form_id": "106E1C",
            "weight": "0.25",
            "value": "15",
            "effects": "Przywrócenie kondycji|Osłabienie regeneracji kondycji|Wyniszczenie zdrowia|Odporność na mróz"
        },
        {
            "name": "Abecejski długopłetwiak",
            "editor_id": "CritterPondFish02Ingredient",
            "form_id": "106E1B",
            "weight": "0.5",
            "value": "15",
            "effects": "Podatność na mróz|Premia do skradania|Wrażliwość na trucizny|Premia do przywracania"
        }
    ],
    "ALCH": [
        {
            "name": "Miód z owocem jałowca",
            "editor_id": "MQ101JuniperMead",
            "form_id": "107A8A",
            "weight": "0",
            "value": "0",
            "effects": "Przywrócenie kondycji|Osłabienie regeneracji kondycji"
        },
        {
            "name": "Miód",
            "editor_id": "FoodHoney",
            "form_id": "10394D",
            "weight": "0",
            "value": "0",
            "effects": "Przywrócenie zdrowia"
        }
    ],
    "MISC": [
        {
            "name": "Wypaczony klejnot duszy",
            "editor_id": "MGRArniel04SoulGem",
            "form_id": "10E44B",
            "weight": "0.5",
            "value": "0"
        },
        {
            "name": "Posąg Dibelli",
            "editor_id": "TG01HaelgaStatuePost",
            "form_id": "10CC6A",
            "weight": "2",
            "value": "100"
        }
    ],
    "AMMO": [
        {
            "name": "Dwemerski bełt",
            "editor_id": "DwarvenSphereBolt02",
            "form_id": "10EC8C",
            "weight": "0",
            "value": "0",
            "damage": "15"
        },
        {
            "name": "Żelazna strzała",
            "editor_id": "FollowerIronArrow",
            "form_id": "10E2DE",
            "weight": "0",
            "value": "1",
            "damage": "8"
        }
    ],
    "SCRL": [
        {
            "name": "Spostrzeżenia Shalidora: Magia",
            "editor_id": "MGR21ScrollMagicka",
            "form_id": "1076EC",
            "weight": "0.5",
            "value": "50",
            "effects": "Zwiększa magię o &lt;mag&gt; pkt.|Regeneracja magii przyśpieszona o"
                       " &lt;mag&gt;% przez &lt;dur&gt; s.|"
        },
        {
            "name": "Spostrzeżenia Shalidora: Przywołanie",
            "editor_id": "MGR21ScrollConjuration",
            "form_id": "1076EB",
            "weight": "0.5",
            "value": "50",
            "effects": "Zwiększa czas trwania i zmniejsza koszt zaklęć przywołania przez &lt;dur&gt; s.|"
        }
    ],
    "SLGM": [
        {
            "name": "Klejnot duszy Wylandriah",
            "editor_id": "FFRiften14SoulGem",
            "form_id": "043E26",
            "weight": "0",
            "value": "0"
        },
        {
            "name": "Uzdatniony klejnot duszy",
            "editor_id": "WhiterunSoulGem",
            "form_id": "094E40",
            "weight": "0.2",
            "value": "25"
        }
    ],
    "KEYM": [
        {
            "name": "Klucz do skonfiskowanych towarów",
            "editor_id": "RiftenConfiscatedGoodsChestKey",
            "form_id": "10E7E6",
            "weight": "0",
            "value": "0"
        },
        {
            "name": "Klucz do pokoju Malurila",
            "editor_id": "MzinchaleftKey01",
            "form_id": "10BEFF",
            "weight": "0",
            "value": "0"
        }
    ],

    "SPEL": [
        {
            "name": "Alternation Spell",
            "editor_id": "DragonPriest",
            "form_id": "000001",
            "effects": "obrażeń od ognia na sekundę.",
            "mastery": "Expert"
        },
        {
            "name": "Destruction Spell",
            "editor_id": "IncinerateLeftHand",
            "form_id": "10FD5F",
            "effects": "Wybuch ognia zadaje &lt;mag&gt; pkt. obrażeń. Płonące cele ponoszą dodatkowe obrażenia.|||",
            "mastery": "Adept"
        },
        {
            "name": "Conjuration Spell",
            "editor_id": "SomeId",
            "form_id": "000002",
            "effects": "obrażeń od lodu na sekundę.",
            "mastery": "Expert"
        },
        {
            "name": "Illusion Spell",
            "editor_id": "Priest",
            "form_id": "000003",
            "effects": "obrażeń sekundę.",
            "mastery": "Expert"
        },
        {
            "name": "Restoration Spell",
            "editor_id": "Dragon",
            "form_id": "000004",
            "effects": "od ognia na sekundę.",
            "mastery": "Expert"
        },
        {
            "name": "Other Spell",
            "editor_id": "OtherId",
            "form_id": "000005",
            "effects": "sekundę.",
            "mastery": ""
        }
    ],
    "WOOP": [
        {
            "word": "Nus",
            "editor_id": "WordNus",
            "form_id": "0602A5",
            "translation": "Posąg"
        },
        {
            "word": "Slen",
            "editor_id": "WordSlen",
            "form_id": "0602A4",
            "translation": "Ciało"
        }
    ],
    "PERK": [
        {
          "name": "Dopasowane blachy",
          "editor_id": "DBWellFitted",
          "form_id": "01711C",
          "description": "Premia +25 do pancerza, jeśli nosisz całą zbroję mroku."
        },
        {
          "name": "Przeszywające pioruny",
          "editor_id": "AugmentedShock60",
          "form_id": "10FCFA",
          "description": "Czary porażeniowe zadają obrażenia większe o 50%."
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
            "fullName": "Alternation Spell",
            "editorId": "DragonPriest",
            "formId": "000001",
            "Effects": "obrażeń od ognia na sekundę.",
            "Category": "Alteration",
            "Mastery": "Expert"
        },
        {
            "fullName": "Destruction Spell",
            "editorId": "IncinerateLeftHand",
            "formId": "10FD5F",
            "Effects": "Wybuch ognia zadaje <mag> pkt. obrażeń. Płonące cele ponoszą dodatkowe obrażenia.|||",
            "Category": "Destruction",
            "Mastery": "Adept"
        },
        {
            "fullName": "Conjuration Spell",
            "editorId": "SomeId",
            "formId": "000002",
            "Effects": "obrażeń od lodu na sekundę.",
            "Category": "Conjuration",
            "Mastery": "Expert"
        },
        {
            "fullName": "Illusion Spell",
            "editorId": "Priest",
            "formId": "000003",
            "Effects": "obrażeń sekundę.",
            "Category": "Illusion",
            "Mastery": "Expert"
        },
        {
            "fullName": "Restoration Spell",
            "editorId": "Dragon",
            "formId": "000004",
            "Effects": "od ognia na sekundę.",
            "Category": "Restoration",
            "Mastery": "Expert"
        },
        {
            "fullName": "Other Spell",
            "editorId": "OtherId",
            "formId": "000005",
            "Effects": "sekundę.",
            "Category": "",
            "Mastery": ""
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
    ],
    "PERK": [
        {
          "fullName": "Dopasowane blachy",
          "editorId": "DBWellFitted",
          "formId": "01711C",
          "Description": "Premia +25 do pancerza, jeśli nosisz całą zbroję mroku."
        },
        {
          "fullName": "Przeszywające pioruny",
          "editorId": "AugmentedShock60",
          "formId": "10FCFA",
          "Description": "Czary porażeniowe zadają obrażenia większe o 50%."
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
            "fullName": "Alternation Spell",
            "editorId": "DragonPriest",
            "formId": "000001",
            "Effects": "obrażeń od ognia na sekundę.",
            "Category": "Alteration",
            "Mastery": "Expert"
        },
        {
            "fullName": "Destruction Spell",
            "editorId": "IncinerateLeftHand",
            "formId": "10FD5F",
            "Effects": "Wybuch ognia zadaje <mag> pkt. obrażeń. Płonące cele ponoszą dodatkowe obrażenia.|||",
            "Category": "Destruction",
            "Mastery": "Adept"
        },
        {
            "fullName": "Conjuration Spell",
            "editorId": "SomeId",
            "formId": "000002",
            "Effects": "obrażeń od lodu na sekundę.",
            "Category": "Conjuration",
            "Mastery": "Expert"
        },
        {
            "fullName": "Illusion Spell",
            "editorId": "Priest",
            "formId": "000003",
            "Effects": "obrażeń sekundę.",
            "Category": "Illusion",
            "Mastery": "Expert"
        },
        {
            "fullName": "Restoration Spell",
            "editorId": "Dragon",
            "formId": "000004",
            "Effects": "od ognia na sekundę.",
            "Category": "Restoration",
            "Mastery": "Expert"
        },
        {
            "fullName": "Other Spell",
            "editorId": "OtherId",
            "formId": "000005",
            "Effects": "sekundę.",
            "Category": "",
            "Mastery": ""
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
    ],
    "PERK": [
        {
          "fullName": "Dopasowane blachy",
          "editorId": "DBWellFitted",
          "formId": "01711C",
          "Description": "Premia +25 do pancerza, jeśli nosisz całą zbroję mroku."
        },
        {
          "fullName": "Przeszywające pioruny",
          "editorId": "AugmentedShock60",
          "formId": "10FCFA",
          "Description": "Czary porażeniowe zadają obrażenia większe o 50%."
        }
    ]
}'''
