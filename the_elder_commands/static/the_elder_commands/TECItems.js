let TECItems = {};


TECItems.initializeItems = function(templateVariable) {

    let tables = TECItems.initializeItemsTables();
    TEC.adjustWrapper();
    TEC.createSubmitButton();
    TECItems.createHideButton();
    TEC.checkForMessages(templateVariable.messages);
    TEC.sendAjaxPOST(tables, templateVariable.url);
    TECItems.hideButton(tables);
    TECItems.reactionToInput(tables);

    return tables
};


TECItems.initializeItemsTables = function() {
    let tableCategories,
        tables = [];

    tableCategories = TECItems.getItems();

    for (let category of tableCategories) {
        tables.push(TEC.initializeDataTable(category));
    }
    return tables;
};



TECItems.createShowButton = function() {
    $(".table_wrapper > div:first-child").after('<div class="col-md-1 col-12"><button type="button" ' +
        'class="btn btn-dark text-info show_all btn-block">Show<br>All</button></div>');
};

TECItems.createHideButton = function() {
    $(".table_wrapper > div:first-child").after('<div class="col-md-1 col-12"><button type="button" ' +
        'class="btn btn-dark text-info hide_not_selected">Hide&nbspNot<br>Selected</button></div>');
};

TECItems.removeHideButton = function() {
    let show = $(".hide_not_selected");
    show.parent().remove();
};

TECItems.removeShowButton = function() {
    let hide = $(".show_all");
    hide.parent().remove();
};

TECItems.hideButton = function(tables) {
    $(".hide_not_selected").click(function () {
        TECItems.removeHideButton();
        TECItems.createShowButton();
        TECItems.showButton(tables);
        TECItems.searchSelected(tables);
    });
};

TECItems.showButton = function(tables) {
    $(".show_all").click(function () {
        TECItems.removeShowButton();
        TECItems.createHideButton();
        TECItems.hideButton(tables);
        TECItems.clearSearch(tables);
    });
};

TECItems.searchSelected = function(tables) {
    for (let table of tables) {
        table.api().search("");
        table.api().column(-1).search("true").draw();
    }
};

TECItems.clearSearch = function(tables) {
    for (let table of tables) {
        table.api().search("");
        table.api().column(-1).search("").draw();
    }
};

TECItems.reactionToInput = function(tables) {
    for (let table of tables) {
        table.on("keyup", "input", function () {
            let inputValue = $(this).closest("tr").find("input").val();
            if (inputValue === "") {
                let row = $(this).parents("tr"),
                col = table.api().column(-1),
                cell = table.api().cell(row, col);
                cell.data("false").draw();
            } else {
                let row = $(this).parents("tr"),
                col = table.api().column(-1),
                cell = table.api().cell(row, col);
                cell.data("true").draw();
            }
            $(this).focus();
        });
    }
}


TECItems.getItems = function() {
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
