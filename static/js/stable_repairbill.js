
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

function crit_item() {
  var setCrit = !$(this).hasClass('item-critted')
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
    if (newState) {
      item.addClass('item-critted');
    } else {
      item.removeClass('item-critted');
    }
  });
}

$( document ).ready(function() {
  $('.item-crittable').click(crit_item);
  $('.mech-armour-location input').change(damage_location);
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