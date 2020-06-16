let parameters = data(),
    server, sandbox;


QUnit.testStart(function () {
    server = sinon.fakeServer.create();
});


QUnit.testDone(function () {
    server = sinon.restore();
});


QUnit.test("Datatable load correctly with populate data from ajax", function (assert) {
    fakeResponse();

    let table = $("#id_alteration_table"),
        selector = $("td", table),
        template = ["on", "Spell!", "adept", "Skyrim", "FR15", "957528", "Something"],
        tdArray = [];

    for (let td of selector) {
        tdArray.push(td.innerHTML);
    }

    assert.equal(selector.length, 7);
    assert.deepEqual(tdArray, template);
});


function fakeResponse() {
    server.respondWith("GET", "/api/tec/spells/alteration/", [
        200,
        {"Content-Type": "application/json"},
        JSON.stringify(parameters.alteration),
    ]);
    server.respondWith("GET", "/api/tec/spells/conjuration/", [
        200,
        {"Content-Type": "application/json"},
        JSON.stringify(parameters.conjuration),
    ]);
    server.respondWith("GET", "/api/tec/spells/destruction/", [
        200,
        {"Content-Type": "application/json"},
        JSON.stringify(parameters.destruction),
    ]);
    server.respondWith("GET", "/api/tec/spells/illusion/", [
        200,
        {"Content-Type": "application/json"},
        JSON.stringify(parameters.illusion),
    ]);
    server.respondWith("GET", "/api/tec/spells/restoration/", [
        200,
        {"Content-Type": "application/json"},
        JSON.stringify(parameters.restoration),
    ]);
    server.respondWith("GET", "/api/tec/spells/wordsofpower/", [
        200,
        {"Content-Type": "application/json"},
        JSON.stringify(parameters.wordsofpower),
    ]);
    server.respondWith("GET", "/api/tec/spells/other/", [
        200,
        {"Content-Type": "application/json"},
        JSON.stringify(parameters.other),
    ]);


    let tables = TECSpells.initializeSpells(parameters);
    server.respond();
    return tables;
}


function data() {
    return {
        messages: ["Test message!", "Other test message!"],
        url: "/fakeUrl/",
        site: "spells",
        alteration: [
            {
                "selected": "on",
                "plugin_name": "Skyrim",
                "fullName": "Spell!",
                "editorId": "FR15",
                "formId": "957528",
                "mastery": "adept",
                "Effect": "Something",
            },
        ],
        conjuration: [
            {
                "selected": "on",
                "plugin_name": "Skyrim",
                "fullName": "Sword!",
                "editorId": "DA14",
                "formId": "017288",
                "mastery": "adept",
                "Effect": "Something",
            },
        ],
        destruction: [
            {
                "selected": "on",
                "plugin_name": "Skyrim",
                "fullName": "Sword!",
                "editorId": "DA14",
                "formId": "017288",
                "mastery": "adept",
                "Effect": "Something",
            },
        ],
        illusion: [
            {
                "selected": "on",
                "plugin_name": "Skyrim",
                "fullName": "Sword!",
                "editorId": "DA14",
                "formId": "017288",
                "mastery": "adept",
                "Effect": "Something",
            },
        ],
        restoration: [
            {
                "selected": "on",
                "plugin_name": "Skyrim",
                "fullName": "Sword!",
                "editorId": "DA14",
                "formId": "017288",
                "mastery": "adept",
                "Effect": "Something",
            },
        ],
        wordsofpower: [
            {
                "selected": "on",
                "plugin_name": "Skyrim",
                "word": "Sword!",
                "editorId": "DA14",
                "formId": "017288",
                "translation": "meaning",
            },
        ],
        other: [
            {
                "selected": "on",
                "plugin_name": "Skyrim",
                "fullName": "Sword!",
                "editorId": "DA14",
                "formId": "017288",
                "mastery": "adept",
                "Effect": "Something",
            },
        ],
};
}

