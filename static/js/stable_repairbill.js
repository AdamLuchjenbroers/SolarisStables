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
	  if (newState == 'true') {
		  item.addClass('item-critted');
	  } else {
		  item.removeClass('item-critted');
	  }
  });
}

$( document ).ready(function() {
	$('.item-crittable').click(crit_item);
});