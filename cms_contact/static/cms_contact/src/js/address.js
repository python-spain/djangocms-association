function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrfToken);
        }
    }
});

$(function () {
    $('#id_city').on('select2:select', function () {
        $.post(dataType, {city: $('#id_city').val()}, function(data){
            $.each(data, function(key, value){
                $('#id_' + key.toLowerCase()).append('<option value="' + value.id +
                                                     '" selected="selected">' + value.name + '</option>')
            });
        });
    });
});