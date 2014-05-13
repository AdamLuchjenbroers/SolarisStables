
$.fn.extend ({
	showForm : function () {
		this.find('div.line_display').hide();
		this.find('div.line_update').show();	
		
		return this;
	},
	showItem : function () {
		this.find('div.line_update').hide();
		this.find('div.line_display').show();
		
		return this;
	},
});

$( document ).ready(function() {
	$('div.lineitem').on('click', function () {
		$('div.lineitem').showItem();		
		$(this).showForm();
	});
});