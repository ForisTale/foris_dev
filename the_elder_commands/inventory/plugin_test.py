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