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