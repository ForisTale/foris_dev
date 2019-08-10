

PLAYABLE_RACES = [
    ["Altmer", "altmer_race"], ["Argonian", "argonian_race"],
    ["Bosmer", "bosmer_race"], ["Breton", "breton_race"],
    ["Dunmer", "dunmer_race"], ["Imperial", "imperial_race"],
    ["Khajiit", "khajiit_race"], ["Nord", "nord_race"],
    ["Ork", "ork_race"], ["Redguard", "redguard_race"],
]

SKILLS_CONSOLE_NAME = [
    'alteration', 'conjuration', 'destruction', 'enchanting',
    'illusion', 'restoration', 'marksman', 'block', 'heavyarmor',
    'onehanded', 'smithing', 'twohanded', 'alchemy', 'lightarmor',
    'lockpicking', 'pickpocket', 'sneak', 'speechcraft'
]

DEFAULT_SKILLS = {
    "Magic": {
        "Alteration": {"console_name": "alteration", "value": 15},
        "Conjuration":  {"console_name": "conjuration", "value": 15},
        "Destruction":  {"console_name": "destruction", "value": 15},
        "Enchanting":  {"console_name": "enchanting", "value": 15},
        "Illusion":  {"console_name": "illusion", "value": 15},
        "Restoration":  {"console_name": "restoration", "value": 15},
    },
    "Combat": {
        "Archery":  {"console_name": "marksman", "value": 15},
        "Block":  {"console_name": "block", "value": 15},
        "Heavy Armor":  {"console_name": "heavyarmor", "value": 15},
        "One-handed":  {"console_name": "onehanded", "value": 15},
        "Smithing":  {"console_name": "smithing", "value": 15},
        "Two-handed":  {"console_name": "twohanded", "value": 15},
    },
    "Stealth": {
        "Alchemy":  {"console_name": "alchemy", "value": 15},
        "Light Armor":  {"console_name": "lightarmor", "value": 15},
        "Lockpicking":  {"console_name": "lockpicking", "value": 15},
        "Pickpocket":  {"console_name": "pickpocket", "value": 15},
        "Sneak":  {"console_name": "sneak", "value": 15},
        "Speech":  {"console_name": "speechcraft", "value": 15},
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

