
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

formset = $formset.formset('getOrCreate');

$formset.on('change', function(){
    // Add a empty
    var hasEmpty = false;
    $.each(formset.$forms(), function(i, form){
        if($(form).is('[data-formset-form-deleted]')){
            return
        }
        if(!$('select', form).val() && !$('input[type=text]', form).val()){
            hasEmpty = true;
        }
    });
    if(!hasEmpty){
        formset.addForm();
    }
});

$formset.on('formAdded', function (ev) {
    formSelect2(ev.target);
});

function formSelect2(form){
    var select = $(form).find('[name$="type"]');
    var $select = $(select);
    $select.select2({theme: "bootstrap", templateResult: formatState, templateSelection: formatState});
}

function formatState (state) {
  if (!state.id) { return state.text; }
  var $state = $(
    '<span><img src="' + STATIC_URL + '/cms_contact/src/img/' + state.element.value.toLowerCase() + '.png" class="img-flag"' +
    ' /> ' + state.text + '</span>'
  );
  return $state;
}
