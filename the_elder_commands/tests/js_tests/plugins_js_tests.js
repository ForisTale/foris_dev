let parameters = data(),
    server;

QUnit.testStart(function () {
    server = sinon.fakeServer.create();
});


QUnit.testDone(function () {
    server = sinon.restore();
});


QUnit.test("DataTable initialize for plugins table.", function (assert) {
    let initializedTable = new TECPlugins(parameters),
        table = $("tr", initializedTable.table);
    assert.equal(table.length, 4);
});


QUnit.test("Adjust table wrapper.", function (assert) {
    new TECPlugins(parameters);
    let wrapper = $(".dataTables_wrapper:first-child > .row:first-child > div");

    assert.equal(wrapper.length, 3);
    assert.equal(wrapper.hasClass("col-sm-12 col-md-2"), true);
    assert.equal(wrapper.hasClass("col-md-8 col-12"), true);
    assert.equal(wrapper.hasClass("col-sm-12 col-md-2"), true);
});

QUnit.test("Inject submit button into table.", function (assert) {
    new TECPlugins(parameters);
    let submit_buttons = $(".table_wrapper > .col-md-2 > .submit_table");

    assert.equal(submit_buttons.length, 1);
});

QUnit.test("Show message in table wrapper.", function (assert) {
    new TECPlugins(parameters);
    let wrapper = $(".table_wrapper:visible");

    assert.equal(wrapper.html().includes("Test message!"), true);
    assert.equal(wrapper.html().includes("Other message."), true);
});

QUnit.test("Sending ajax post.", function (assert) {
    new TECPlugins(parameters);

    let button = $(".table_wrapper > .col-md-2 > .submit_table");
    button.click();

    assert.equal(server.requests.length, 1);
    let request = server.requests[0];

    assert.equal(request.url, "/fakeUrl/");
    assert.equal(request.method, "POST");
    assert.equal(
        request.requestBody,
        "csrfmiddlewaretoken=fakeToken&selected_plugins=%5B%7B%22name%22%3A%22colorfulmagicse%22%2C%22variant%22%" +
        "3A%221.0%26english%26%22%2C%22load_order%22%3A%2202%22%7D%2C%7B%22name%22%3A%22skyrim%22%2C%22variant%22%" +
        "3A%221.0%26english%26%22%2C%22load_order%22%3A%2201%22%7D%5D"
    );
});


function data() {
    return {
        messages: ["Test message!", "Other message."],
        url: "/fakeUrl/",
    };
}