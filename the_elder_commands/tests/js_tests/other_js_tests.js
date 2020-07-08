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

    let WordsofpowerTable = $("#id_wordsofpower_table"),
        wordsOfPowerTableData = $("td", WordsofpowerTable),
        wordsOfPowerInput = $("label > input", wordsOfPowerTableData),
        firstSpell = ["Word!", "adept", "Skyrim", "FR15", "957528"],
        secondSpell = ["Other word!", "expert", "Skyrim", "Tas5", "04925"],
        tdArray = [];

    for (let td of wordsOfPowerTableData) { tdArray.push(td.innerHTML); }

    assert.equal(wordsOfPowerTableData.length, 12);
    assert.equal(wordsOfPowerInput[0].checked, false);
    assert.equal(wordsOfPowerInput[1].checked, true);
    assert.deepEqual(tdArray.slice(1, 6), secondSpell);
    assert.deepEqual(tdArray.slice(7, 12), firstSpell);
});

QUnit.test("Datatable initialize for normal tables", function (assert) {
    let tables = fakeResponse(),
        varietyTable = $("tr", tables[0]),
        locationTable = $("tr", tables[1]);

    assert.equal(varietyTable.length, 7);
    assert.equal(locationTable.length, 3);
});


QUnit.test("Adjust table wrapper", function (assert) {
    new TECOther(parameters);
    let firstTable = $("#id_wordsofpower_panel"),
        wrapper = $(".dataTables_wrapper:first-child > .row:first-child > div", firstTable);

    assert.equal(wrapper.length, 3);
    assert.equal(wrapper.hasClass("col-sm-12 col-md-2"), true);
    assert.equal(wrapper.hasClass("col-md-8 col-12"), true);
    assert.equal(wrapper.hasClass("col-sm-12 col-md-2"), true);
});


QUnit.test("Inject buttons in table wrapper", function (assert) {
    new TECOther(parameters);
    let submit_buttons = $(".table_wrapper > .col-md-2 > .submit_table"),
        reset_buttons = $(".table_wrapper > .col-md-2 > .reset_tables");

    assert.equal(submit_buttons.length, 3);
    assert.equal(reset_buttons.length, 3);
});

QUnit.test("Show messages in table wrapper", function (assert) {
    new TECOther(parameters);
    let wrapper = $(".table_wrapper:visible");

    assert.equal(wrapper.html().includes("Test message!"), true);
    assert.equal(wrapper.html().includes("Other test message!"), true);
});

QUnit.test("Messages are show only on visible table", function (assert) {
    fakeResponse();

    let firstPanel = $("#id_wordsofpower_panel"),
        secondPanel = $("#id_perks_panel"),
        firstWrapper = $(".table_wrapper", firstPanel),
        secondWrapper = $(".table_wrapper", secondPanel);

    assert.equal(firstWrapper.html().includes(("Test message!")), true)
    assert.equal(firstWrapper.html().includes(("Other test message!")), true)
    assert.equal(secondWrapper.html().includes(("Test message!")), false)
    assert.equal(secondWrapper.html().includes(("Other test message!")), false)
});


QUnit.test("Test sending ajax post", function (assert) {
    fakeResponse()

    let button = $("#id_wordsofpower_table_wrapper > .row > div > .table_wrapper > .col-md-2 > .submit_table");
    button.click();

    assert.equal(server.requests.length, 3);
    let request = server.requests[2];

    assert.equal(request.url, "/fakeUrl/");
    assert.equal(request.method, "POST");
    assert.equal(
        request.requestBody,
        "csrfmiddlewaretoken=fakeToken&table_input=%5B%7B%22name%22%3A%22gold%22%2C%22value%22%3A%2210%22" +
        "%7D%2C%7B%22name%22%3A%22location%22%2C%22value%22%3A%22Test!%22%7D%2C%7B%22name%22%3A%22word957528%22%" +
        "2C%22value%22%3A%22on%22%7D%2C%7B%22name%22%3A%22perk017288%22%2C%22value%22%3A%22on%22%7D%5D"
    );

});

QUnit.test("Test reset button send ajax post", function (assert) {
    fakeResponse()

    let button = $("#id_wordsofpower_table_wrapper > .row > div > .table_wrapper > .col-md-2 > .reset_tables");
    button.click();

    assert.equal(server.requests.length, 3);
    let request = server.requests[2];

    assert.equal(request.url, "/fakeUrl/");
    assert.equal(request.method, "POST");
    assert.equal(request.requestBody, "csrfmiddlewaretoken=fakeToken&reset=");
});


function fakeResponse() {
    server.respondWith("GET", "/api/tec/wordsofpower/", [
        200,
        {"Content-Type": "application/json"},
        JSON.stringify(parameters.wordsofpower),
    ]);
    server.respondWith("GET", "/api/tec/perks/", [
        200,
        {"Content-Type": "application/json"},
        JSON.stringify(parameters.perks),
    ]);


    let tec = new TECOther(parameters);
    server.respond();
    return tec.tables;
}


function data() {
    return {
        messages: ["Test message!", "Other test message!"],
        url: "/fakeUrl/",
        wordsofpower: [
            {
                "selected": "on",
                "plugin_name": "Skyrim",
                "word": "Word!",
                "editor_id": "FR15",
                "form_id": "957528",
                "translation": "adept",
            },
            {
                "selected": "",
                "plugin_name": "Skyrim",
                "word": "Other word!",
                "editor_id": "Tas5",
                "form_id": "04925",
                "translation": "expert",
            },
        ],
        perks: [
            {
                "selected": "on",
                "plugin_name": "Skyrim",
                "name": "Perk!",
                "editor_id": "DA14",
                "form_id": "017288",
                "description": "Something",
            },
        ],
};
}

