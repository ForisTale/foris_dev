
window.TEC = {}
window.TEC.initialize = (params) => {

    let table = window.TEC.initializeDataTable();
    window.TEC.adjustWrapper();
    window.TEC.createSubmitButton();
    window.TEC.sendAjaxPOST(table, params.url);
};


window.TEC.initializeDataTable = () => {
    return $('table').DataTable({
        "createdRow": function (row) {
            $(row).addClass("bg-dark");
        },
        "order": [[1, "asc"]],
        "columnDefs": [{"orderable": false, "targets": 0}],
        "autoWidth": false,
    })
};

window.TEC.adjustWrapper = () => {
    let wrapperCols = $(".dataTables_wrapper > div:nth-child(1) > div");
    wrapperCols.removeClass("col-md-6");
    wrapperCols.addClass("col-md-2");
    let wrapperFirstCols = $(".dataTables_wrapper > div:nth-child(1) > div:first-child");
    wrapperFirstCols.after('<div class="col-md-8 col-12"><div class="row" id="id_wrapper"></div></div>');
}

window.TEC.createSubmitButton = () => {
    $('#id_wrapper').append('<div class="col-1"><button type="submit" name="submit_table" id="id_submit_table" ' +
        'class="btn btn-dark text-info">Generate<br>Commands</button></div>')
};

window.TEC.sendAjaxPOST = (table, url) => {
    $('#id_submit_table').click(function(event) {
        let table_input = table.$('input').serialize();
        event.preventDefault();

        $.ajax({
            type: "POST",
            dataType: "text",
            url: url,
            data: {"csrfmiddlewaretoken": jQuery("[name=csrfmiddlewaretoken]").val(), "table_input": table_input},
        }).done(function (result) {
            window.TEC.createMessage(result);
        }).fail(function () {
            alert("Something went wrong! If the error persists, contact Foris.");
        });
    });
};

window.TEC.createMessage = (result) => {
    let jsonResponse = JSON.parse(result),
        first_part = '<div class=" col-5 alert alert-primary alert-dismissible fade show" role="alert"> <h4><strong>',
        second_part = '</strong></h4> <button type="button" class="close" data-dismiss="alert" ' +
            'aria-label="Close"><span aria-hidden="true">&times;</span></button></div>';
    $("#id_wrapper").append(first_part + jsonResponse.message + second_part).show();
};
