class Commands:
    def __init__(self, request):
        self.request = request
        self._skills_key = "skills_commands"
        self._items_key = "items_commands"
        self._spells_key = "spells_commands"
        self._other_key = "other_commands"

    def set_skills(self, commands):
        self.request.session.update({self._skills_key: commands})

    def set_items(self, items):
        commands = []
        for form_id, quantity in items.items():
            commands.append(f"player.additem {form_id} {quantity}")
        self.request.session.update({self._items_key: commands})

    def set_spells(self, spells):
        commands = []
        for form_id in spells.keys():
            commands.append(f"player.addspell {form_id}")
        self.request.session.update({self._spells_key: commands})

    def set_other(self, various):
        commands = []
        commands += self._prepare_variety_commands(various)
        commands += self._prepare_words_of_power_commands(various)
        commands += self._prepare_perks_commands(various)
        commands += self._prepare_location_commands(various)
        self.request.session.update({self._other_key: commands})

    @staticmethod
    def _prepare_variety_commands(various):
        commands = []
        if various.get("gold"):
            commands.append(f"player.additem 0000000F {various.get('gold')}")
        if various.get("dragon_souls"):
            commands.append(f"player.modav dragonsouls {various.get('dragon_souls')}")
        if various.get("health"):
            commands.append(f"player.modav health {various.get('health')}")
        if various.get("magicka"):
            commands.append(f"player.modav magicka {various.get('magicka')}")
        if various.get("stamina"):
            commands.append(f"player.modav stamina {various.get('stamina')}")
        if various.get("carry_weight"):
            commands.append(f"player.modav carryweight {various.get('carry_weight')}")
        if various.get("movement_speed"):
            commands.append(f"player.setav speedmult {various.get('movement_speed')}")
        return commands

    @staticmethod
    def _prepare_location_commands(various):
        location = various.get("location")
        locations_ids = {
            "Whiterun": "Whiterun",
            "Eldergleam Sanctuary": "EldergleamSanctuaryExterior",
            "Solitude": "Solitude",
            "Windhelm": "Windhelm",
            "Markarth": "MarkarthOrigin",
            "Riften": "RiftenOrigin",
            "Morthal": "MorthalExterior01",
            "Dawnstar": "DawnstarExterior01",
            "Winterhold": "WinterholdExterior01",
            "Falkreath": "FalkreathExterior01",
            "Riverwood": "Riverwood",
            "Dragon Bridge": "DragonBridgeExterior01",
            "Karthwasten": "KarthwastenExterior01",
            "Ivarstead": "IvarsteadExterior01",
            "Helgen": "HelgenExterior",
            "Shor's Stone": "ShorsStoneExterior01",
            "The Atronach Stone": "DoomstoneVolcanicTundra",
            "The Lady Stone": "DoomstonePineForest01",
            "The Lord Stone": "DoomstoneSnowy02",
            "The Lover Stone": "DoomstoneReach01",
            "The Mage Stone": "GuardianStones",
            "The Ritual Stone": "DoomstoneTundra01",
            "The Serpent Stone": "DoomstoneNorthernCoast01",
            "The Shadow Stone": "DoomstoneFallForest01",
            "The Steed Stone": "DoomstoneNorthernPineForest01",
            "The Thief Stone": "GuardianStones",
            "The Tower Stone": "DoomstoneSnowy01",
            "The Warrior Stone": "GuardianStones",
            "The Apprentice Stone": "DoomstoneTundraMarsh01",
            "Rorikstead": "RoriksteadExterior01",
            "Mixwater Mill": "MixwaterMillExterior",
            "Mzulft": "Mzulft01",
            "Sacellum of Boethiah": "DA02BoethiahShrine",
            "Darkwater Crossing": "DarkwaterCrossingExterior01",
            "Kynesgrove": "Kynesgrove",
            "Narzulbur": "Narzulburexterior01",
            "Lakeview Manor": "BYOHHouse1Exterior",
            "Forgotten Vale": "FalmerValleyStart",
            "Mor Khazgur": "MorKhazgurExterior",
            "Stonehills": "StonehillsExterior01",
            "Raven Rock": "DLC2RavenRock01",
            "Skaal Village": "DLC2SkaalVillage01",
            "Soul Cairn": "DLC01SoulCairnOrigin",
            "Sovngarde": "Sovngarde01",
            "Blackreach": "BlackreachCity",
            "Anga's Mill": "AngasMill",
            "Dushnikh Yal": "DushnikhYalExterior01",
            "Largashbur": "LargashburExterior01",
        }
        if location:
            return [f"coc {locations_ids.get(location)}"]
        return []

    @staticmethod
    def _prepare_words_of_power_commands(various):
        words = [word[4:] for word in various.keys() if word[:4] == "word"]
        commands = [f"player.teachword {word}" for word in words]
        return commands

    @staticmethod
    def _prepare_perks_commands(various):
        perks = [perk[4:] for perk in various.keys() if perk[:4] == "perk"]
        commands = [f"player.addperk {perk}" for perk in perks]
        return commands

    def get_commands(self):
        commands = []
        commands += self.request.session.get(self._skills_key, [])
        commands += self.request.session.get(self._items_key, [])
        commands += self.request.session.get(self._spells_key, [])
        commands += self.request.session.get(self._other_key, [])
        return commands