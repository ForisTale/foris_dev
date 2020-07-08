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

    let alterationTable = $("#id_alteration_table"),
        alterationSelector = $("td", alterationTable),
        alterationInput = $("label > input", alterationSelector),
        firstSpell = ["Spell!", "adept", "Skyrim", "FR15", "957528", "Something"],
        secondSpell = ["Other spell!", "expert", "Skyrim", "Tas5", "04925", "Something else!"],
        tdArray = [];

    for (let td of alterationSelector) { tdArray.push(td.innerHTML); }

    assert.equal(alterationSelector.length, 14);
    assert.equal(alterationInput[0].checked, false);
    assert.equal(alterationInput[1].checked, true);
    assert.deepEqual(tdArray.slice(1, 7), secondSpell);
    assert.deepEqual(tdArray.slice(8, 14), firstSpell);
});


QUnit.test("Adjust table wrapper", function (assert) {
    new TECSpells(parameters);
    let firstTable = $("#id_alteration_panel"),
        wrapper = $(".dataTables_wrapper:first-child > .row:first-child > div", firstTable);

    assert.equal(wrapper.length, 3);
    assert.equal(wrapper.hasClass("col-sm-12 col-md-2"), true);
    assert.equal(wrapper.hasClass("col-md-8 col-12"), true);
    assert.equal(wrapper.hasClass("col-sm-12 col-md-2"), true);
});


QUnit.test("Inject button in table wrapper", function (assert) {
    new TECSpells(parameters);
    let submit_buttons = $(".table_wrapper > .col-md-2 > .submit_table"),
        reset_buttons = $(".table_wrapper > .col-md-2 > .reset_tables");

    assert.equal(submit_buttons.length, 6);
    assert.equal(reset_buttons.length, 6);
});

QUnit.test("Show messages in table wrapper", function (assert) {
    new TECSpells(parameters);
    let wrapper = $(".table_wrapper");

    assert.equal(wrapper.html().includes("Test message!"), true);
    assert.equal(wrapper.html().includes("Other test message!"), true);
});

QUnit.test("Messages are show only on visible table", function (assert) {
    fakeResponse();

    let firstPanel = $("#id_alteration_panel"),
        secondPanel = $("#id_destruction_panel"),
        firstWrapper = $(".table_wrapper", firstPanel),
        secondWrapper = $(".table_wrapper", secondPanel);

    assert.equal(firstWrapper.html().includes(("Test message!")), true)
    assert.equal(firstWrapper.html().includes(("Other test message!")), true)
    assert.equal(secondWrapper.html().includes(("Test message!")), false)
    assert.equal(secondWrapper.html().includes(("Other test message!")), false)
});


QUnit.test("Test sending ajax post", function (assert) {
    fakeResponse()

    let button = $("#id_alteration_table_wrapper > .row > div > .table_wrapper > .col-md-2 > .submit_table");
    button.click();

    assert.equal(server.requests.length, 7);
    let request = server.requests[6];

    assert.equal(request.url, "/fakeUrl/");
    assert.equal(request.method, "POST");
    assert.equal(
        request.requestBody,
        "csrfmiddlewaretoken=fakeToken&table_input=%5B%7B%22name%22%3A%22957528%22%2C%22value%22%3A%22on%22" +
        "%7D%2C%7B%22name%22%3A%22017288%22%2C%22value%22%3A%22on%22%7D%2C%7B%22name%22%3A%22017288%22%2C%22value%" +
        "22%3A%22on%22%7D%2C%7B%22name%22%3A%22017288%22%2C%22value%22%3A%22on%22%7D%2C%7B%22name%22%3A%22017288%" +
        "22%2C%22value%22%3A%22on%22%7D%2C%7B%22name%22%3A%22017288%22%2C%22value%22%3A%22on%22%7D%5D"
    );

});

QUnit.test("Test reset button send ajax post", function (assert) {
    fakeResponse()

    let button = $("#id_alteration_table_wrapper > .row > div > .table_wrapper > .col-md-2 > .reset_tables");
    button.click();

    assert.equal(server.requests.length, 7);
    let request = server.requests[6];

    assert.equal(request.url, "/fakeUrl/");
    assert.equal(request.method, "POST");
    assert.equal(request.requestBody, "csrfmiddlewaretoken=fakeToken&reset=");
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
    server.respondWith("GET", "/api/tec/spells/other/", [
        200,
        {"Content-Type": "application/json"},
        JSON.stringify(parameters.other),
    ]);


    let tec = new TECSpells(parameters);
    server.respond();
    return tec.tables;
}


function data() {
    return {
        messages: ["Test message!", "Other test message!"],
        url: "/fakeUrl/",
        alteration: [
            {
                "selected": "on",
                "plugin_name": "Skyrim",
                "name": "Spell!",
                "editor_id": "FR15",
                "form_id": "957528",
                "mastery": "adept",
                "effects": "Something",
            },
            {
                "selected": "",
                "plugin_name": "Skyrim",
                "name": "Other spell!",
                "editor_id": "Tas5",
                "form_id": "04925",
                "mastery": "expert",
                "effects": "Something else!",
            },
        ],
        conjuration: [
            {
                "selected": "on",
                "plugin_name": "Skyrim",
                "name": "Sword!",
                "editor_id": "DA14",
                "form_id": "017288",
                "mastery": "adept",
                "effects": "Something",
            },
        ],
        destruction: [
            {
                "selected": "on",
                "plugin_name": "Skyrim",
                "name": "Sword!",
                "editor_id": "DA14",
                "form_id": "017288",
                "mastery": "adept",
                "effects": "Something",
            },
        ],
        illusion: [
            {
                "selected": "on",
                "plugin_name": "Skyrim",
                "name": "Sword!",
                "editor_id": "DA14",
                "form_id": "017288",
                "mastery": "adept",
                "effects": "Something",
            },
        ],
        restoration: [
            {
                "selected": "on",
                "plugin_name": "Skyrim",
                "name": "Sword!",
                "editor_id": "DA14",
                "form_id": "017288",
                "mastery": "adept",
                "effects": "Something",
            },
        ],
        other: [
            {
                "selected": "on",
                "plugin_name": "Skyrim",
                "name": "Sword!",
                "editor_id": "DA14",
                "form_id": "017288",
                "mastery": "adept",
                "effects": "Something",
            },
        ],
};
}

