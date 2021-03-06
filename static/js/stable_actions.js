function update_action_info() {
  id = $('#id_action option:selected').val();

  if (id == "") {
    $('#preview-action-name').text('Action Effects')
    $('#preview-action').html('')
    $('#id_cost').val(0)
    
    $('#stable-action-submit').attr('disabled','yes');

    return;
  }

  $.ajax({
    type : 'get'
  , url  : '/reference/actions/' + id + '/json'
  , dataType: 'json'
  }).done(function(response) {
    $('#preview-action-name').text(response['action'])
    $('#preview-action').html(response['description'])
    $('#id_cost').val(response['base_cost'])

    $('#stable-action-submit').removeAttr('disabled');
  });
}

function send_updated_cost(field, oldvalue) {
  newvalue = field.find('input').val();

  $.ajax({
    type: 'post'
  , url : field.attr('set_url')
  , dataType : 'json'
  , data : { 'cost' : newvalue }
  }).success(function() {
    refresh_section('#stable-actions-list', setup_actions_list);
  }).fail(function(response) {
    field.text(oldvalue);
  }).always(function() {
    to_number_input(field, send_updated_cost);
  });
}

function send_updated_notes(field, oldvalue) {
  newvalue = field.find('input').val();

  $.ajax({
    type: 'post'
  , url : field.attr('set_url')
  , dataType : 'json'
  , data : { 'notes' : newvalue }
  }).success(function() {
    refresh_section('#stable-actions-list', setup_actions_list);
  }).fail(function(response) {
    field.text(oldvalue);
  }).always(function() {
    to_text_input(field, send_updated_notes);
  });
}

function setup_actions_form() {
  $('#id_action').change(update_action_info);
  $('#stable-action-submit').click(submit_action_form);
}

function setup_actions_list() {
  $('#stable-actions-list .action-notes.editable').one('click', function() {
    to_text_input($(this), send_updated_notes);
  });

  $('#stable-actions-list .action-cost.editable').one('click', function() {
    to_number_input($(this), send_updated_cost);
  });

  $('#stable-actions-list .icon-delete').click( function() {
    row = $(this).parents('.action-chit');

    $.ajax({
      type : 'post'
    , url  : $(this).attr('delete_url')
    , dataType : 'json'
    }).success( function(response) {
      row.slideUp(function() {
        refresh_section('#stable-actions-list', setup_actions_list);
      });

      refresh_section('#stable-action-form', setup_actions_form);
      refresh_section('#stable-action-management', setup_management_pane);
    })

  });
}

function setup_management_pane() {
  $('#stable-action-start').click( function() {
    $.ajax({
      type : 'post'
    , url  : $(this).attr('action_url')
    , dataType : 'json'
    , data : { 'start_week' : $(this).attr('start_week') }
    }).done( function(response) {
      refresh_section('#stable-actions-list', setup_actions_list);
      refresh_section('#stable-action-form', setup_actions_form);
      refresh_section('#stable-action-management', setup_management_pane);
    });
  }) 
}

function submit_action_form() {
  formData = form_to_dictionary('#stable-action-form');

  formUrl = $('#stable-action-form').attr('action');

  $.ajax({
    type : 'post'
  , url  : $('#stable-action-form').attr('action')
  , dataType : 'json'
  , data : formData
  }).done(function(response) {
    refresh_section('#stable-actions-list', setup_actions_list);
    refresh_section('#stable-action-form', setup_actions_form);
    refresh_section('#stable-action-management', setup_management_pane);
  });
}

$( document ).ready(function() {
  setup_actions_list();
  setup_actions_form();
  setup_management_pane();
});
