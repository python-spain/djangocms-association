
$('.avatar').on('click', function () {
    $('#id_avatar').click();
});

function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('.avatar div').attr('style', 'background-image: url(' + e.target.result + ')');
            $('.avatar .glyphicon').hide();
        };

        reader.readAsDataURL(input.files[0]);
    }
}

$("#id_avatar").change(function(){
    readURL(this);
});

var $formset = $("#formset");

$formset.formset({
    animateForms: false
});

$.each($formset.find('[name$="type"]'), function(key, select) {
    var $select = $(select);
    $select.select2();
});
