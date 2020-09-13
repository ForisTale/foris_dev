let server;

QUnit.testStart(function () {
    server = sinon.fakeServer.create();
});


QUnit.testDone(function () {
    server = sinon.restore();
});


QUnit.test("DataTable initialize for plugins table.", function (assert) {
    let initializedTable = new TECPlugins(),
        table = $("tr", initializedTable.table);
    assert.equal(table.length, 4);
});


QUnit.test("Adjust table wrapper.", function (assert) {
    new TECPlugins();
    let wrapper = $(".dataTables_wrapper:first-child > .row:first-child > div");

    assert.equal(wrapper.length, 3);
    assert.equal(wrapper.hasClass("col-sm-12 col-md-2"), true);
    assert.equal(wrapper.hasClass("col-md-8 col-12"), true);
    assert.equal(wrapper.hasClass("col-sm-12 col-md-2"), true);
});

QUnit.test("Inject submit button into table.", function (assert) {
    new TECPlugins();
    let submit_buttons = $(".table_wrapper > .col-md-2 > .submit_table");

    assert.equal(submit_buttons.length, 1);
});

QUnit.test("Show message in table wrapper.", function (assert) {
    assert.equal(1, 3);
});

QUnit.test("Sending ajax post.", function (assert) {
    assert.equal(1, 3);
});
