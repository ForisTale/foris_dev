

window.Superlists = {};

window.Superlists.updateItems = (url) => {
    $.get(url).done(function (response) {
        let rows = "";
        for (let i=0; i<response.length; i++) {
            let item = response[i];
            rows += "\n<tr><td>" + (i+1) + ": " + item.text + "</td></tr>";
        }
        $("#id_list_table").html(rows);
    });
};

window.Superlists.initialize = (url) => {
    $('input[name="text"]').on('keypress', function () {
        $('.has-error').hide();
    });

    if (url) {
        window.Superlists.updateItems(url);

        let form = $("#id_item_form");
        form.on("submit", function(event) {
            event.preventDefault();
            $.post(url, {
                "text": form.find("input[name='text']").val(),
                "csrfmiddlewaretoken": form.find("input[name='csrfmiddlewaretoken']").val(),
            }).done(function () {
                window.Superlists.updateItems(url);
            }).fail(function (xhr) {
                $(".has-error").show();
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    $(".has-error .help-block").text(xhr.responseJSON.error);
                } else {
                    $(".has-error .help-block").text("Error talking to server. Please try again later.");
                }
            });
        });
    }
};
