class TEC {
    initializeDataTable(item) {
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

    adjustWrapper() {
        let wrapperCols = $(".dataTables_wrapper > div:nth-child(1) > div");
        wrapperCols.removeClass("col-md-6");
        wrapperCols.addClass("col-md-2");
        let wrapperFirstCols = $(".dataTables_wrapper > div:nth-child(1) > div:first-child");
        wrapperFirstCols.after('<div class="col-md-8 col-12"><div class="row table_wrapper"></div></div>');
    };

    createSubmitButton() {
        $('.table_wrapper').append('<div class="col-md-2 col-12"><button type="button" ' +
            'class="btn btn-dark text-info submit_table">Generate<br>Commands</button></div>');
    };

    createResetButton(type) {
        $('.table_wrapper').append('<div class="col-md-2 col-12"><button type="submit" ' +
            `class="btn btn-dark text-info reset_tables">Reset all<br> ${type}</button></div>`);
    };

    checkForMessages(messages) {
        for (let message of messages) {
            this.createMessage(message);
        }
    };

    createMessage(message) {
        let visibleWrapper = $(".table_wrapper:visible");
        visibleWrapper.append('<div class=" col alert alert-primary alert-dismissible fade show" role="alert"><h4>' +
            `<strong>${message}</strong></h4> <button type="button" class="close" data-dismiss="alert" ` +
            'aria-label="close"><span aria-hidden="true">&times;</span></button></div>').show();
    };

    sendAjaxPOST() {
        let tecThis = this;
        $('.submit_table').click(function() {
            let postData = tecThis.getPostData()

            $.ajax({
                type: "POST",
                dataType: "text",
                url: tecThis.url,
                data: {"csrfmiddlewaretoken": jQuery("[name=csrfmiddlewaretoken]").val(), ...postData},
            }).done(function (result) {
                let templateVariable = JSON.parse(result),
                    message = templateVariable.message;

                tecThis.createMessage(message);
            }).fail(function () {
                console.log("Something went wrong! If the error persists, contact Foris.");
            });
        });
    };

    sendResetPost() {
        let tecThis = this;
        $(".reset_tables").click(function () {
            $.ajax({
                type: "POST",
                dataType: "text",
                url: tecThis.url,
                data: {"csrfmiddlewaretoken": jQuery("[name=csrfmiddlewaretoken]").val(), "reset": ""}
            }).done(function () {
                window.location.replace(tecThis.url);
            });
        });
    };

    getPostData() {
        let table_input = [],
                stringifyInput;
            for (let table of this.tables) {
                table_input = table_input.concat(table.$("input").serializeArray());
            }
            let clearInput = [];
            for (let item of table_input) {
                if (item.value !== "") {
                    clearInput = clearInput.concat(item);
                }
            }

            stringifyInput = JSON.stringify(clearInput)
        return {"table_input": stringifyInput}
    };
}
