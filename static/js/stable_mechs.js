function check_purchase_form_ready() {
  form = $('#mech-purchase-form');
  submit = form.find('#mech-purchase-submit');

  submit_type = form.find('.mech-purchase-select input:checked').val();

  if (submit_type == 'C') {
    if (form.find('select#id_mech_code').val()) {
      submit.removeAttr('disabled');
    } else {
      submit.attr('disabled','yes');
    }
  } else if (submit_type == 'U') {
    if (form.find('input#id_mech_ssw').val()) {
      submit.removeAttr('disabled');
    } else {
      submit.attr('disabled','yes');
    }
  } else {
    submit.attr('disabled','yes');
  }
}

function refresh_mechlist() {
  $('#stable-mech-list').load(window.location.href + '/list #stable-mech-list'
  , function() {
    $('#stable-mech-list .refit-button').click( show_refit_form );
    $('#stable-mech-list .remove-button').click( show_removal_dialog );
  });
}

function submit_purchase_data(form, mech_data) {
  $.ajax({
    type : 'post'
  , url  : window.location.href + '/purchase'
  , dataType : 'json'
  , contentType : false
  , processData : false
  , data : mech_data
  }).done(function(response) {
    refresh_mechlist();

    if (response['success']) {
      form.find('#id_mech_code').html('')
      form.find('input:not([type=radio])').val('');
    }
  });

  form.find('#mech-purchase-submit').attr('disabled','yes');
}

function show_refit_form() {
  $('#mech_refit_form').slideUp( function() { $(this).remove() } );

  button = $(this);
  refit = button.parents('.mech-body').find('.refit-panel');
  refit.hide().load(button.attr('form_url'), function() { 
    $(this).slideDown() 

    refit.find('#id_add_ledger').change( function () {
      if ($(this).prop('checked')) {
         refit.find('#id_failed_by').removeAttr('disabled');
      } else {
         refit.find('#id_failed_by').attr('disabled','yes');
      }
    });

    refit.find('.action-preview').click( function() {
      radio = $(this).siblings('.mech-source-radio');
      preview_mech(radio.attr('mech_name'), radio.attr('mech_code'));
    });

    refit.find('#refit-button-submit').click( function() {
      var refit_data = new FormData(refit.find('#mech_refit_form')[0]);

      chosen = refit.find('.mech-source-radio:checked');
      if (chosen.val() == 'C') {
        refit_data.append('mech_name', chosen.attr('mech_name'));     
        refit_data.append('mech_code', chosen.attr('mech_code'));
      }  

      $.ajax({
        type : 'post'
      , url  : button.attr('form_url')
      , dataType : 'json'
      , contentType : false
      , processData : false
      , data : refit_data
      }).done(function(response) { 
        refresh_mechlist();
      });
    });
  });
}

function send_removal(submit_url, instruction) {
  $.ajax({
    type : 'post'
  , url  : submit_url
  , dataType : 'json'
  , data : { 'action' : instruction }
  }).done(function(response) { 
    refresh_mechlist();
  });
}

function show_removal_dialog() {
  form_url = $(this).attr("form_url");
  mech_name = $(this).attr("mech_name");

  dialog = $('#dialog-removemech');
  dialog.attr('title', "Remove " + mech_name);
  dialog.find('p').text("Remove " + mech_name + " from your stable?");

  dialog.dialog({
    modal: true,
    width: (window.innerWidth * 0.5),
    buttons: {
      Core   : function() { send_removal(form_url, 'core'); $( this ).dialog("close"); } 
    , Remove : function() { send_removal(form_url, 'remove'); $( this ).dialog("close"); } 
    , Keep   : function() { $( this ).dialog("close"); }
    } 
  });
}

function submit_purchase_form() {
  form = $('#mech-purchase-form');

  submit_type = form.find('.mech-purchase-select input:checked').val();
  if (submit_type == 'C' || submit_type == 'U') {
    var mech_data = new FormData(form[0]);
    mech_data.append('mech_source', submit_type);

    submit_purchase_data(form, mech_data);
  } else {
    //No submit type selected, abandon attempt
    return;
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

    $('.refit-button').click( show_refit_form );
    $('.remove-button').click( show_removal_dialog );
    $('#mech-purchase-submit').click( submit_purchase_form );
});
