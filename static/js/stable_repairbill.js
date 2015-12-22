function crit_item() {
  if ($(this).hasClass('item-critted')) {
	  $(this).removeClass('item-critted');
  } else {
	  $(this).addClass('item-critted');
  }
}

$( document ).ready(function() {
	$('.item-crittable').click(crit_item);
});