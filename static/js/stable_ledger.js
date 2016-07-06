ledger_edit_button = '<input class=\"icon-button ledger-edit\" value=\"✎\" tabindex=\"\" type=\"submit\">'

function send_changed_ledger_cost(field, oldvalue) {
  newvalue = field.find('input').val();
  entry = field.parents('tr.ledger-iten').attr('entry');	
  url = field.attr('edit_url');

  $.ajax({
    type : 'post'
  , url  : field.attr('edit_url')
  , dataType : 'json'
  , data : { 
      'cost'      : newvalue
    , 'entry_id'  : entry
    }
  }).success(function(response) { 
    field.text(response['cost']);
    recalc_all();
  }).fail(function(response) {
    field.text(oldvalue);
  }).always(function() {
    field.one('click', function() {
      to_number_input( $(this), send_changed_ledger_cost );
    });
  });
}

function send_changed_ledger_description(field, oldvalue) {
  newvalue = field.find('input').val();
  entry = field.parents('tr.ledger-iten').attr('entry');	
  url = field.attr('edit_url');

  $.ajax({
    type : 'post'
  , url  : field.attr('edit_url')
  , dataType : 'json'
  , data : { 
      'description' : newvalue
    , 'entry_id'    : entry
    }
  }).success(function(response) {
    field.html(ledger_edit_button + response['description']);
  }).fail(function(response) {
    field.text(oldvalue);
  }).always(function() {
    field.one('click', function() {
      to_text_input( $(this), send_changed_ledger_description );
    });
  });
}

function recalc_group(group) {
   var grouptotal = 0;
   
  $('.ledger-item[group=' + group + '] .ledger-value').each( function() {
    cost = parseInt( $(this).text());

    if (!isNaN(cost)) {
      grouptotal += cost;
    }
  });

  if (grouptotal >= 0) {
    $('#ledger-sumvalue-' + group).text(grouptotal).removeClass('ledger-negative');
  } else if (grouptotal < 0) {
    $('#ledger-sumvalue-' + group).text(grouptotal).addClass('ledger-negative');
  }

  return grouptotal;
}

function recalc_all() {
  var total = parseInt( $('#ledger-opening-balance').text());

  $.each(['r', 'p', 'e', 'w', 'i'], function(i, group) {
      total += recalc_group(group);
  });

  $('#ledger-closing-balance').text(total); 
}

function setup_row_edit_handlers() {
  $('.ledger-item[entry] td.ledger-value').one('click', function() {
    to_number_input( $(this), send_changed_ledger_cost );
  }); 

  $('.ledger-item[entry] td.ledger-desc').one('click', function() {
    to_text_input( $(this), send_changed_ledger_description );
  }); 

  $('.ledger-item[entry] input.ledger-delete').click( function() {
    row = $(this).parents('tr.ledger-item');

    $.ajax({
      type : 'post'
    , url  : $(this).attr('delete_url')
    , dataType : 'json'
    , data : {'entry_id' : row.attr('entry')}
    }).success( function(response) {
      row.fadeOut(function() { 
        row.remove();
        recalc_all();
      });
    });
  });
}

function submit_new_entry() {
  row = $(this).parents('tr.ledger-add-form');
  data = {
    'group'       : row.find('input[name=type]').val()
  , 'cost'        : row.find('input[name=cost]').val()
  , 'description' : row.find('input[name=description]').val()
  }; 

  $.ajax({
    type : 'post'
  , url  : row.attr('add_url')
  , dataType : 'json'
  , data : data
  }).success(function(response) {
    last_row = $('.ledger-item[group=' + response['group'].toLowerCase() + ']:last');
    if (last_row.length < 1) {
      /* No last row, so add the new item after the header */
      last_row = $('#ledger-subheader-' + response['group'].toLowerCase());
    }

    last_row.after(response['entry_html']);      
    $('.ledger-item[group=' + response['group'].toLowerCase() + '].hidden').fadeIn();

    setup_row_edit_handlers()
    recalc_all();
  });
}

$( document ).ready(function() {
  setup_row_edit_handlers()

  $('.ledger-add').on('click', submit_new_entry);

  recalc_all();
});
