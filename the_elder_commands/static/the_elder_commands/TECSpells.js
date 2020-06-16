let TECSpells = {};


TECSpells.initializeSpells = function () {
    this.initializeSpellsTables();
};


TECSpells.initializeSpellsTables = function () {
    let spellsCategories = this.getSpells();

    for (let category of spellsCategories) {
        TEC.initializeDataTable(category);
    }

};


TECSpells.getSpells = function () {
    return [
        {
            url: `/api/tec/spells/alteration/`,
            tableId: "id_alteration_table",
            fields: [
                {data: "selected"},
                {data: "fullName"},
                {data: "mastery"},
                {data: "plugin_name"},
                {data: "editorId"},
                {data: "formId"},
                {data: "Effect"},
            ],
        },
        {
            url: `/api/tec/spells/conjuration/`,
            tableId: "id_conjuration_table",
            fields: [
                {data: "selected"},
                {data: "fullName"},
                {data: "mastery"},
                {data: "plugin_name"},
                {data: "editorId"},
                {data: "formId"},
                {data: "Effect"},
            ],
        },
        {
            url: `/api/tec/spells/destruction/`,
            tableId: "id_destruction_table",
            fields: [
                {data: "selected"},
                {data: "fullName"},
                {data: "mastery"},
                {data: "plugin_name"},
                {data: "editorId"},
                {data: "formId"},
                {data: "Effect"},
            ],
        },
        {
            url: `/api/tec/spells/illusion/`,
            tableId: "id_illusion_table",
            fields: [
                {data: "selected"},
                {data: "fullName"},
                {data: "mastery"},
                {data: "plugin_name"},
                {data: "editorId"},
                {data: "formId"},
                {data: "Effect"},
            ],
        },
        {
            url: `/api/tec/spells/restoration/`,
            tableId: "id_restoration_table",
            fields: [
                {data: "selected"},
                {data: "fullName"},
                {data: "mastery"},
                {data: "plugin_name"},
                {data: "editorId"},
                {data: "formId"},
                {data: "Effect"},
            ],
        },
        {
            url: `/api/tec/spells/wordsofpower/`,
            tableId: "id_wordsofpower_table",
            fields: [
                {data: "selected"},
                {data: "word"},
                {data: "translation"},
                {data: "plugin_name"},
                {data: "editorId"},
                {data: "formId"},
            ],
        },
        {
            url: `/api/tec/spells/other/`,
            tableId: "id_other_table",
            fields: [
                {data: "selected"},
                {data: "fullName"},
                {data: "mastery"},
                {data: "plugin_name"},
                {data: "editorId"},
                {data: "formId"},
                {data: "Effect"},
            ],
        },
    ];
};
