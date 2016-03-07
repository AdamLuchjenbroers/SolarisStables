function to_number_input(field, sender) {
  oldvalue = field.html();
  value = parseInt(field.text());

  input = '<input type=\'number\' value=\'' + value +'\'></input>';
  field.html(input);
  input = field.find('input');
  input.on('focusout', function() {
    sender(field, value);
  });
}

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

function pilot_row_update(callsign, spent_xp, final_xp) {
  pilot = $('#stable-pilot-table tr[callsign=\'' + callsign + '\']');

  pilot.children('.spent-xp').text(spent_xp);
  pilot.children('.final-xp').text(final_xp);
}

function training_table_setup() {
  table = $('#pilot-training-list');

  if (table.find('tr:not(.header)').length > 0) {
    table.show();
  } else {
    table.hide();
  }

  table.find('input.icon-delete').click( function() {
    $.ajax({
      type : 'post'
    , url  : window.location.href + '/remove-training'
    , dataType : 'json'
    , data : { 'train_id' : $(this).attr('train_id'), 'callsign' : $(this).attr('callsign') }
    }).done(function(response) { 
      pilot_row_update(response['callsign'], response['spent-xp'], response['final-xp'])

      reload_training_table();
    });
  });
}

function reload_training_table() {
  $('#pilot-training-list').load(window.location.href + '/training #pilot-training-list', training_table_setup);
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
  $('#pilot-triat-pilot').val('');
  $('#pilot-triat-trait').val('');

  $('#pilot-triat-submit').attr('disabled','yes');
}

$( document ).ready(function() {
  $('#training-total.editable').one('click', function() {
    to_number_input( $(this), send_changed_tp );
  });
  $('#stable-pilot-table .pilot-row .editable').one('click', function() {
    to_number_input( $(this), send_changed_pilot_attrib );
  });

  reset_training_form();
  $('#pilot-training-pilot').change( function() { 
    callsign = $(this).children(':selected').text();
    get_pilot_training_options(callsign, '#pilot-training-training'); 
  });
  $('#pilot-training-training').change( function() { change_pilot_training(); });
  $('#pilot-training-form select, #pilot-training-form input').change( function() { validate_training_form(); });

  $('#pilot-trait-form select, #pilot-trait-form input').change( function() { validate_trait_form(); });

  $('#pilot-training-submit').click( function() { submit_pilot_training(); } );
  training_table_setup();

  check_tp_assignment();
});
