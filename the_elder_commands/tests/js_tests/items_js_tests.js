
let parameters = data(),
    server, sandbox;


QUnit.testStart(function () {
    server = sinon.fakeServer.create();
});


QUnit.testDone(function () {
    server = sinon.restore();
});


QUnit.test("InitializeDatatable call ajax with correct url", function (assert) {
    window.TEC.initializeDataTables("items");
    assert.equal(server.requests.length, 10);
    let request = server.requests[0];

    assert.equal(request.url.slice(0, 20), "/api/tec/items/WEAP/");
    assert.equal(request.method, "GET");
});


QUnit.test("Datatable load correctly with populate data from ajax", function (assert) {
    fakeResponse();

    let table = $("#id_weapons_table"),
        selector = $("td", table),
        template = ['<label><input type="text" name="017288" value="11"></label>', "Sword!", '17', '90', "Two Handed",
            '17', "Skyrim", "DA14", "017288", "Something"],
        tdArray = [],
        expected = [];

    for (let i = 0; i < 10; i++) {
        expected = expected.concat(template);
    }

    for (let td of selector) {
        tdArray.push(td.innerHTML);
    }

    assert.equal(selector.length, 100);
    assert.deepEqual(tdArray, expected);
});


QUnit.test("First column is type input", function (assert) {
    fakeResponse();

    let table = $("#id_weapons_table"),
        td = $("td", table),
        firstTdHtml = td.get(0).innerHTML;

    assert.equal(firstTdHtml.slice(0, 13), "<label><input");
});

QUnit.test("Column selected is not visible", function (assert) {
    let tables = window.TEC.initialize(parameters),
        table = tables[0],
        lastColumn = table.api().column(-1);

    assert.equal(lastColumn.visible(), false);
});

QUnit.test("Adjust table wrapper", function (assert) {
    window.TEC.initialize(parameters);
    let firstTable = $("#id_weapons_panel"),
        wrapper = $(".dataTables_wrapper:first-child > .row:first-child > div", firstTable);

    assert.equal(wrapper.length, 3);
    assert.equal(wrapper.hasClass("col-sm-12 col-md-2"), true);
    assert.equal(wrapper.hasClass("col-md-8 col-12"), true);
    assert.equal(wrapper.hasClass("col-sm-12 col-md-2"), true);

});

QUnit.test("Inject button in table wrapper", function (assert) {
    window.TEC.initialize(parameters);
    let wrapper = $(".table_wrapper > .col-md-1 > button");

    assert.equal(wrapper.hasClass("submit_table"), true);
});

QUnit.test("Show messages in table wrapper", function (assert) {
    window.TEC.initialize(parameters);
    let wrapper = $(".table_wrapper");

    assert.equal(wrapper.html().includes("Test message!"), true);
    assert.equal(wrapper.html().includes("Other test message!"), true);
});

QUnit.test("Messages are show only on visible table", function (assert) {
    fakeResponse();

    let firstPanel = $("#id_weapons_panel"),
        secondPanel = $("#id_armors_panel"),
        firstWrapper = $(".table_wrapper", firstPanel),
        secondWrapper = $(".table_wrapper", secondPanel);


    assert.equal(firstWrapper.html().includes(("Test message!")), true)
    assert.equal(firstWrapper.html().includes(("Other test message!")), true)
    assert.equal(secondWrapper.html().includes(("Test message!")), false)
    assert.equal(secondWrapper.html().includes(("Other test message!")), false)

});

QUnit.test("Test sending ajax post", function (assert) {
    fakeResponse()

    let button = $("#id_weapons_table_wrapper > .row > div > .table_wrapper > .col-md-1 > .submit_table");
    button.click();

    assert.equal(server.requests.length, 11);
    let request = server.requests[10];

    assert.equal(request.url, "/fakeUrl/");
    assert.equal(request.method, "POST");
    assert.equal(
        request.requestBody,
        "csrfmiddlewaretoken=fakeToken&table_input=%5B%7B%22name%22%3A%22017288%22%2C%22value%22%3A%22" +
        "11%22%7D%2C%7B%22name%22%3A%22017288%22%2C%22value%22%3A%2211%22%7D%2C%7B%22name%22%3A%22017288%22%" +
        "2C%22value%22%3A%2211%22%7D%2C%7B%22name%22%3A%22017288%22%2C%22value%22%3A%2211%22%7D%2C%7B%22name%" +
        "22%3A%22017288%22%2C%22value%22%3A%2211%22%7D%2C%7B%22name%22%3A%22017288%22%2C%22value%22%3A%2211%2" +
        "2%7D%2C%7B%22name%22%3A%22017288%22%2C%22value%22%3A%2211%22%7D%2C%7B%22name%22%3A%22017288%22%2C%22" +
        "value%22%3A%2211%22%7D%2C%7B%22name%22%3A%22017288%22%2C%22value%22%3A%2211%22%7D%2C%7B%22name%22%3A" +
        "%22017288%22%2C%22value%22%3A%2211%22%7D%2C%7B%22name%22%3A%22017288%22%2C%22value%22%3A%2211%22%7D%2" +
        "C%7B%22name%22%3A%22016FFF%22%2C%22value%22%3A%2201%22%7D%2C%7B%22name%22%3A%22016FFF%22%2C%22value%2" +
        "2%3A%2201%22%7D%2C%7B%22name%22%3A%22016FFF%22%2C%22value%22%3A%2201%22%7D%2C%7B%22name%22%3A%22016FF" +
        "F%22%2C%22value%22%3A%2201%22%7D%2C%7B%22name%22%3A%22016FFF%22%2C%22value%22%3A%2201%22%7D%2C%7B%22" +
        "name%22%3A%22016FFF%22%2C%22value%22%3A%2201%22%7D%2C%7B%22name%22%3A%22016FFF%22%2C%22value%22%3A%2201" +
        "%22%7D%2C%7B%22name%22%3A%22016FFF%22%2C%22value%22%3A%2201%22%7D%2C%7B%22name%22%3A%22016FFF%22%2C%22value" +
        "%22%3A%2201%22%7D%5D"
    );

});


QUnit.test("Test buttons hide not selected and show all, click on one remove it and show other.", function (assert) {
    fakeResponse();
    let only_test_table = $(".tab-content"),
        wrapper = $(".table_wrapper > .col-md-1 >", only_test_table);

    assert.equal(wrapper.length, 20);
    assert.equal(wrapper[1].outerHTML.includes('hide_not_selected'), true);

    wrapper[1].click();

    wrapper = $(".table_wrapper > .col-md-1 >", only_test_table);

    assert.equal(wrapper.length, 20);
    assert.equal(wrapper[1].outerHTML.includes('show_all'), true);

    wrapper[1].click();

    wrapper = $(".table_wrapper > .col-md-1 >", only_test_table);

    assert.equal(wrapper.length, 20);
    assert.equal(wrapper[1].outerHTML.includes('hide_not_selected'), true);
});


QUnit.test("test show and hide search on selected column", function (assert) {
    fakeResponse();
    let only_test_table = $(".tab-content"),
        entries = $("tbody > tr", only_test_table);
    assert.equal(entries.length, 28);

    $(".hide_not_selected")[0].click();

    entries = $("tbody > tr", only_test_table);
    assert.equal(entries.length, 19);

    $(".show_all")[0].click();

    entries = $("tbody > tr", only_test_table);
    assert.equal(entries.length, 28);


});

QUnit.test("test show and hide clear normal search when pressed", function (assert) {
    fakeResponse();
    let only_test_table = $("#id_weapons_tbody"),
        search_input = $("#id_weapons_table_filter > label > input");

    search_input.val("9999");
    search_input.trigger("keyup");

    let rows = $("tr", only_test_table);
    assert.equal(rows.length, 1);

    $(".hide_not_selected")[0].click();

    rows = $("tr", only_test_table);
    assert.equal(rows.length, 10);

    search_input.val("9999");
    search_input.trigger("keyup");

    $(".show_all")[0].click();

    rows = $("tr", only_test_table);
    assert.equal(rows.length, 10);


});


QUnit.test("test give quantity change selected column to true, empty string change it to false", function (assert) {
    let tables = fakeResponse(),
        table = tables[0],
        row, col, cell,
        simpleTable = $("#id_weapons_table"),
        input = $("input:first-child", simpleTable);

    input.val("");
    input.trigger("keyup");

    row = table.api().row(0);
    col = table.api().column(-1);
    cell = table.api().cell(row, col);

    assert.equal(cell.data(), "false");


    input.val("12");
    input.trigger("keyup");

    row = table.api().row(0);
    col = table.api().column(-1);
    cell = table.api().cell(row, col);

    assert.equal(cell.data(), "true");
});




function fakeResponse() {
    server.respondWith("GET", "/api/tec/items/WEAP/", [
        200,
        {"Content-Type": "application/json"},
        JSON.stringify(parameters.WEAP),
    ]);
    server.respondWith("GET", "/api/tec/items/ARMO/", [
        200,
        {"Content-Type": "application/json"},
        JSON.stringify(parameters.ARMO),
    ]);
    server.respondWith("GET", "/api/tec/items/AMMO/", [
        200,
        {"Content-Type": "application/json"},
        JSON.stringify(parameters.AMMO),
    ]);
    server.respondWith("GET", "/api/tec/items/BOOK/", [
        200,
        {"Content-Type": "application/json"},
        JSON.stringify(parameters.BOOK),
    ]);
    server.respondWith("GET", "/api/tec/items/INGR/", [
        200,
        {"Content-Type": "application/json"},
        JSON.stringify(parameters.INGR),
    ]);
    server.respondWith("GET", "/api/tec/items/ALCH/", [
        200,
        {"Content-Type": "application/json"},
        JSON.stringify(parameters.ALCH),
    ]);
    server.respondWith("GET", "/api/tec/items/SCRL/", [
        200,
        {"Content-Type": "application/json"},
        JSON.stringify(parameters.SCRL),
    ]);
    server.respondWith("GET", "/api/tec/items/SLGM/", [
        200,
        {"Content-Type": "application/json"},
        JSON.stringify(parameters.SLGM),
    ]);
    server.respondWith("GET", "/api/tec/items/KEYM/", [
        200,
        {"Content-Type": "application/json"},
        JSON.stringify(parameters.KEYM),
    ]);
    server.respondWith("GET", "/api/tec/items/MISC/", [
        200,
        {"Content-Type": "application/json"},
        JSON.stringify(parameters.MISC),
    ]);


    let tables = window.TEC.initialize(parameters);
    server.respond();
    return tables;
}


function data() {
    return {
        messages: ["Test message!", "Other test message!"],
        url: "/fakeUrl/",
        site: "items",
        WEAP: [
            {
                "quantity": "11",
                "plugin_name": "Skyrim",
                "fullName": "Sword!",
                "editorId": "DA14",
                "formId": "017288",
                "Weight": 17,
                "Value": 90,
                "Damage": 17,
                "Type": "Two Handed",
                "Description": "Something",
                "selected": true,
            },
            {
                "quantity": "11",
                "plugin_name": "Skyrim",
                "fullName": "Sword!",
                "editorId": "DA14",
                "formId": "017288",
                "Weight": 17,
                "Value": 90,
                "Damage": 17,
                "Type": "Two Handed",
                "Description": "Something",
                "selected": true,
            },
            {
                "quantity": "11",
                "plugin_name": "Skyrim",
                "fullName": "Sword!",
                "editorId": "DA14",
                "formId": "017288",
                "Weight": 17,
                "Value": 90,
                "Damage": 17,
                "Type": "Two Handed",
                "Description": "Something",
                "selected": true,
            },
            {
                "quantity": "11",
                "plugin_name": "Skyrim",
                "fullName": "Sword!",
                "editorId": "DA14",
                "formId": "017288",
                "Weight": 17,
                "Value": 90,
                "Damage": 17,
                "Type": "Two Handed",
                "Description": "Something",
                "selected": true,
            },
            {
                "quantity": "11",
                "plugin_name": "Skyrim",
                "fullName": "Sword!",
                "editorId": "DA14",
                "formId": "017288",
                "Weight": 17,
                "Value": 90,
                "Damage": 17,
                "Type": "Two Handed",
                "Description": "Something",
                "selected": true,
            },
            {
                "quantity": "11",
                "plugin_name": "Skyrim",
                "fullName": "Sword!",
                "editorId": "DA14",
                "formId": "017288",
                "Weight": 17,
                "Value": 90,
                "Damage": 17,
                "Type": "Two Handed",
                "Description": "Something",
                "selected": true,
            },
            {
                "quantity": "11",
                "plugin_name": "Skyrim",
                "fullName": "Sword!",
                "editorId": "DA14",
                "formId": "017288",
                "Weight": 17,
                "Value": 90,
                "Damage": 17,
                "Type": "Two Handed",
                "Description": "Something",
                "selected": true,
            },
            {
                "quantity": "11",
                "plugin_name": "Skyrim",
                "fullName": "Sword!",
                "editorId": "DA14",
                "formId": "017288",
                "Weight": 17,
                "Value": 90,
                "Damage": 17,
                "Type": "Two Handed",
                "Description": "Something",
                "selected": true,
            },
            {
                "quantity": "11",
                "plugin_name": "Skyrim",
                "fullName": "Sword!",
                "editorId": "DA14",
                "formId": "017288",
                "Weight": 17,
                "Value": 90,
                "Damage": 17,
                "Type": "Two Handed",
                "Description": "Something",
                "selected": true,
            },
            {
                "quantity": "11",
                "plugin_name": "Skyrim",
                "fullName": "Sword!",
                "editorId": "DA14",
                "formId": "017288",
                "Weight": 17,
                "Value": 90,
                "Damage": 17,
                "Type": "Two Handed",
                "Description": "Something",
                "selected": true,
            },
            {
                "quantity": "11",
                "plugin_name": "Skyrim",
                "fullName": "Sword!",
                "editorId": "DA14",
                "formId": "017288",
                "Weight": 17,
                "Value": 90,
                "Damage": 17,
                "Type": "Two Handed",
                "Description": "Something",
                "selected": true,
            },
        ],
        ARMO: [
            {
                "quantity": "",
                "plugin_name": "Skyrim",
                "fullName": "Shoes",
                "editorId": "DremoraBoots",
                "formId": "016FFF",
                "Weight": 1,
                "Value": 4,
                "Armor rating": 0,
                "Armor type": "Clothing",
                "Description": "",
                "selected": false,
            },
            {
                "quantity": "",
                "plugin_name": "Skyrim",
                "fullName": "Shoes",
                "editorId": "DremoraBoots",
                "formId": "016FFF",
                "Weight": 1,
                "Value": 4,
                "Armor rating": 0,
                "Armor type": "Clothing",
                "Description": "",
                "selected": false,
            },
            {
                "quantity": "",
                "plugin_name": "Skyrim",
                "fullName": "Shoes",
                "editorId": "DremoraBoots",
                "formId": "016FFF",
                "Weight": 1,
                "Value": 4,
                "Armor rating": 0,
                "Armor type": "Clothing",
                "Description": "",
                "selected": false,
            },
            {
                "quantity": "",
                "plugin_name": "Skyrim",
                "fullName": "Shoes",
                "editorId": "DremoraBoots",
                "formId": "016FFF",
                "Weight": 1,
                "Value": 4,
                "Armor rating": 0,
                "Armor type": "Clothing",
                "Description": "",
                "selected": false,
            },
            {
                "quantity": "",
                "plugin_name": "Skyrim",
                "fullName": "Shoes",
                "editorId": "DremoraBoots",
                "formId": "016FFF",
                "Weight": 1,
                "Value": 4,
                "Armor rating": 0,
                "Armor type": "Clothing",
                "Description": "",
                "selected": false,
            },
            {
                "quantity": "",
                "plugin_name": "Skyrim",
                "fullName": "Shoes",
                "editorId": "DremoraBoots",
                "formId": "016FFF",
                "Weight": 1,
                "Value": 4,
                "Armor rating": 0,
                "Armor type": "Clothing",
                "Description": "",
                "selected": false,
            },
            {
                "quantity": "",
                "plugin_name": "Skyrim",
                "fullName": "Shoes",
                "editorId": "DremoraBoots",
                "formId": "016FFF",
                "Weight": 1,
                "Value": 4,
                "Armor rating": 0,
                "Armor type": "Clothing",
                "Description": "",
                "selected": false,
            },
            {
                "quantity": "",
                "plugin_name": "Skyrim",
                "fullName": "Shoes",
                "editorId": "DremoraBoots",
                "formId": "016FFF",
                "Weight": 1,
                "Value": 4,
                "Armor rating": 0,
                "Armor type": "Clothing",
                "Description": "",
                "selected": false,
            },
            {
                "quantity": "",
                "plugin_name": "Skyrim",
                "fullName": "Shoes",
                "editorId": "DremoraBoots",
                "formId": "016FFF",
                "Weight": 1,
                "Value": 4,
                "Armor rating": 0,
                "Armor type": "Clothing",
                "Description": "",
                "selected": false,
            },
            {
                "quantity": "",
                "plugin_name": "Skyrim",
                "fullName": "Shoes",
                "editorId": "DremoraBoots",
                "formId": "016FFF",
                "Weight": 1,
                "Value": 4,
                "Armor rating": 0,
                "Armor type": "Clothing",
                "Description": "",
                "selected": false,
            },
            {
                "quantity": "",
                "plugin_name": "Skyrim",
                "fullName": "Shoes",
                "editorId": "DremoraBoots",
                "formId": "016FFF",
                "Weight": 1,
                "Value": 4,
                "Armor rating": 0,
                "Armor type": "Clothing",
                "Description": "",
                "selected": false,
            },
            {
                "quantity": "01",
                "plugin_name": "Skyrim",
                "fullName": "Shoes",
                "editorId": "DremoraBoots",
                "formId": "016FFF",
                "Weight": 1,
                "Value": 4,
                "Armor rating": 0,
                "Armor type": "Clothing",
                "Description": "",
                "selected": true,
            },
        ],
        AMMO: [
            {
                "quantity": "01",
                "plugin_name": "Skyrim",
                "fullName": "Shoes",
                "editorId": "DremoraBoots",
                "formId": "016FFF",
                "Damage": 1,
                "Value": 4,
                "selected": true,
            },
        ],
        BOOK: [
            {
                "quantity": "01",
                "plugin_name": "Skyrim",
                "fullName": "Shoes",
                "editorId": "DremoraBoots",
                "formId": "016FFF",
                "Value": 4,
                "Weight": 1,
                "selected": true,
            },
        ],
        INGR: [
            {
                "quantity": "01",
                "plugin_name": "Skyrim",
                "fullName": "Shoes",
                "editorId": "DremoraBoots",
                "formId": "016FFF",
                "Effects": 1,
                "Value": 4,
                "Weight": 1,
                "selected": true,
            },
        ],
        ALCH: [
            {
                "quantity": "01",
                "plugin_name": "Skyrim",
                "fullName": "Shoes",
                "editorId": "DremoraBoots",
                "formId": "016FFF",
                "Effects": 1,
                "Value": 4,
                "Weight": 1,
                "selected": true,
            },
        ],
        SCRL: [
            {
                "quantity": "01",
                "plugin_name": "Skyrim",
                "fullName": "Shoes",
                "editorId": "DremoraBoots",
                "formId": "016FFF",
                "Value": 4,
                "Weight": 1,
                "Effects": 1,
                "selected": true,
            },
        ],
        SLGM: [
            {
                "quantity": "01",
                "plugin_name": "Skyrim",
                "fullName": "Shoes",
                "editorId": "DremoraBoots",
                "formId": "016FFF",
                "Value": 4,
                "Weight": 1,
                "selected": true,
            },
        ],
        KEYM: [
            {
                "quantity": "01",
                "plugin_name": "Skyrim",
                "fullName": "Shoes",
                "editorId": "DremoraBoots",
                "formId": "016FFF",
                "Value": 4,
                "Weight": 1,
                "selected": true,
            },
        ],
        MISC: [
            {
                "quantity": "01",
                "plugin_name": "Skyrim",
                "fullName": "Shoes",
                "editorId": "DremoraBoots",
                "formId": "016FFF",
                "Value": 4,
                "Weight": 1,
                "selected": true,
            },
        ],
};
}