
function damage_location() {
  item = $(this);

  $.ajax({
    type : 'post',
    url  : window.location.href + '/setdamage',
    dataType : 'json',
    data : {
      location : $(this).attr('location')
    , type     : $(this).attr('damage')
    , damage   : $(this).val()
    },
  }).done(function(newState) {
    item.val(newState);
  });
}

function do_destroy_location(loc) {
  $.ajax({
    type : 'post',
    url  : window.location.href + '/destroy',
    dataType : 'json',
    data : {
      location : loc
    },
  }).done(function(newState) {
    $('#input_armour_' + loc.toLowerCase()).val(newState['armour']);
    $('#input_structure_' + loc.toLowerCase()).val(newState['structure']);
    $.each(newState['criticals'], function(slot, critted) {
      $('.item-crittable[location=\"' + loc + '\"][slot=\"' + slot + '\"]').setCritted(critted);
    });
  });
}

function destroy_location() {
  loc = $(this).text();

  $('#dialog-destroy').text('Are you sure you want to mark the ' + loc + ' as destroyed?');
  $('#dialog-destroy').dialog({
    title   : 'Destroy Location'
  , buttons : {
      'Leave Intact' : function() { $(this).dialog('close'); }
    , 'Destroy' : function() { 
         do_destroy_location(loc);
         $(this).dialog('close');
       }
    }
  });
}

function crit_item() {
  var setCrit = !$(this).isCritted()
  item = $(this);
  
  $.ajax({
    type : 'post',
    url  : window.location.href + '/setcrit',
    dataType : 'json',
    data : {
      location : $(this).attr('location')
    , slot     : $(this).attr('slot')
    , critted  : setCrit
    },
  }).done(function(newState) {
    item.setCritted(newState);
  });
}

$.fn.extend({
  isCritted : function () { return this.hasClass('item-critted') }
, setCritted : function(critted) {
    if (critted) {
      this.addClass('item-critted');
    } else {
      this.removeClass('item-critted');
    }
  },
});

$( document ).ready(function() {
  $('.item-crittable').click(crit_item);
  $('.mech-armour-location input').change(damage_location);
  $('.mech-armour-front .mech-section-header').click(destroy_location);
});

$( document ).ajaxStop( function() {
  $.ajax({
    type : 'get',
    url  : window.location.href + '/itemised',
    dataType : 'html',
    global : false
  }).done(function(itemised) {
    $('#repair-cost-itemised').html(itemised);
  });
});


