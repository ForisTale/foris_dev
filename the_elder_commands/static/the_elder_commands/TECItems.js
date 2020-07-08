class TECItems extends TEC{
    constructor(templateVariables) {
        super();
        this.url = templateVariables.url;
        this.initializeItemsTables();
        this.adjustWrapper();
        this.createSubmitButton();
        this.createResetButton();
        this.createHideButton();
        this.checkForMessages(templateVariables.messages);
        this.sendAjaxPOST();
        this.sendResetPost();
        this.hideButton();
        this.reactionToInput();
    };

    initializeItemsTables() {
        this.tables = [];

        for (let category of this.getItems()) {
            this.tables.push(this.initializeDataTable(category));
        }
    };

    hideButton() {
        let tecThis = this;
        $(".hide_not_selected").click(function () {
            tecThis.removeHideButton();
            tecThis.createShowButton();
            tecThis.showButton();
            tecThis.searchSelected();
        });
    };

    showButton() {
        let tecThis = this;
        $(".show_all").click(function () {
            tecThis.removeShowButton();
            tecThis.createHideButton();
            tecThis.hideButton();
            tecThis.clearSearch();
        });
    };

    createShowButton() {
        $(".table_wrapper > div:first-child").after('<div class="col-md-1 col-12"><button type="button" ' +
            'class="btn btn-dark text-info show_all btn-block">Show<br>All</button></div>');
    };

    createHideButton() {
        $(".table_wrapper > div:first-child").after('<div class="col-md-1 col-12"><button type="button" ' +
            'class="btn btn-dark text-info hide_not_selected">Hide&nbspNot<br>Selected</button></div>');
    };

    removeHideButton() {
        let show = $(".hide_not_selected");
        show.parent().remove();
    };

    removeShowButton() {
        let hide = $(".show_all");
        hide.parent().remove();
    };

    searchSelected() {
        for (let table of this.tables) {
            table.api().search("");
            table.api().column(-1).search("true").draw();
        }
    };

    clearSearch() {
        for (let table of this.tables) {
            table.api().search("");
            table.api().column(-1).search("").draw();
        }
    };

    reactionToInput() {
        for (let table of this.tables) {
            table.on("keyup", "input", function () {
                let input = $(this).closest("tr").find("input"),
                    inputValue = input.val();
                if (inputValue === "") {
                    let row = $(this).parents("tr"),
                    col = table.api().column(-1),
                    cell = table.api().cell(row, col);
                    cell.data("false");
                } else {
                    let row = $(this).parents("tr"),
                    col = table.api().column(-1),
                    cell = table.api().cell(row, col);
                    cell.data("true");
                }
                input.focus();
            });
        }
    }

    getItems() {
        return [
            {
                url: `/api/tec/items/WEAP/`,
                tableId: "id_weapons_table",
                fields: [{data: null, render: function (data) {
                             return '<label><input type="text" name="' + data.form_id +
                                 '" value="' + data.quantity + '"></label>';
                             }},
                     {data: "name"},
                     {data: "damage"},
                     {data: "value"},
                     {data: "type"},
                     {data: "weight"},
                     {data: "plugin_name"},
                     {data: "editor_id"},
                     {data: "form_id"},
                     {data: "description"},
                     {data: "selected", visible: false}],
            },
            {
                url: `/api/tec/items/ARMO/`,
                tableId: "id_armors_table",
                fields: [{data: null, render: function (data) {
                             return '<label><input type="text" name="' + data.form_id +
                                 '" value="' + data.quantity + '"></label>';
                             }},
                     {data: "name"},
                     {data: "armor_rating"},
                     {data: "armor_type"},
                     {data: "value"},
                     {data: "weight"},
                     {data: "plugin_name"},
                     {data: "editor_id"},
                     {data: "form_id"},
                     {data: "description"},
                     {data: "selected", visible: false}],
            },
            {
                url: `/api/tec/items/AMMO/`,
                tableId: "id_ammo_table",
                fields: [{data: null, render: function (data) {
                             return '<label><input type="text" name="' + data.form_id +
                                 '" value="' + data.quantity + '"></label>';
                             }},
                     {data: "name"},
                     {data: "damage"},
                     {data: "value"},
                     {data: "plugin_name"},
                     {data: "editor_id"},
                     {data: "form_id"},
                     {data: "selected", visible: false}],
            },
            {
                url: `/api/tec/items/BOOK/`,
                tableId: "id_books_table",
                fields: [{data: null, render: function (data) {
                             return '<label><input type="text" name="' + data.form_id +
                                 '" value="' + data.quantity + '"></label>';
                             }},
                     {data: "name"},
                     {data: "value"},
                     {data: "weight"},
                     {data: "plugin_name"},
                     {data: "editor_id"},
                     {data: "form_id"},
                     {data: "selected", visible: false}],
            },
            {
                url: `/api/tec/items/INGR/`,
                tableId: "id_ingredients_table",
                fields: [{data: null, render: function (data) {
                             return '<label><input type="text" name="' + data.form_id +
                                 '" value="' + data.quantity + '"></label>';
                             }},
                     {data: "name"},
                     {data: "value"},
                     {data: "weight"},
                     {data: "plugin_name"},
                     {data: "editor_id"},
                     {data: "form_id"},
                     {data: "effects"},
                     {data: "selected", visible: false}],
            },
            {
                url: `/api/tec/items/ALCH/`,
                tableId: "id_alchemy_table",
                fields: [{data: null, render: function (data) {
                             return '<label><input type="text" name="' + data.form_id +
                                 '" value="' + data.quantity + '"></label>';
                             }},
                     {data: "name"},
                     {data: "value"},
                     {data: "weight"},
                     {data: "plugin_name"},
                     {data: "editor_id"},
                     {data: "form_id"},
                     {data: "effects"},
                     {data: "selected", visible: false}],
            },
            {
                url: `/api/tec/items/SCRL/`,
                tableId: "id_scrolls_table",
                fields: [{data: null, render: function (data) {
                             return '<label><input type="text" name="' + data.form_id +
                                 '" value="' + data.quantity + '"></label>';
                             }},
                     {data: "name"},
                     {data: "value"},
                     {data: "weight"},
                     {data: "plugin_name"},
                     {data: "editor_id"},
                     {data: "form_id"},
                     {data: "effects"},
                     {data: "selected", visible: false}],
            },
            {
                url: `/api/tec/items/SLGM/`,
                tableId: "id_soulgems_table",
                fields: [{data: null, render: function (data) {
                             return '<label><input type="text" name="' + data.form_id +
                                 '" value="' + data.quantity + '"></label>';
                             }},
                     {data: "name"},
                     {data: "value"},
                     {data: "weight"},
                     {data: "plugin_name"},
                     {data: "editor_id"},
                     {data: "form_id"},
                     {data: "selected", visible: false}],
            },
            {
                url: `/api/tec/items/KEYM/`,
                tableId: "id_keys_table",
                fields: [{data: null, render: function (data) {
                             return '<label><input type="text" name="' + data.form_id +
                                 '" value="' + data.quantity + '"></label>';
                             }},
                     {data: "name"},
                     {data: "value"},
                     {data: "weight"},
                     {data: "plugin_name"},
                     {data: "editor_id"},
                     {data: "form_id"},
                     {data: "selected", visible: false}],
            },
            {
                url: `/api/tec/items/MISC/`,
                tableId: "id_miscellaneous_table",
                fields: [{data: null, render: function (data) {
                             return '<label><input type="text" name="' + data.form_id +
                                 '" value="' + data.quantity + '"></label>';
                             }},
                     {data: "name"},
                     {data: "value"},
                     {data: "weight"},
                     {data: "plugin_name"},
                     {data: "editor_id"},
                     {data: "form_id"},
                     {data: "selected", visible: false}],
            },
        ];
    };
}
