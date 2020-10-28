class TECOther extends TEC {
    constructor(templateVariables) {
        super();
        this.url = templateVariables.url;
        this.initializeOtherTables();
        this.adjustWrapper();
        this.modifyVarietyTableWrapper();
        this.modifyLocationsTableWrapper();
        this.createSubmitButton();
        this.createResetButton("Others");
        this.checkForMessages(templateVariables.messages);
        this.sendAjaxPOST();
        this.sendResetPost();
    }

    initializeOtherTables = () => {
        this.tables = [];

        this.tables.push(this.initializeVarietyTable());
        this.tables.push(this.initializeLocationTable());

        for (let category of this.getOthers()) {
            this.tables.push(this.initializeDataTable(category));
        }
    };

    initializeVarietyTable = () => {
        return $("#id_variety_table").dataTable({
            "createdRow": (row) => {
                $(row).addClass("bg-dark");
            },
            "order": [[1, "asc"]],
            "columnDefs": [{"orderable": false, "targets": [0, 1]},],
            searching: false,
            paging: false,
            info: false,
        })
    };

    initializeLocationTable = () => {
        return $("#id_locations_table").dataTable({
            "createdRow": (row) => {
                $(row).addClass("bg-dark");
            },
            "columnDefs": [{"orderable": false, "targets": [0, 1]},],
        })
    };

    modifyVarietyTableWrapper = () => {
        let tableWrapper = $("#id_variety_table_wrapper > div:first-child");
        tableWrapper.empty();
        tableWrapper.append('<div class="col"><div class="row table_wrapper"></div></div>');
        tableWrapper.after('<div class="row row-separator"></div>');
        tableWrapper.after('<div class="row row-separator"></div>');
    };

    modifyLocationsTableWrapper = () => {
        let tableWrapper = $("#id_locations_table_wrapper > div:first-child > div:nth-child(2) > div:first-child");
        tableWrapper.removeClass("table_wrapper");
    };

    getOthers = () => {
        return [
            {
                url: `/api/tec/wordsofpower/`,
                tableId: "id_wordsofpower_table",
                fields: [
                    {data: null, render: function (data) {
                        let checked = '';
                        if (data.selected){ checked = 'checked' }
                        return `<label><input type="checkbox" ${checked} name="word${data.form_id}"></label>`
                        }},
                    {data: "word"},
                    {data: "translation"},
                    {data: "plugin_name"},
                    {data: "editor_id"},
                    {data: "form_id"},
                ],
            },
            {
                url: `/api/tec/perks/`,
                tableId: "id_perks_table",
                fields: [
                    {data: null, render: function (data) {
                        let checked = '';
                        if (data.selected){ checked = 'checked' }
                        return `<label><input type="checkbox" ${checked} name="perk${data.form_id}"></label>`
                        }},
                    {data: "name"},
                    {data: "plugin_name"},
                    {data: "editor_id"},
                    {data: "form_id"},
                    {data: "description"},
                ],
            },
        ];
    };
}