function show_fight_form() {
  $('#dialog-add-fight').load( $('#button-add-fight').attr('form_url'), function() {
    $(this).dialog({
      modal : true
    , width : '80%'
    , buttons : {
      Submit : function() {}
    , Cancel : function() { $(this).dialog("close"); }
    }
    });
  });
}

$( document ).ready(function() {
  $('#button-add-fight').click(show_fight_form);
});
