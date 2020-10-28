class TECPlugins extends TEC {
    constructor(templateVariables) {
        super();
        this.url = templateVariables.url;
        this.initializePluginsTable();
        this.adjustWrapper();
        this.injectSubmitButton();
        this.checkForMessages(templateVariables.messages);
        this.sendAjaxPOST();

    }


    initializePluginsTable = () => {
        this.table = $("#id_plugins_table").dataTable({
            "createdRow": (row) => {
                $(row).addClass("bg-dark");
            },
        });
    };

    injectSubmitButton = () => {
         $('.table_wrapper').append('<div class="col-md-2 col-12"><button type="button" ' +
            'class="btn btn-dark text-info submit_table">Submit<br>Plugins</button></div>');
    };

    getPostData = () => {
        let selector_selected_plugins = this.table.$("[name=selected]"),
            selected_plugins = [],
            table_input = [],
            stringifyInput;

        for (let selector of selector_selected_plugins) {
            if (selector.checked) {
                selected_plugins.push(selector.value);
            }

        }

        for (let plugin of selected_plugins) {
            table_input.push({
                "name": plugin,
                "variant": this.getVariant(plugin),
                "load_order": this.getLoadOrder(plugin),
            })
        }

        stringifyInput =JSON.stringify(table_input);
        return {"selected_plugins": stringifyInput};
    }

    ajaxDone = () => {
        location.reload();
    }

    getVariant = (plugin_name) => {
        let variantSelector = this.table.$(`[name=${plugin_name}_variant]`);
        return variantSelector.val();
    }


    getLoadOrder = (plugin_name) => {
        let loadOrderSelector = this.table.$(`[name=${plugin_name}_load_order]`);
        return loadOrderSelector.val();
    }
}