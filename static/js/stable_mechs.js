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
      form.find('input:not([type=radio])').val('C');
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
      preview_mech($(this).attr('preview_url'));
    });

    refit.find('#refit-button-submit').click( function() {
      var refit_data = new FormData(refit.find('#mech_refit_form')[0]);

      chosen = refit.find('.mech-source-radio:checked');
      if (chosen.val() == 'C') {
        refit_data.append('omni_loadout', chosen.attr('omni_loadout')); 
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

function show_loadout_form() {
  $('#mech_refit_form').slideUp( function() { $(this).remove() } );

  button = $(this);
  refit = button.parents('.mech-body').find('.refit-panel');
  refit.hide().load(button.attr('form_url'), function() { 
    $(this).slideDown() 

    refit.find('.action-preview').click( function() {
      preview_mech($(this).attr('preview_url'));
    });

    refit.find('#loadout-button-submit').click( function() {
      chosen = refit.find('.mech-source-radio:checked');
      if (chosen.val() == 'C') {
        refit_data = {
          mech_source  : 'C'
        , omni_loadout : chosen.attr('omni_loadout')
        , mech_name    : chosen.attr('mech_name')
        , mech_code    : chosen.attr('mech_code')
        , add_ledger   : $('#id_add_ledger').prop('checked')
        }
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

function show_upload_dialog() {
  $('#dialog-uploadmech').load($(this).attr('form_url'), function() {
    $(this).dialog({      
      modal   : true
    , width   : '20em'
    , buttons : {
        Upload : upload_mech
      , Cancel : function() { $( this ).dialog("close"); }
      } 
    });
  });
}

function upload_mech() {
  mechform = new FormData($('#dialog-uploadmech form')[0]);  
  
  $.ajax({
      url: $('#dialog-uploadmech form').attr('action')
    , type: 'post'
    , data: mechform
    , dataType : 'json'
    , processData: false
    , contentType: false
    , statusCode : {
        400: function(response) {
          as_json = $.parseJSON(response.responseText);
          errorlist = ''
            
          $.each(as_json['errors'], function(field, errors) {
            $.each(errors, function(index, error_text) {
              errorlist += '<ul><em>' + field + ':</em> ' + error_text + '</ul>'
            });
          });
          
          $('#upload-error-list').html(errorlist);
          $('#dialog-uploadmech .form_error').show();
        }
      }
  }).done( function( response ) {
      name_html = response['mech_name'] 
      name_html += '<input type=\"hidden\" name=\"mech_name\" value=\"' + response['mech_name'] + "\"/>"
      name_html += '<input type=\"hidden\" name=\"temp_id\" value=\"' + response['temp_id'] + "\"/>"      
      
      $('#mech-purchase-custom .mech-purchase-chassis').html(name_html);
      
      if ( response['is_omni'] == false) {
        model_html = response['mech_name'];
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
          
          check_purchase_form_ready();
        })
      }   
    
      $('#dialog-uploadmech').dialog("close");
  });
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
    $('#mech-purchase-upload').click( show_upload_dialog );
});
