
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
});
