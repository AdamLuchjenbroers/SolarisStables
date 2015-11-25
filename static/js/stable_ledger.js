
function recalc_group(group) {
   var grouptotal = 0;
   
  $('div.item-group-' + group + ' div.ledger-view-display span.ledger-value p').each( function() {
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

$.fn.extend ({
	showForm : function () {
		this.find('div.ledger-view-display').hide();
		this.find('form.ledger-item-edit').show();	
		
		return this;
	},
	showItem : function () {
		this.find('form.ledger-item-edit').hide();
		this.find('div.ledger-view-display').show();
		
		return this;
	},
});

$( document ).ready(function() {
	$('div.ledger-item-edit').on('click', function () {
		$('div.ledger-item-edit').showItem();		
		$(this).showForm();
	});

        recalc_all();
});
