
window.TEC = {};


window.TEC.initialize = function(templateVariable) {

    let tables = this.initializeDataTables();
    this.adjustWrapper();
    this.createSubmitButton();
    this.checkForMessages(templateVariable.messages)
    this.sendAjaxPOST(tables, templateVariable.url)
    return tables
};


window.TEC.initializeDataTables = function() {
    let items = this.getItems(),
        tables = [];

    for (let item of items) {
        tables.push(this.initializeDataTable(item));
    }
    return tables;
};


window.TEC.initializeDataTable = function(item) {
    return $(`#${item.tableId}`).dataTable({
            ajax:{
                url: item.url,
                dataSrc: "",
                cache: true,
            },
            "columns": item.fields,
            "createdRow": function (row) {
                $(row).addClass("bg-dark");
            },
            "order": [[1, "asc"]],
            "columnDefs": [{"orderable": false, "targets": 0},],
            "autoWidth": false,
        });
};


window.TEC.adjustWrapper = function() {
    let wrapperCols = $(".dataTables_wrapper > div:nth-child(1) > div");
    wrapperCols.removeClass("col-md-6");
    wrapperCols.addClass("col-md-2");
    let wrapperFirstCols = $(".dataTables_wrapper > div:nth-child(1) > div:first-child");
    wrapperFirstCols.after('<div class="col-md-8 col-12"><div class="row table_wrapper"></div></div>');
};


window.TEC.createSubmitButton = function() {
    $('.table_wrapper').append('<div class="col-1"><button type="submit" name="submit_table" ' +
        'class="btn btn-dark text-info submit_table">Generate<br>Commands</button></div>');
};


window.TEC.checkForMessages = function(messages) {
    for (let message of messages) {
        this.createMessage(message);
    }
};


window.TEC.createMessage = function(message) {
    let visibleWrapper = $(".table_wrapper:visible");
    visibleWrapper.append('<div class=" col-5 alert alert-primary alert-dismissible fade show" role="alert"><h4>' +
        `<strong>${message}</strong></h4> <button type="button" class="close" data-dismiss="alert" ` +
        'aria-label="close"><span aria-hidden="true">&times;</span></button></div>').show();
};


window.TEC.sendAjaxPOST = function(tables, url) {
    $('.submit_table').click(function() {
        let table_input = [],
            stringifyInput;
        for (let table of tables) {
            table_input = table_input.concat(table.$("input").serializeArray());
        }
        let clearInput = [];
        for (let item of table_input) {
            if (item.value !== "") {
                clearInput = clearInput.concat(item);
            }
        }

        stringifyInput = JSON.stringify(clearInput)

        $.ajax({
            type: "POST",
            dataType: "text",
            url: url,
            data: {"csrfmiddlewaretoken": jQuery("[name=csrfmiddlewaretoken]").val(), "table_input": stringifyInput},
        }).done(function (result) {
            let templateVariable = JSON.parse(result),
                message = templateVariable.message;

            window.TEC.createMessage(message);
        }).fail(function () {
            console.log("Something went wrong! If the error persists, contact Foris.");
        });
    });
};


window.TEC.getItems = function() {
    return [
        {
            url: `/api/tec/items/WEAP/`,
            tableId: "id_weapons_table",
            fields: [{data: null, "render": function (data) {
                         return '<label><input type="text" name="' + data.formId +
                             '" value="' + data.quantity + '"></label>';
                         }},
                 {data: "fullName"},
                 {data: "Damage"},
                 {data: "Value"},
                 {data: "Type"},
                 {data: "Weight"},
                 {data: "plugin_name"},
                 {data: "editorId"},
                 {data: "formId"},
                 {data: "Description"},
                 {data: "selected", visible: false}],
        },
        {
            url: `/api/tec/items/ARMO/`,
            tableId: "id_armors_table",
            fields: [{data: null, "render": function (data) {
                         return '<label><input type="text" name="' + data.formId +
                             '" value="' + data.quantity + '"></label>';
                         }},
                 {data: "fullName"},
                 {data: "Armor rating"},
                 {data: "Armor type"},
                 {data: "Value"},
                 {data: "Weight"},
                 {data: "plugin_name"},
                 {data: "editorId"},
                 {data: "formId"},
                 {data: "Description"},
                 {data: "selected", visible: false}],
        },
        {
            url: `/api/tec/items/AMMO/`,
            tableId: "id_ammo_table",
            fields: [{data: null, "render": function (data) {
                         return '<label><input type="text" name="' + data.formId +
                             '" value="' + data.quantity + '"></label>';
                         }},
                 {data: "fullName"},
                 {data: "Damage"},
                 {data: "Value"},
                 {data: "plugin_name"},
                 {data: "editorId"},
                 {data: "formId"},
                 {data: "selected", visible: false}],
        },
        {
            url: `/api/tec/items/BOOK/`,
            tableId: "id_books_table",
            fields: [{data: null, "render": function (data) {
                         return '<label><input type="text" name="' + data.formId +
                             '" value="' + data.quantity + '"></label>';
                         }},
                 {data: "fullName"},
                 {data: "Value"},
                 {data: "Weight"},
                 {data: "plugin_name"},
                 {data: "editorId"},
                 {data: "formId"},
                 {data: "selected", visible: false}],
        },
        {
            url: `/api/tec/items/INGR/`,
            tableId: "id_ingredients_table",
            fields: [{data: null, "render": function (data) {
                         return '<label><input type="text" name="' + data.formId +
                             '" value="' + data.quantity + '"></label>';
                         }},
                 {data: "fullName"},
                 {data: "Value"},
                 {data: "Weight"},
                 {data: "plugin_name"},
                 {data: "editorId"},
                 {data: "formId"},
                 {data: "Effects"},
                 {data: "selected", visible: false}],
        },
        {
            url: `/api/tec/items/ALCH/`,
            tableId: "id_alchemy_table",
            fields: [{data: null, "render": function (data) {
                         return '<label><input type="text" name="' + data.formId +
                             '" value="' + data.quantity + '"></label>';
                         }},
                 {data: "fullName"},
                 {data: "Value"},
                 {data: "Weight"},
                 {data: "plugin_name"},
                 {data: "editorId"},
                 {data: "formId"},
                 {data: "Effects"},
                 {data: "selected", visible: false}],
        },
        {
            url: `/api/tec/items/SCRL/`,
            tableId: "id_scrolls_table",
            fields: [{data: null, "render": function (data) {
                         return '<label><input type="text" name="' + data.formId +
                             '" value="' + data.quantity + '"></label>';
                         }},
                 {data: "fullName"},
                 {data: "Value"},
                 {data: "Weight"},
                 {data: "plugin_name"},
                 {data: "editorId"},
                 {data: "formId"},
                 {data: "Effects"},
                 {data: "selected", visible: false}],
        },
        {
            url: `/api/tec/items/SLGM/`,
            tableId: "id_soulgems_table",
            fields: [{data: null, "render": function (data) {
                         return '<label><input type="text" name="' + data.formId +
                             '" value="' + data.quantity + '"></label>';
                         }},
                 {data: "fullName"},
                 {data: "Value"},
                 {data: "Weight"},
                 {data: "plugin_name"},
                 {data: "editorId"},
                 {data: "formId"},
                 {data: "selected", visible: false}],
        },
        {
            url: `/api/tec/items/KEYM/`,
            tableId: "id_keys_table",
            fields: [{data: null, "render": function (data) {
                         return '<label><input type="text" name="' + data.formId +
                             '" value="' + data.quantity + '"></label>';
                         }},
                 {data: "fullName"},
                 {data: "Value"},
                 {data: "Weight"},
                 {data: "plugin_name"},
                 {data: "editorId"},
                 {data: "formId"},
                 {data: "selected", visible: false}],
        },
        {
            url: `/api/tec/items/MISC/`,
            tableId: "id_miscellaneous_table",
            fields: [{data: null, "render": function (data) {
                         return '<label><input type="text" name="' + data.formId +
                             '" value="' + data.quantity + '"></label>';
                         }},
                 {data: "fullName"},
                 {data: "Value"},
                 {data: "Weight"},
                 {data: "plugin_name"},
                 {data: "editorId"},
                 {data: "formId"},
                 {data: "selected", visible: false}],
        },
    ];
};
