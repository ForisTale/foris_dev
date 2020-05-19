
window.TEC = {}
window.TEC.initialize = (params) => {

    let table = window.TEC.initializeDataTable();

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

window.TEC.createSubmitButton = () => {
    $('div.dataTables_length').html('<button type="submit" name="submit_table" id="id_submit_table" ' +
        'class="btn btn-dark text-info">Generate<br>Commands</button>')
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
        first_part = '<div class="alert alert-primary alert-dismissible fade show" role="alert"> <h4><strong>',
        second_part = '</strong></h4> <button type="button" class="close" data-dismiss="alert" ' +
            'aria-label="Close"><span aria-hidden="true">&times;</span></button></div>';
    $("#id_error_messages").html(first_part + jsonResponse.message + second_part).show();
};


window.TEC_test = {}
