function check_tp_assignment() {
  tp_check('#training-contender-tp','#training-contender-assigned', '[rank=contender]', '#training-contender-warning', 'You\'ve assigned more training points to your contenders than your stable has earned.');
  tp_check('#training-rookie-tp','#training-rookie-assigned', '[rank=rookie]', '#training-rookie-warning', 'You\'ve assigned more training points to your rookies than your stable has earned.');
}

function tp_check(id_points, id_assigned, attr_select, id_warning, message) {

  if (parseInt($(id_points).text()) < parseInt($(id_assigned).text())) {
    $(id_points).addClass('wrong');
    $(id_assigned).addClass('wrong');
    $('#stable-pilot-table .pilot-row' + attr_select + ' .assigned-tp').addClass('wrong');

    $(id_warning).html('&#x26A0; ' + message);
  } else {
    $(id_points).removeClass('wrong');
    $(id_assigned).removeClass('wrong');
    $('#stable-pilot-table .pilot-row' + attr_select + ' .assigned-tp').removeClass('wrong');
    $(id_warning).text('');
  }
}

function send_changed_pilot_attrib(field, oldvalue) {
  newvalue = field.find('input').val();
  callsign = field.parents('tr.pilot-row').attr('callsign');
  attribute = field.attr('field');

  $.ajax({
    type : 'post'
  , url  : window.location.href + '/set-attrib'
  , dataType : 'json'
  , data : { 
      'callsign'  : encodeURIComponent(callsign)
    , 'attribute' : attribute
    , 'value'     : newvalue
    }
  }).success(function(response) { 
    field.text(response['value']);

    field.siblings('.final-xp').text(response['total-cp']);
    if (response['is-dead']) {
        field.parents('tr.pilot-row').addClass('dead');
    } else {
        field.parents('tr.pilot-row').removeClass('dead');
    }

    $('#training-rookie-assigned').text(response['tp-table']['Rookie'])
    $('#training-contender-assigned').text(response['tp-table']['Contender'])
    $('#training-total-assigned').text(response['tp-table']['Total'])

    check_tp_assignment();
  }).fail(function(response) {
    field.text(oldvalue);
  }).always(function() {
    field.one('click', function() {
      to_number_input( $(this), send_changed_pilot_attrib );
    });
  });
}

function send_changed_tp(field, oldvalue) {
  new_tp = field.find('input').val();

  $.ajax({
    type : 'post'
  , url  : window.location.href + '/set-tp'
  , dataType : 'json'
  , data : { 'training-points' : new_tp }
  }).success(function(response) { 
    $('#training-rookie-tp').text(response['rookie-tp']);    
    $('#training-contender-tp').text(response['contender-tp']);

    total_html = response['total-tp'] + '<span class=\'icon-right\'>&#x270E;</span>';        
    $('#training-total').html(total_html);    

    check_tp_assignment();
  }).fail(function(response) {
    field.text(oldvalue);
  }).always(function() {
    field.one('click', function() {
      to_number_input( $(this), send_changed_tp );
    });
  });
}

function get_pilot_skills_list(callsign) {
  $.ajax({
    type : 'get'
  , url  : window.location.href + '/skill-list'
  , dataType : 'json'
  , data : { 'callsign' : encodeURIComponent(callsign) }
  }).success(function(response) {
    opthtml = '<option value=\'\'>-- Select Skill --</option>'

    $.each(response, function(group, list) {
      opthtml += '<optgroup label=\'' + group + '\'>'
      $.each(list, function(index, skill) {
        opthtml += '<option value=\'' + skill['id'] +'\'>' + skill['name'] + '</option>'
      });
      opthtml += '</optgroup>'
    });

    $('#pilot-training-skill').html(opthtml);
    $('#pilot-training-skill').removeAttr('disabled');
  });
}

function render_option(text, cost, key, available) {
   opthtml = '<option value=\'' + key + '\'';
   if (!available) {
      opthtml += ' disabled=\'yes\'';
   }
   opthtml += 'cost=\"' + cost + '\"> [' + cost + '] ' + text + '</option>';

   return opthtml;
}

function get_pilot_training_options(callsign, select_id) {
  field = $(select_id);

  $.ajax({
    type : 'get'
  , url  : window.location.href + '/training-opts'
  , dataType : 'json'
  , data : { 'callsign' : encodeURIComponent(callsign) }
  }).success(function(response) {
    opthtml = '<option value=\'\'>-- Select Training --</option>'
    opthtml += render_option( 'Piloting ' + response['piloting']['skill']
                            , response['piloting']['cost']
                            , 'P|' + response['piloting']['skill']
                            , response['piloting']['available']);
    opthtml += render_option( 'Gunnery ' + response['gunnery']['skill'] 
                            , response['gunnery']['cost']
                            , 'G|' + response['gunnery']['skill']
                            , response['gunnery']['available']);
    opthtml += render_option( to_ordinal(response['skills']['skill']) + ' Skill' 
                            , response['skills']['cost']
                            , 'S|' + response['skills']['skill']
                            , response['skills']['available']);

    field.html(opthtml);
    field.removeAttr('disabled');

  }).fail(function(response) {
    field.html('');
    field.attr('disabled','yes');
  });
}

function change_pilot_training() {
  train = $('#pilot-training-training');
  skills = $('#pilot-training-skill');
  notes = $('#pilot-training-notes');
  submit = $('#pilot-training-submit');

  if (train.val().charAt(0) == 'S') {
    notes.removeAttr('disabled');
    get_pilot_skills_list(callsign);
  } else {
    skills.html('');
    skills.attr('disabled','yes');
    notes.attr('disabled','yes');
  } 
}

function change_defer_pilot() {
  callsign = $('#pilot-defer-pilot option:selected').text()

  if (callsign == '-- Select Pilot --') { 
    $('#pilot-defer-deferred').html('');
    $('#pilot-defer-deferred').attr('disabled', 'yes');

    return; 
  }

  $.ajax({
    type : 'get'
  , url  : window.location.href + '/pilot-traits'
  , dataType : 'json'
  , data : { 'callsign' : callsign }
  }).success(function(response) { 
     opthtml = "<option value=\"\">-- Select Trait --</option>"
     $.each( response, function (i, trait) {
       opthtml += "<option value=\"" + trait['id'] + "\">" + trait['name'] + "</option>"
     });

     $('#pilot-defer-deferred').html(opthtml);
     $('#pilot-defer-deferred').removeAttr('disabled');
  }); 
}

function submit_pilot_training() {
  training = {
    'callsign' : $('#pilot-training-pilot option:selected').text()
  , 'training' : $('#pilot-training-training').val()
  };

  if (training['training'].charAt(0) == 'S') {
    training['skill'] = $('#pilot-training-skill').val();
    training['notes'] = $('#pilot-training-notes').val();
  };  

  $.ajax({
    type : 'post'
  , url  : window.location.href + '/add-training'
  , dataType : 'json'
  , data : training
  }).done(function(response) { 
     pilot_row_update(response['callsign'], response['spent-xp'], response['final-xp'])

     reset_training_form();
     reload_training_table();
  }); 
}

function submit_pilot_trait() {
  trait = {
    'callsign' : $('#pilot-trait-pilot option:selected').text()
  , 'trait' : $('#pilot-trait-trait').val()
  , 'notes'    : $('#pilot-trait-notes').val()
  };

  $.ajax({
    type : 'post'
  , url  : window.location.href + '/add-trait'
  , dataType : 'json'
  , data : trait
  }).done(function(response) { 
     pilot_row_update(response['callsign'], response['spent-xp'], response['final-xp'])

     reset_trait_form();
     reload_trait_table();
  });
}

function submit_pilot_deferred() {
  defer = {
    'callsign' : $('#pilot-defer-pilot option:selected').text()
  , 'trait'    : $('#pilot-defer-deferred').val()
  , 'notes'    : $('#pilot-defer-notes').val()
  , 'duration' : $('#pilot-defer-duration').val()
  };

  $.ajax({
    type : 'post'
  , url  : window.location.href + '/add-deferred'
  , dataType : 'json'
  , data : defer
  }).done(function(response) { 
     reset_defer_form();
     reload_defer_table();
  });
}

function pilot_row_update(callsign, spent_xp, final_xp) {
  pilot = $('#stable-pilot-table tr[callsign=\'' + callsign + '\']');

  pilot.children('.spent-xp').text(spent_xp);
  pilot.children('.final-xp').text(final_xp);

  $('#pilot-training-training option[cost]').each( function(idx, option) {
    opt = $(option);
    cost = parseInt(opt.attr('cost'));

    if (final_xp >= cost) {
      opt.removeAttr('disabled');
    } else {
      opt.attr('disabled','yes');
    }
  });
}

function event_table_setup(table_id, remove_suffix, id_attr) {
  table = $(table_id);

  if (table.find('tr:not(.header)').length > 0) {
    table.show();
  } else {
    table.hide();
  }

  table.find('input.icon-delete').click( function() {
    $.ajax({
      type : 'post'
    , url  : window.location.href + remove_suffix
    , dataType : 'json'
    , data : { 'train_id' : $(this).attr('train_id')
             , 'trait_id' : $(this).attr('trait_id')
             , 'defer_id' : $(this).attr('defer_id')
             , 'callsign' : $(this).attr('callsign') 
             }
    }).done(function(response) { 
      pilot_row_update(response['callsign'], response['spent-xp'], response['final-xp'])

      reload_training_table();
      reload_trait_table();
      reload_defer_table();
    });
  });
}

function training_table_setup() {
  event_table_setup('#pilot-training-list', '/remove-training', 'train_id');
}

function trait_table_setup() {
  event_table_setup('#pilot-trait-list', '/remove-trait', 'trait_id');
}

function defer_table_setup() {
  event_table_setup('#pilot-defer-list', '/end-deferred', 'defer_id');
}

function pilot_list_setup() {
  $('#stable-pilot-table .pilot-row .editable').one('click', function() {
    to_number_input( $(this), send_changed_pilot_attrib );
  });
  $('#stable-pilot-table .pilot-row .name').click( dialog_edit_pilot );
}

function reload_training_table() {
  $('#pilot-training-list').load(window.location.href + '/training #pilot-training-list', training_table_setup); 
}

function reload_trait_table() {
  $('#pilot-trait-list').load(window.location.href + '/trait #pilot-trait-list', trait_table_setup);
}

function reload_defer_table() {
  $('#pilot-defer-list').load(window.location.href + '/defer #pilot-defer-list', defer_table_setup);
}

function reload_pilots() {
  $('#stable-pilot-table').load(window.location.href + '/pilot-list #stable-pilot-table', pilot_list_setup);
}

function validate_training_form() {
  if (($('#pilot-training-pilot').val() == '')) {
    $('#pilot-training-submit').attr('disabled','yes');
    return false;
  }
  
  training = $('#pilot-training-training').val();
  if (training == null || training == '') {
    $('#pilot-training-submit').attr('disabled','yes');
    return false;
  } else if (training.charAt(0) != 'S') {
    $('#pilot-training-submit').removeAttr('disabled');
    return true;
  } else {
    skill = $('#pilot-training-skill').val();
    if (skill == null || skill == '') {
      $('#pilot-training-submit').attr('disabled','yes');
      return false;
    } else {
      $('#pilot-training-submit').removeAttr('disabled');
      return true;
    }
  }
  // Shouldn't be reachable, but if it does consider the form invalid
  $('#pilot-training-submit').attr('disabled','yes');
  return false;
}

function reset_training_form() {
  $('#pilot-training-pilot').val('');

  $('#pilot-training-training').html('');
  $('#pilot-training-training').attr('disabled','yes');

  $('#pilot-training-skill').html('');
  $('#pilot-training-skill').attr('disabled','yes');

  $('#pilot-training-notes').val('');
  $('#pilot-training-notes').attr('disabled','yes');

  $('#pilot-training-submit').attr('disabled','yes');
} 

function validate_trait_form() {
  pilot = $('#pilot-trait-pilot').val();
  trait = $('#pilot-trait-trait').val();

  if (pilot == null || pilot == '' || trait == null || trait == '') {
    $('#pilot-trait-submit').attr('disabled', 'yes');
    return false;
  } else {
    $('#pilot-trait-submit').removeAttr('disabled');
    return true;
  }
}

function reset_trait_form() {
  $('#pilot-trait-pilot').val('');
  $('#pilot-trait-trait').val('');

  $('#pilot-trait-submit').attr('disabled','yes');
}

function reset_defer_form() {
  $('#pilot-defer-pilot').val('');

  $('#pilot-defer-deferred').html('');
  $('#pilot-defer-deferred').attr('disabled','yes');

  $('#pilot-defer-notes').val('');
  $('#pilot-defer-duration').val('');

  $('#pilot-defer-submit').attr('disabled','yes');
}

function validate_deferred_form() {
  pilot    = $('#pilot-defer-pilot').val();
  deferred = $('#pilot-defer-deferred').val();
  duration = $('#pilot-defer-duration').val();

  if (pilot == null || pilot == "" || deferred == null || deferred == "" || duration == null || duration == "") {
    $('#pilot-defer-submit').attr('disabled', 'yes');
    return false;
  } else {
    $('#pilot-defer-submit').removeAttr('disabled');
    return true;
  }  
}

function dialog_add_pilot() {
  $('#dialog-add-pilot').attr('title', 'Add Pilot');

  $('#dialog-add-pilot').load( 
    window.location.href + '/add-pilot' 
  , function(response, state, jqxhr) {
    $('#dialog-add-pilot').dialog({
      modal: true
    , width: 550
    , height: (window.innerHeight * 0.75)
    , buttons: {
        Add: function() {
          submit_pilot(window.location.href + '/add-pilot');
        }
      , Close: function() { $( this ).dialog("close"); }
      }
    });
    
    $('#add-pilot-add-skill').click(dialog_add_pilot_skill_form);   
    attach_skill_delete_handler('#add-pilot-training-form');
    $('#add-pilot-add-problem').click(dialog_add_pilot_issue_form);   
    attach_issue_delete_handler('#add-pilot-training-form');
  });
}

function submit_pilot(submit_url) {
  formdata = form_to_dictionary('#add-pilot-form');

  $.ajax({
    type : 'post'
  , url  : submit_url 
  , dataType : 'html'
  , data : formdata
  , statusCode : {
      201 : function() { 
        reload_pilots();
        $('#dialog-add-pilot').dialog('close');
      }
    , 200 : function(response, statusText, jqXHR) {
        $('#add-pilot-form').replaceWith(response);
      }
    }
  });
}

function dialog_edit_pilot() {
  $('#dialog-add-pilot').attr('title', 'Edit Pilot');

  edit_url = $(this).attr('edit_url');

  $('#dialog-add-pilot').load( 
    edit_url
  , function(response, state, jqxhr) {
    $('#dialog-add-pilot').dialog({
      modal: true
    , width: 550
    , height: (window.innerHeight * 0.75)
    , buttons: {
       Update: function() {
          submit_pilot(edit_url);
        }
      , Close: function() { $( this ).dialog("close"); }
      }
    });
    
    $('#add-pilot-add-skill').click(dialog_add_pilot_skill_form);   
    attach_skill_delete_handler('#add-pilot-training-form');
    $('#add-pilot-add-problem').click(dialog_add_pilot_issue_form);   
    attach_issue_delete_handler('#add-pilot-training-form');
  });
}

function attach_skill_delete_handler(form_group_id) {
  $(form_group_id + ' .icon-delete').click( dialog_remove_pilot_skill_form )
}

function dialog_add_pilot_skill_form() {
  add_inline_form(
    '#add-pilot-training-form'
  , '#add-pilot-skill-template'
  , '#add-pilot-add-skill'
  , 'div.form-row:not(.template-form)'
  , '#id_train-TOTAL_FORMS'
  , attach_skill_delete_handler
  );
}

function dialog_remove_pilot_skill_form() {
  $(this).parents('.skill-row').remove();

  update_form_count(
    '#id_train-TOTAL_FORMS'
  , '#add-pilot-training-form'
  , 'div.form-row:not(.template-form)'
  );
}

function dialog_add_pilot_issue_form() {
  add_inline_form(
    '#add-pilot-problem-form'
  , '#add-pilot-issue-template'
  , '#add-pilot-add-problem'
  , 'div.form-row:not(.template-form)'
  , '#id_issue-TOTAL_FORMS'
  , attach_issue_delete_handler
  );
}

function attach_issue_delete_handler(form_group_id) {
  $(form_group_id + ' .icon-delete').click( dialog_remove_pilot_issue_form )
}

function dialog_remove_pilot_issue_form() {
  $(this).parents('.skill-row').remove();

  update_form_count(
    '#id_issue-TOTAL_FORMS'
  , '#add-pilot-problem-form'
  , 'div.form-row:not(.template-form)'
  );
}

$( document ).ready(function() {
  $('#training-total.editable').one('click', function() {
    to_number_input( $(this), send_changed_tp );
  });
  pilot_list_setup();

  reset_training_form();
  $('#pilot-training-pilot').change( function() { 
    callsign = $(this).children(':selected').text();
    get_pilot_training_options(callsign, '#pilot-training-training'); 
  });
  $('#pilot-training-training').change( change_pilot_training );
  $('#pilot-training-form select, #pilot-training-form input').change( validate_training_form);

  reset_trait_form();
  reset_defer_form();
  $('#pilot-trait-form select, #pilot-trait-form input').change( validate_trait_form );
  $('#pilot-defer-form select, #pilot-defer-form input').change( validate_deferred_form );

  $('#pilot-defer-pilot').change( change_defer_pilot );

  $('#pilot-training-submit').click( submit_pilot_training );
  $('#pilot-trait-submit').click( submit_pilot_trait );
  $('#pilot-defer-submit').click( submit_pilot_deferred );
  training_table_setup(); 
  trait_table_setup(); 
  defer_table_setup();

  $('#button-add-pilot').click( dialog_add_pilot );
  check_tp_assignment();
});
