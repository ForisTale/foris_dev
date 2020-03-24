

def template_variables(request):
    return {
        "playable_races": [
            ["Altmer", "altmer_race"], ["Argonian", "argonian_race"],
            ["Bosmer", "bosmer_race"], ["Breton", "breton_race"],
            ["Dunmer", "dunmer_race"], ["Imperial", "imperial_race"],
            ["Khajiit", "khajiit_race"], ["Nord", "nord_race"],
            ["Ork", "ork_race"], ["Redguard", "redguard_race"],
        ],
    }


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

