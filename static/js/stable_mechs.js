function check_purchase_form_ready() {
  form = $('#mech-purchase-form');
  submit = form.find('#mech-purchase-submit');

  submit_type = form.find('.mech-purchase-select input:checked').val();

  if (submit_type == 'C') {
    if (form.find('select#id_mech_code').val() != "") {
      submit.removeAttr('disabled');
    } else {
      submit.attr('disabled','yes');
    }
  } else if (submit_type == 'U') {
    if (form.find('input#id_mech_ssw').val() != "") {
      submit.removeAttr('disabled');
    } else {
      submit.attr('disabled','yes');
    }
  } else {
    submit.attr('disabled','yes');
  }
}

function submit_purchase_form() {
  form = $('#mech-purchase-form');

  submit_type = form.find('.mech-purchase-select input:checked').val();
  if (submit_type = 'C') {
    $.ajax({
      type : 'post'
    , url  : window.location.href + '/purchase'
    , dataType : 'json'
    , data : {
        mech_source : 'C'
      , mech_name   : form.find('#id_mech_name').val()
      , mech_code   : form.find('#id_mech_code').val()
      , as_purchase : form.find('#id_as_purchase').is(':checked')
      },
    }).done(function(response) {
      window.location.reload(true);
    });
  }
}

$( document ).ready(function() {

    attach_mechlist_autocomplete( 
      $('#mech-purchase-prod .mech-purchase-chassis input')
    , '#mech-purchase-prod'
    , '.mech-purchase-model select' 
    );

    $('#mech-purchase-prod .mech-purchase-model select').change(
      select_chassis_handler(
        '#mech-purchase-prod'
      , '.mech-purchase-chassis input'
      , '.mech-purchase-cost'
      , '.mech-purchase-preview .word-button'
      )
    );

    $('#mech-purchase-prod .mech-purchase-model select').change( check_purchase_form_ready );
    $('#mech-purchase-form .mech-purchase-select input').change( check_purchase_form_ready );
    $('#mech-purchase-form input#id_mech_ssw').change( check_purchase_form_ready );

    $('#mech-purchase-submit').click( submit_purchase_form );
});
