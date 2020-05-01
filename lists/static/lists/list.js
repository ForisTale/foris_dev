

window.Superlists = {};

window.Superlists.updateItems = (url) => {
    $.get(url).done(function (response) {
        if (!response.items){return;}
        let rows = "";
        for (let i=0; i<response.items.length; i++) {
            let item = response.items[i];
            rows += "\n<tr><td>" + (i+1) + ": " + item.text + "</td></tr>";
        }
        $("#id_list_table").html(rows);
    });
};

window.Superlists.initialize = (params) => {
    $('input[name="text"]').on('keypress', function () {
        $('.has-error').hide();
    });

    if (params) {
        window.Superlists.updateItems(params.listApiUrl);

        let form = $("#id_item_form");

        form.on("submit", function(event) {
            event.preventDefault();
            $.post(params.itemsApiUrl, {
                "list": params.listId,
                "text": form.find("input[name='text']").val(),
                "csrfmiddlewaretoken": form.find("input[name='csrfmiddlewaretoken']").val(),
            }).done(function () {
                form.find("input[name='text']").val("");
                window.Superlists.updateItems(params.listApiUrl);
            }).fail(function (xhr) {
                $(".has-error").show();
                if (xhr.responseJSON) {
                    $(".has-error .help-block").text(xhr.responseJSON.error || xhr.responseJSON.non_field_errors);
                } else {
                    $(".has-error .help-block").text("Error talking to server. Please try again later.");
                }
            });
        });
    }
};
