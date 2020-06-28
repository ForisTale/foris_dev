class TECSpells extends TEC {
    constructor(templateVariables) {
        super();
        this.initializeSpellsTables();
        this.adjustWrapper();
        this.createSubmitButton();
        this.checkForMessages(templateVariables.messages);
        this.sendAjaxPOST(templateVariables.url);
    }

    initializeSpellsTables() {
        this.tables = []

        for (let category of this.getSpells()) {
            this.tables.push(this.initializeDataTable(category));
        }
    };

    getSpells() {
        return [
            {
                url: `/api/tec/spells/alteration/`,
                tableId: "id_alteration_table",
                fields: [
                    {data: null, render: function (data) {
                        let checked = '';
                        if (data.selected){ checked = 'checked' }
                        return `<label><input type="checkbox" ${checked} name="${data.form_id}"></label>`
                        }},
                    {data: "name"},
                    {data: "mastery"},
                    {data: "plugin_name"},
                    {data: "editor_id"},
                    {data: "form_id"},
                    {data: "effects"},
                ],
            },
            {
                url: `/api/tec/spells/conjuration/`,
                tableId: "id_conjuration_table",
                fields: [
                    {data: null, render: function (data) {
                        let checked = '';
                        if (data.selected){ checked = 'checked' }
                        return `<label><input type="checkbox" ${checked} name="${data.form_id}"></label>`
                        }},
                    {data: "name"},
                    {data: "mastery"},
                    {data: "plugin_name"},
                    {data: "editor_id"},
                    {data: "form_id"},
                    {data: "effects"},
                ],
            },
            {
                url: `/api/tec/spells/destruction/`,
                tableId: "id_destruction_table",
                fields: [
                    {data: null, render: function (data) {
                        let checked = '';
                        if (data.selected){ checked = 'checked' }
                        return `<label><input type="checkbox" ${checked} name="${data.form_id}"></label>`
                        }},
                    {data: "name"},
                    {data: "mastery"},
                    {data: "plugin_name"},
                    {data: "editor_id"},
                    {data: "form_id"},
                    {data: "effects"},
                ],
            },
            {
                url: `/api/tec/spells/illusion/`,
                tableId: "id_illusion_table",
                fields: [
                    {data: null, render: function (data) {
                        let checked = '';
                        if (data.selected){ checked = 'checked' }
                        return `<label><input type="checkbox" ${checked} name="${data.form_id}"></label>`
                        }},
                    {data: "name"},
                    {data: "mastery"},
                    {data: "plugin_name"},
                    {data: "editor_id"},
                    {data: "form_id"},
                    {data: "effects"},
                ],
            },
            {
                url: `/api/tec/spells/restoration/`,
                tableId: "id_restoration_table",
                fields: [
                    {data: null, render: function (data) {
                        let checked = '';
                        if (data.selected){ checked = 'checked' }
                        return `<label><input type="checkbox" ${checked} name="${data.form_id}"></label>`
                        }},
                    {data: "name"},
                    {data: "mastery"},
                    {data: "plugin_name"},
                    {data: "editor_id"},
                    {data: "form_id"},
                    {data: "effects"},
                ],
            },
            {
                url: `/api/tec/spells/wordsofpower/`,
                tableId: "id_wordsofpower_table",
                fields: [
                    {data: null, render: function (data) {
                        let checked = '';
                        if (data.selected){ checked = 'checked' }
                        return `<label><input type="checkbox" ${checked} name="${data.form_id}"></label>`
                        }},
                    {data: "word"},
                    {data: "translation"},
                    {data: "plugin_name"},
                    {data: "editor_id"},
                    {data: "form_id"},
                ],
            },
            {
                url: `/api/tec/spells/other/`,
                tableId: "id_other_table",
                fields: [
                    {data: null, render: function (data) {
                        let checked = '';
                        if (data.selected){ checked = 'checked' }
                        return `<label><input type="checkbox" ${checked} name="${data.form_id}"></label>`
                        }},
                    {data: "name"},
                    {data: "mastery"},
                    {data: "plugin_name"},
                    {data: "editor_id"},
                    {data: "form_id"},
                    {data: "effects"},
                ],
            },
        ];
    };
}