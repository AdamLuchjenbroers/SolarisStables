function check_purchase_form_ready() {
  form = $('#mech-purchase-form');
  submit = form.find('#mech-purchase-submit');

  submit_type = form.find('.mech-purchase-select input:checked').val();

  if (submit_type == 'C') {
    if (form.find('#id_mech_code').val()) {
      submit.removeAttr('disabled');
    } else {
      submit.attr('disabled','yes');
    }
  } else if (submit_type == 'U') {
    if (form.find('#id_ssw_mech_code').val()) {
      submit.removeAttr('disabled');
    } else {
      submit.attr('disabled','yes');
    }
  } else {
    submit.attr('disabled','yes');
  }
}

function setup_mechlist_buttons() {
  $('#stable-mech-list .refit-button').click( show_refit_form );
  $('#stable-mech-list .remove-button').click( show_removal_dialog );
  $('#stable-mech-list .edit-button').click( show_edit_form );
  $('#stable-mech-list .loadout-button').click( show_loadout_form );    
}

function refresh_mechlist() {
  $('#stable-mech-list').load(window.location.href + '/list #stable-mech-list', setup_mechlist_buttons);
}

function submit_purchase_data(form, mech_data) {
  $.ajax({
    type : 'post'
  , url  : window.location.href + '/purchase'
  , dataType : 'json'
  , data : mech_data
  }).done(function(response) {
    refresh_mechlist();

    if (response['success']) {
      form.find('#id_mech_code').html('<option value=\"\">--</option>')
      form.find('input:not([type=radio])').val('');
      $('#mech-purchase-custom .mech-purchase-chassis').html('');
      $('#mech-purchase-custom .mech-purchase-model').html('');
      $('#mech-purchase-custom .mech-purchase-cost').html('');
    }

    form.find('#mech-purchase-submit').attr('disabled','yes');
  });

}

function show_refit_form() {
  button = $(this);
  panel = button.parents('.mech-body').find('.refit-panel');

  oldform = $('#mech_refit_form');
  if (oldform.length > 0) {
    // If a form is already active, take care of its removal animation first.
    oldform.slideUp( function() { 
      $(this).remove();
    
      display_refit_form(panel, button);
    });
  } else {
    display_refit_form(panel, button);
  }

}

function display_refit_form(panel, button) {
  panel.hide().load(button.attr('form_url'), function() { 
    panel.slideDown() 

    panel.find('#id_add_ledger').change( function () {
      if ($(this).prop('checked')) {
         panel.find('#id_failed_by').removeAttr('disabled');
      } else {
         panel.find('#id_failed_by').attr('disabled','yes');
      }
    });

    panel.find('.action-preview').click( function() {
      preview_mech($(this).attr('preview_url'));
    });

    $('#refit-button-upload').click( show_refit_upload_dialog );
    $('#refit-button-submit').click( submit_refit_form )
  });
}

function submit_refit_form() {
  chosen = $('#mech_refit_form .mech-source-radio:checked');
  refit_data = {
    'mech_source' : chosen.val()
  , 'mech_name'   : chosen.attr('mech_name')
  , 'mech_code'   : chosen.attr('mech_code')
  , 'omni_loadout' : 'Base'
  , 'failed_by'   : $('#id_failed_by').val()
  , 'add_ledger'  : $('#id_add_ledger').prop('checked')
  } 

  if (chosen.val() == 'U') {
    refit_data['temp_id'] = chosen.attr('temp_id');
  }

  $.ajax({
    type : 'post'
  , url  : $('#mech_refit_form').attr('form_url')
  , dataType : 'json'
  , data : refit_data
  }).done(function(response) { 
    refresh_mechlist();
  });
}

function show_refit_upload_dialog() {
  form_url = $(this).attr('form_url');
  show_upload_dialog( render_refit_purchaseform, form_url );
}

function render_refit_purchaseform( response ) {
  $('#refit-uploaded-mech').remove();
  $('#dialog-uploadmech').dialog("close");
  $('#refit-custom-header').show();

  mech_html = "<li id=\"refit-uploaded-mech\" class=\"hidden\">";
  mech_html += "<input type=\"radio\" name=\"mech_source\" value=\"U\" class=\"mech-source-radio\"";
  mech_html += " mech_name=\"" + response ['mech_name'] + "\""; 
  mech_html += " mech_code=\"" + response ['mech_code'] + "\"";
  mech_html += " temp_id=\"" + response ['temp_id'] + "\">";
  mech_html += "<span class=\"mech-model\">" + response['mech_name'] + " " + response['mech_code'];
  mech_html += "</span></input></li>"; 

  $('#mech_refit_form ul.refit-mechs').append(mech_html);
  $('#refit-uploaded-mech').fadeIn();
}

function show_loadout_form() {
  $('#mech_refit_form').slideUp( function() { $(this).remove() } );

  button = $(this);
  refit = button.parents('.mech-body').find('.refit-panel');
  refit.hide().load(button.attr('form_url'), function() { 
    $(this).slideDown() 

    refit.find('.action-preview').click( function() {
      preview_mech($(this).attr('preview_url'));
    });

    $('#loadout-button-upload').click( show_loadout_upload_dialog );

    $('#loadout-button-submit').click( function() {
      chosen = $('#mech_refit_form .mech-source-radio:checked');
      refit_data = {
        'mech_source' : chosen.val()
      , 'mech_name'   : chosen.attr('mech_name')
      , 'mech_code'   : chosen.attr('mech_code')
      , 'omni_loadout' : chosen.attr('omni_loadout')
      , 'failed_by'   : $('#id_failed_by').val()
      , 'add_ledger'  : $('#id_add_ledger').prop('checked')
      } 

      if (chosen.val() == 'U') {
        refit_data['temp_id'] = chosen.attr('temp_id');
      }  

      $.ajax({
        type : 'post'
      , url  : button.attr('form_url')
      , dataType : 'json'
      , data : refit_data
      }).done(function(response) { 
        refresh_mechlist();
      });
    });
  });
}

function show_loadout_upload_dialog() {
  form_url = $(this).attr('form_url');
  show_upload_dialog( render_loadout_purchaseform, form_url );
}

function render_loadout_purchaseform(response) {
  $('#mech_refit_form ul.refit_mechs li.uploaded').remove();
  $('#dialog-uploadmech').dialog("close");
  $('#loadout-custom-header').show();

  $.each( response['loadouts'], function(loadout, info) {
    mech_html = "<li class=\"hidden uploaded\">";
    mech_html += "<input type=\"radio\" name=\"mech_source\" value=\"U\" class=\"mech-source-radio\"";
    mech_html += " mech_name=\"" + response['mech_name'] + "\""; 
    mech_html += " mech_code=\"" + response['mech_code'] + "\"";
    mech_html += " omni_loadout=\"" + loadout + "\"";
    mech_html += " temp_id=\"" + response['temp_id'] + "\">";
    mech_html += "<span class=\"mech-model\">" + loadout;
    mech_html += "</span></input></li>"; 
  
    $('#mech_refit_form ul.refit-mechs').append(mech_html);
    $('#mech_refit_form li.hidden').fadeIn();
  });
}

function show_edit_form() {
  url = $(this).attr('form_url');
  $('#dialog-editmech').load(url, function() {
    $(this).dialog({
      modal   : true
    , width   : (window.innerWidth * 0.5)
    , buttons : {
        Edit   : submit_edit_form
      , Cancel : function() { $( this ).dialog("close"); }
      } 
    });

    $('#mech-removal-button').click(function() {
      $('#mech-removal-button').fadeOut( function() {
        $('#mech-removal-options').slideDown();
      });
    });

    $('#mech-omniremoval-button').click(function() {
      $('#mech-omniremoval-button').fadeOut();

      $('#edit-mech-form .config-remove').css('display','inline-block').hide().fadeIn();
      $('#edit-mech-form .config-remove').click(remove_config_clicked);
    });
  });
}

function remove_config_clicked() {
  remove_id = $(this).attr('attached');

  $.ajax({
    type : 'post'
  , url  : $(this).attr('remove_url')
  , dataType : 'json'
  , data : { 'remove' : true }
  }).done(function(response) { 
    if (response['success']) {
      $('#' + remove_id).slideUp();
    }	
    
    refresh_mechlist();
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
  var formdata;
    
  form = $('#mech-purchase-form');
  
  submit_type = form.find('.mech-purchase-select input:checked').val();
  if (submit_type == 'C') {
    formdata = form_to_dictionary('#mech-purchase-prod');
    selected = $('#id_mech_code').find(':selected');
  } else if (submit_type == 'U') {
    formdata = form_to_dictionary('#mech-purchase-custom');
    selected = $('#id_ssw_mech_code').find(':selected');
  } else {
    //No submit type selected, abandon attempt
    return;
  }
    
  formdata['mech_source'] = submit_type
  formdata['omni_loadout'] = selected.attr('loadout');
  formdata['as_purchase'] = $('#id_as_purchase').is(':checked'); 
  formdata['delivery'] = $('#id_delivery').val();

  submit_purchase_data(form, formdata);  
}

function submit_edit_form() {
  formdata = form_to_dictionary('#edit-mech-form');
  submit_url = $('#edit-mech-form').attr('action');

  $.ajax({
    type : 'post'
  , url  : submit_url 
  , dataType : 'json'
  , data : formdata
  , statusCode : {
      201 : function() { 
        refresh_mechlist();
        $('#dialog-editmech').dialog('close');
      }
    }
  , complete : function(response, textStatus, xhr) {
      $('#dialog-editmech').html(response);
    }
  });
}

function show_upload_dialog(success_handler, form_url) {
  $('#dialog-uploadmech').load(form_url, function() {
    $(this).dialog({      
      modal   : true
    , width   : '20em'
    , buttons : {
        Upload : function() { upload_mech(success_handler, form_url); }
      , Cancel : function() { $( this ).dialog("close"); }
      } 
    });
  });
}

function show_purchase_upload_dialog() {
  form_url = $(this).attr('form_url');
  show_upload_dialog( render_upload_purchaseform, form_url );
}

function render_upload_purchaseform(response) {
  name_html = response['mech_name'] 
  name_html += '<input type=\"hidden\" name=\"mech_name\" value=\"' + response['mech_name'] + "\"/>"
  name_html += '<input type=\"hidden\" name=\"temp_id\" value=\"' + response['temp_id'] + "\"/>"      
  
  $('#mech-purchase-custom .mech-purchase-chassis').html(name_html);
  
  if ( response['is_omni'] == false) {
    model_html = response['mech_code'];
    model_html += '<input type=\"hidden\" name=\"mech_code\" id=\"id_ssw_mech_code\" ';
    model_html += 'value=\"' + response['mech_code'] + "\"/>";
      
    $('#mech-purchase-custom .mech-purchase-model').html(model_html);
    $('#mech-purchase-custom .mech-purchase-cost').text('-' + response['cost']);
  } else if ( response['num_loadouts'] == 1) {
    loadout = keys(response['loadouts'])[0];
      
    model_html = response['mech_name'] + ' (' + loadout + ')';
    model_html += '<input type=\"hidden\" name=\"mech_code\" id=\"id_ssw_mech_code\" ';
    model_html += 'loadout=\"' + loadout + '\" '
    model_html += 'value=\"' + response['mech_code'] + "\"/>";
    
    $('#mech-purchase-custom .mech-purchase-model').html(model_html);
    $('#mech-purchase-custom .mech-purchase-cost').text('-' + response['cost']);
  } else {
    select_html = "<select id=\"id_ssw_mech_code\" name=\"mech_code\">"
    select_html += "<option value=\"\">--</option>";
    $.each(response['loadouts'], function(config, info) {
      select_html += "<option loadout=\"" + config + "\"" + " value=\"" + response['mech_code'] + "\" ";
      select_html += "cost=\"" + info['cost'] + "\">";
      select_html += response['mech_code'] + ' (' + config + ')</option>';
    });    
    
    select_html += "</select>"
    $('#mech-purchase-custom .mech-purchase-model').html(select_html);
    
    $('#mech-purchase-custom .mech-purchase-model select').change(function() {
      cost = $(this).find(':selected').attr('cost')
      
      if (isNaN(cost)) {
        $('#mech-purchase-custom .mech-purchase-cost').text('');
      } else {
        $('#mech-purchase-custom .mech-purchase-cost').text('-' + cost);
      }
      
    })
  }   

  check_purchase_form_ready();
  $('#dialog-uploadmech').dialog("close");
}

function upload_form_render_errors(response) {
  as_json = $.parseJSON(response.responseText);
  errorlist = ''
    
  $.each(as_json['errors'], function(field, errors) {
    $.each(errors, function(index, error_text) {
      errorlist += '<li>'+ error_text + '</li>'
    });
  });
  
  $('#upload-error-list').html(errorlist);
  $('#dialog-uploadmech .form_error').show();
}

function upload_mech(success_handler, form_url) {
  mechform = new FormData($('#dialog-uploadmech form')[0]);  
  
  $.ajax({
      url: form_url
    , type: 'post'
    , data: mechform
    , dataType : 'json'
    , processData: false
    , contentType: false
    , statusCode : {
        400: upload_form_render_errors
      }
  }).done( success_handler );
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

    $('#id_allmechs').change( function() {
      if ($('#id_allmechs:checked').length > 0) {
        $('#id_delivery').val(3);
      } else {
        $('#id_delivery').val(1);
      }

      attach_mechlist_autocomplete( 
        $('#mech-purchase-prod .mech-purchase-chassis input')
      , '#mech-purchase-prod'
      , '.mech-purchase-model select' 
      );
    });

    $('#mech-purchase-prod .mech-purchase-model select').change( check_purchase_form_ready );
    $('#mech-purchase-form .mech-purchase-select input').change( check_purchase_form_ready );
    $('#mech-purchase-form input#id_mech_ssw').change( check_purchase_form_ready );

    setup_mechlist_buttons();

    $('#mech-purchase-submit').click( submit_purchase_form );
    $('#mech-purchase-upload').click( show_purchase_upload_dialog );
});
