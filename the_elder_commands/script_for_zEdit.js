//SLGM - soul gems
const itemsSignatures = ["WEAP", "ARMO", "BOOK", "INGR", "ALCH",
                         "MISC", "AMMO", "SCRL", "SLGM", "KEYM"],
    magicSignatures = ["SPEL", "WOOP"];
let pluginName,
    //waiting for new version of zEdit for ESL support.
    isEsl = false,
    skyrimAndDlc = ["Skyrim", "Dawnguard", "Dragonborn", "HearthFires"];


function processSelectedPlugins(){
    for (let selectedPlugin of zedit.GetSelectedNodes()) {
        const selectedPluginHandle = selectedPlugin.handle,
            signatures = itemsSignatures.concat(magicSignatures);
        pluginName = selectedPlugin.column_values[0].slice(5, -4);

        fh.saveJsonFile(fh.jetpack.cwd() + "\\The_Elder_Commands\\" + pluginName + ".json",
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
    if (skyrimAndDlc.includes(pluginName))
        return xelib.GetHexFormID(record);
    else if (isEsl)
        return "FEXXX" + xelib.GetHexFormID(record).slice(5);
    else
        return "XX" + xelib.GetHexFormID(record).slice(2);
}

function getItemCommonData(record) {
    if (itsItem(record))
        return {"Weight": xelib.GetWeight(record), "Value": xelib.GetGoldValue(record)};
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
    return {"Effects": getEffectsDescriptions(effects), "Spell Mastery": getSpellMastery(record)};
}

function getSpellMastery(record){
    let mastery = xelib.GetValue(record, "SPIT - Data\\Half-cost Perk");
    return mastery.slice(mastery.indexOf("\"") + 1, mastery.lastIndexOf("\""));
}

function getItemDescription(record) {
    const defaultItemDescription = xelib.GetValue(record, "DESC");
    if(defaultItemDescription !== "") return defaultItemDescription;

    let itemMagicEffect = xelib.GetValue(record, "EITM");
    if( itemMagicEffect === "") return "";

    const objectEffectFormID = parseInt(sliceOfItself(itemMagicEffect, ":", "]"), 16),
        enhanceRecord = xelib.GetRecord(0, objectEffectFormID),
        effects = getEffects(enhanceRecord);

    return getEffectsDescriptions(effects);
}

function sliceOfItself(string, startString, endString){
    return string.slice(string.indexOf(startString) + 1, string.indexOf(endString));
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
        const formID = parseInt(sliceOfItself(effect, ":", "]"), 16);
        //Skyrim.esp has error in spell records, it call to non exist effects, possible cause of crash in game.
        if (formID === 12) return "";

        const effectRecord = xelib.GetRecord(0, formID);
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




processSelectedPlugins();
