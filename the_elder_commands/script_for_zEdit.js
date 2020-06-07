//SLGM - soul gems
const itemsSignatures = ["WEAP", "ARMO", "BOOK", "INGR", "ALCH",
                         "MISC", "AMMO", "SCRL", "SLGM", "KEYM"],
    magicSignatures = ["SPEL", "WOOP", "PERK"];
let pluginName,
    isEsl,
    skyrimAndDlc = ["Skyrim", "Dawnguard", "Dragonborn", "HearthFires"];


function processSelectedPlugins(){
    for (let selectedPlugin of zedit.GetSelectedNodes()) {
        const selectedPluginHandle = selectedPlugin.handle,
            signatures = itemsSignatures.concat(magicSignatures);
        pluginName = selectedPlugin.column_values[0].slice(5, -4);
        let file = xelib.GetElement(0, selectedPlugin.column_values[0].slice(5)),
        fileHeader = xelib.GetElement(file, "File Header");

        isEsl = xelib.GetRecordFlag(fileHeader, "ESL");

        fh.saveJsonFile(fh.jetpack.cwd() + "\\The_Elder_Commands\\" + pluginName + ".tec",
            getSignaturesData(signatures, selectedPluginHandle),
            false);
    }
}

function getSignaturesData(signatures, pluginHandle) {
    let itemsData = {};

    for (let category of signatures){
        const records = xelib.GetRecords(pluginHandle, category);
        itemsData[category] = processRecords(records);
    }
    itemsData["isEsl"] = isEsl
    return itemsData;
}

function processRecords(records) {
    let fullData = [];

    for (let record of records) {
        if ( hasFullName(record) ) {
            const data = assembleData(record);
            if (Object.keys(data).length !== 0) fullData.push(data);
        }
    }

    return fullData;
}

function hasFullName(record) {
    const fullName = xelib.FullName(record);
    return fullName !== "";
}

function assembleData(record){
    if (skyrimAndDlc.includes(pluginName)) {
        if (xelib.Signature(record) === "SPEL")
            if (xelib.GetValue(record, "SPIT - Data\\Half-cost Perk").includes("NULL")) {
            return {};
        }
        if (xelib.Signature(record) === "WOOP")
            if (xelib.GetValue(record, "TNAM - Translation") === "") {
                return {};
            }
    }


    return {...getCommonData(record), ...getItemCommonData(record), ...getSpecifyData(record)};
}

function getCommonData(record){
    const editorId = xelib.EditorID(record),
        formId = getFormId(record),
        fullName = xelib.FullName(record);

    return {"fullName":fullName, "editorId": editorId, "formId": formId};
}

function getFormId(record){
    if (isEsl)
        return xelib.GetHexFormID(record).slice(5);
    else
        return xelib.GetHexFormID(record).slice(2);
}

function getItemCommonData(record) {
    if (itsItem(record)) {
        let itemWeight = xelib.GetWeight(record),
            itemValue = xelib.GetGoldValue(record);
        if (isNaN(itemWeight)) itemWeight = 0;
        if (isNaN(itemValue)) itemValue = 0;

        return {"Weight": itemWeight, "Value": itemValue};
    }
    else return {};
}

function itsItem(record) {
    return itemsSignatures.includes(xelib.Signature(record));
}

function getSpecifyData(record){
    switch ( xelib.Signature(record) ) {
        case "WEAP":
            return getWeaponData(record);
        case "ARMO":
            return getArmorData(record);
        case "INGR":
            return {"Effects": getEffectsNames(getEffects(record))};
        case "ALCH":
            return {"Effects": getEffectsNames(getEffects(record))};
        case "AMMO":
            return {"Damage":xelib.GetDamage(record)};
        case "SCRL":
            return {"Effects": getEffectsDescriptions(getEffects(record))};
        case "BOOK":
            return {};
        case "MISC":
            return {};
        case "SLGM":
            return {};
        case "KEYM":
            return {};
        case "SPEL":
            return getSpellData(record);
        case "WOOP":
            return getWordOfPowerData(record);
        case "PERK":
            return {"Description": getPerkDescription(record)};
        default:
            zedit.log("Something went wrong! " + xelib.Signature(record));
            return {};
    }
}

function getWeaponData(record) {
    return {
        "Damage":xelib.GetDamage(record),
        "Type": getWeaponType(record),
        "Description": getItemDescription(record),
    };
}

function getWeaponType(record){
    const typePath = "DNAM\\Skill",
        weaponsTypes = ["One Handed", "Two Handed", "Archery"],
        receivedType = xelib.GetValue(record, typePath);

    if ( weaponsTypes.includes(receivedType) ) {
        return receivedType;
    } else if (receivedType !== "") {
        return ("Staff of " + receivedType);
    } else return ("Unknown");
}

function getArmorData(record){
    return {
        "Armor rating": xelib.GetArmorRating(record),
        "Armor type": xelib.GetArmorType(record),
        "Description": getItemDescription(record),
    }
}

function getSpellData(record){
    const effects = getEffects(record);
    return {"Effects": getEffectsDescriptions(effects), ...getSpellMasteryAndCategory(record)};
}

function getSpellMasteryAndCategory(record){
    let mastery = xelib.GetValue(record, "SPIT - Data\\Half-cost Perk"),
        category = mastery.slice(0, 4);
    switch(category) {
        case "Alte":
            return {"Category": "Alteration", "Mastery": getMastery(10, mastery)};
        case "Conj":
            return {"Category": "Conjuration", "Mastery": getMastery(11, mastery)};
        case "Dest":
            return {"Category": "Destruction", "Mastery": getMastery(11, mastery)};
        case "Illu":
            return {"Category": "Illusion", "Mastery": getMastery(8, mastery)};
        case "Rest":
            return {"Category": "Restoration", "Mastery": getMastery(11, mastery)};
        default:
            return {"Category": "", "Mastery": ""};
    }
}

function getMastery(start, fullString) {
    let mastery = fullString.slice(start, start+3)
    switch (mastery) {
        case "Nov":
            return "Novice";
        case "App":
            return "Apprentice";
        case "Ade":
            return "Adept";
        case "Exp":
            return "Expert";
        case "Mas":
            return "Master";
        default:
            return "";
    }
}

function getItemDescription(record) {
    const defaultItemDescription = xelib.GetValue(record, "DESC");
    if(defaultItemDescription !== "") return defaultItemDescription;

    let itemMagicEffect = xelib.GetValue(record, "EITM"),
        effects;
    if( itemMagicEffect === "") return "";

    const objectEffectString = sliceOfItself(itemMagicEffect, "H:", "]"),
        objectEffectFormID = parseInt(objectEffectString, 16);
    if (isNaN(objectEffectFormID)) {
        effects = [];
    } else {
        const enhanceRecord = xelib.GetRecord(0, objectEffectFormID);
        effects = getEffects(enhanceRecord);
    }


    return getEffectsDescriptions(effects);
}

function sliceOfItself(string, startString, endString){
    const startStringLength = startString.length;
    return string.slice(string.indexOf(startString) + startStringLength, string.indexOf(endString));
}

function getEffects(record){
    let effectIndex = 0,
        effect = xelib.GetValue(record, "Effects\\[" + effectIndex.toString() + "]\\EFID - Base Effect"),
        effects = [];

    while (effect !== ""){
        effects.push(effect);
        effectIndex = effectIndex + 1;
        effect = xelib.GetValue(record, "Effects\\[" + effectIndex.toString() + "]\\EFID - Base Effect");
    }
    return effects;
}

function getEffectsDescriptions(effects){
    let description = "";
    for (let effect of effects){
        const hexID = sliceOfItself(effect, "F:", "]"),
            formID = parseInt(hexID, 16),
            effectRecord = xelib.GetRecord(0, formID);

        description += xelib.GetValue(effectRecord, "DNAM - Magic Item Description");
        description += "|";
    }
    return description;
}

function getEffectsNames(effects){
    let names = "";
    for (let effect of effects){
        const firstQuoteIndex = effect.indexOf('"'),
            name = effect.slice(firstQuoteIndex + 1, effect.indexOf('"', firstQuoteIndex + 1));
        names += name;
        names += "|";
    }
    return names.slice(0, -1);
}

function getWordOfPowerData(record){
    return {"Translation": xelib.GetValue(record, "TNAM - Translation")};
}

function getPerkDescription(record) {
    return xelib.GetValue(record, "DESC");
}




processSelectedPlugins();
