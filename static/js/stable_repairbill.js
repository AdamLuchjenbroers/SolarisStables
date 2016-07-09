
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

function toggle_cored() {
  button = $(this);

  $.ajax({
    type : 'post',
    url  : window.location.href + '/setcored',
    dataType : 'json',
    data : {
      cored : ($(this).attr('undo') == 'no')
    },
  }).done(function(nowCored) {
    if (nowCored) {
      button.attr('undo','yes');
      button.text('Restore Mech');
    } else {
      button.attr('undo','no');
      button.text('Core Mech');
    }
  });
}

function finish_bill() {
  finish = !($(this).attr('id') == 'button-reopen');

  $.ajax({
    type : 'post',
    url  : window.location.href + '/setfinal',
    dataType : 'json',
    data : {
      final : finish
    },
  }).done(function(newState) {
    window.location.reload(true);
  });
}

function do_crit_item(item, setCrit) {
  $.ajax({
    type : 'post',
    url  : window.location.href + '/setcrit',
    dataType : 'json',
    data : {
      location : item.attr('location')
    , slot     : item.attr('slot')
    , critted  : setCrit
    },
  }).done(function(newState) {
    item.setCritted(newState);
  });
}

function crit_item() {
  var setCrit = !$(this).isCritted()
  item = $(this);
 
  if ( item.isAmmo() && !item.isCritted() ) {
    loc = item.attr('location');
    $('#dialog-ammocrit').dialog({
      title   : 'Ammunition Explosion'
    , minWidth : 500
    , buttons : {
        'Leave Intact' : function() { $(this).dialog('close'); }
      , 'Just the bin' : function() { 
           do_crit_item(item, setCrit); 
           $(this).dialog('close');
         }
      , 'Destroy' : function() { 
           do_destroy_location(loc);
           $(this).dialog('close');
         }
      }
    });
  } else {
    do_crit_item(item, setCrit); 
  }
}

function set_ammo_amount() {
  ammo = $(this);
  $.ajax({
    type : 'post',
    url  : window.location.href + '/setammocount',
    dataType : 'json',
    data : {
      lineid  : ammo.parents('.ammo-row').attr('lineid')
    , count   : ammo.val()
    },
  }).done(function(result) {
    ammo.val(result);
  });
}

function delete_bill() {
  $('#dialog-destroy').text('Are you sure you want to delete this bill and all related records?');
  $('#dialog-destroy').dialog({
    title   : 'Delete Repair Bill'
  , buttons : {
      'Keep' : function() { $(this).dialog('close'); }
    , 'Delete' : function() { 
        $.ajax({
          type : 'post',
          url  : window.location.href + '/delete',
          dataType : 'json',
        }).done(function(result) {
          window.location.href = result;
        });
      }
    }
  });
}

function set_omni_config() {
  $.ajax({
    type : 'post',
    url  : window.location.href + '/set-config',
    dataType : 'json',
    data : {
      config : $('#repair-omni-loadout').val()
    },
  }).done(function(result) {
      window.location.reload();
  });
}

function set_ammo_type() {
  ammo = $(this);

  $.ajax({
    type : 'post',
    url  : window.location.href + '/setammotype',
    dataType : 'json',
    data : {
      lineid  : ammo.attr('lineid')
    , ammoid  : ammo.val()
    },
  }).done(function(result) {
    count = ammo.parents('ammo-row').children('.ammo-amount input')
    if (result['critted']) {
      count.attr('disabled','yes');
    }
  
    count.val(result['count']);
  });
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

function page_ready() {
  $('.item-crittable').click(crit_item);
  $('.mech-armour-location input').change(damage_location);
  $('.mech-armour-location input').keypress( function(ev) {
    if (ev.keyCode == 13) {
      damage_location()
      return false;
    }
  });
  $('.mech-armour-front .mech-section-header').click(destroy_location);
  $('.ammo-type select').change(set_ammo_type);
  $('.ammo-amount input').change(set_ammo_amount);
  $('#button-core-mech').click(toggle_cored);
  $('#button-finalize').click(finish_bill);
  $('#button-reopen').click(finish_bill);
  $('#button-delete-bill').click(delete_bill);  
  $('#repair-omni-loadout').change(set_omni_config);
}

$( document ).ready( page_ready );

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


