class TECPlugins extends TEC {
    constructor() {
        super();
        this.initializePluginsTable();
        this.adjustWrapper();
        this.injectSubmitButton()
    }


    initializePluginsTable () {
        this.table = $("#id_plugins_table").dataTable({
            "createdRow": function (row) {
                $(row).addClass("bg-dark");
            },
        });
    };

    injectSubmitButton () {
         $('.table_wrapper').append('<div class="col-md-2 col-12"><button type="button" ' +
            'class="btn btn-dark text-info submit_table">Submit<br>Plugins</button></div>');
    };

}