
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
    $.each(newState['locations'], function(loc, state) {
      $('#input_armour_' + loc.toLowerCase()).val(state['armour']);
      $('#input_structure_' + loc.toLowerCase()).val(state['structure']);
    });

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
 
  if ( item.isAmmo() && !item.isCritted() ) {
    loc = item.attr('location');
    $('#dialog-ammocrit').dialog({
      title   : 'Ammunition Explosion'
    , buttons : {
        'Leave Intact' : function() { $(this).dialog('close'); }
      , 'Destroy' : function() { 
           do_destroy_location(loc);
           $(this).dialog('close');
         }
      }
    });
  } else { 
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
}

function ammoform_for_item(item) {
  loc  = item.attr('location');
  slot = item.attr('slot');
  $('.ammo-row[location=' + loc + ' ][slot=' + slot + '] .ammo-amount input').attr('disabled','yes');
}

$.fn.extend({
  isCritted      : function () { return this.hasClass('item-critted') }
, isAmmo         : function () { return this.hasClass('item-ammo') }
, setAmmoCritted : function(item, critted) {
    loc  = this.attr('location');
    slot = this.attr('slot');
    inCount = $('.ammo-row[location=' + loc + ' ][slot=' + slot + '] .ammo-amount input');

    if (critted) {
       inCount.attr('disabled','yes');
       inCount.val( inCount.attr('max') );
    } else {
       inCount.removeAttr('disabled');
       inCount.val( '0' );
    }
}
, setCritted     : function(critted) {
    if (critted) {
      this.addClass('item-critted');
    } else {
      this.removeClass('item-critted');
    }

    if (this.isAmmo()) {
      loc  = this.attr('location');
      slot = this.attr('slot');
      inCount = $('.ammo-row[location=' + loc + ' ][slot=' + slot + '] .ammo-amount input');
  
      if (critted) {
         inCount.attr('disabled','yes');
         inCount.val( inCount.attr('max') );
      } else {
         inCount.removeAttr('disabled');
         inCount.val( '0' );
      }
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


