function to_number_input(field, sender) {
  oldvalue = field.html();
  value = parseInt(field.text());

  input = "<input type=\"number\" value=\"" + value +"\"></input>";
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

    total_html = response['total-tp'] + "<span class=\"icon-right\">&#x270E;</span>";        
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
    opthtml = '<option>-- Select Skill --</option>'

    $.each(response, function(group, list) {
      opthtml += "<optgroup label=\"" + group + "\">"
      $.each(list, function(index, skill) {
        opthtml += "<option value=\"" + skill['id'] +"\">" + skill['name'] + "</option>"
      });
      opthtml += "</optgroup>"
    });

    $('#pilot-training-form span.skill select').html(opthtml);
    $('#pilot-training-form span.skill select').removeAttr('disabled');
  });
}

function render_option(text, cost, key, available) {
   opthtml = '<option value=\"' + key + '\"';
   if (!available) {
      opthtml += ' disabled=\"yes\"';
   }
   opthtml += '> [' + cost + '] ' + text + '</option>';

   return opthtml;
}

function get_pilot_training_options(field) {
  callsign = $(field).children(':selected').text();

  $.ajax({
    type : 'get'
  , url  : window.location.href + '/training-opts'
  , dataType : 'json'
  , data : { 'callsign' : encodeURIComponent(callsign) }
  }).success(function(response) {
    opthtml = ''
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

    field = $('#pilot-training-form span.training select');
    field.html(opthtml);
    field.removeAttr('disabled');

    field.change( function() {
      skills = $('#pilot-training-form span.skill select');
      notes = $('#pilot-training-form span.notes input');

      if (field.val().charAt(0) == 'S') {
        notes.removeAttr('disabled');

        get_pilot_skills_list(callsign);
      } else {
        skills.html('');
        skills.attr('disabled','yes');
        notes.attr('disabled','yes');
      } 
    });

  }).fail(function(response) {
    $('#pilot-training-form span.training select').html = '';
    $('#pilot-training-form span.training select').attr('disabled','yes');
  });
}

$( document ).ready(function() {
  $('#training-total.editable').one('click', function() {
    to_number_input( $(this), send_changed_tp );
  });
  $('#stable-pilot-table .pilot-row .editable').one('click', function() {
    to_number_input( $(this), send_changed_pilot_attrib );
  });

  $('#pilot-training-form span.pilot select').change( function() { get_pilot_training_options(this); } )

  check_tp_assignment();
});
