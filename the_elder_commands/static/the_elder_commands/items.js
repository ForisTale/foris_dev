
window.TEC = {}

window.TEC.getMessages = (result) => {
    let jsonResponse = JSON.parse(result);
    $("#id_error_messages").html(jsonResponse.message).show();
}

window.TEC.initialize = (params) => {

    let table = $('table').DataTable({
        "createdRow": function(row) {
            $(row).addClass("bg-dark");
        },
        "order": [[1, "asc"]],
        "columnDefs": [{"orderable": false, "targets": 0}],
    });

    $('div.dataTables_length').html('<button type="submit" name="submit_table" id="id_submit_table" ' +
        'class="btn btn-dark text-info">Generate<br>Commands</button>')

    $('#id_submit_table').click(function(event) {
        let table_input = table.$('input').serialize();
        event.preventDefault();

        $.ajax({
            type: "POST",
            dataType: "text",
            url: params.url,
            data: {"csrfmiddlewaretoken": jQuery("[name=csrfmiddlewaretoken]").val(), "table_input": table_input},
        }).done(function (result) {
            window.TEC.getMessages(result);
        }).fail(function () {
            alert("Something went wrong! If the error persists, contact Foris.");
        });
    });
};

