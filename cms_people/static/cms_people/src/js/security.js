var disable_password = function(){
    var disable = !$('#id_change_password').is(':checked');
    $('#id_new_password').prop("disabled", disable);
    $('#id_repeat_new_password').prop("disabled", disable);
};

$(function(){
    disable_password();
    $('#id_change_password').on('change', disable_password);
});