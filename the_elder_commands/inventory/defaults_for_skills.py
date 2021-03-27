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