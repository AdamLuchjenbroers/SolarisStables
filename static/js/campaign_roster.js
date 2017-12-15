function show_fight_form() {
  $('#dialog-add-fight').load( $('#button-add-fight').attr('form_url'), function() {
    $(this).dialog({
      modal : true
    , width : '80%'
    , buttons : {
      Submit : function() { submit_fight_form('#add-fight-form'); }
    , Cancel : function() { $(this).dialog("close"); }
    }
    });
  });
}

function submit_fight_form(form_id) {
  submit_url = $(form_id).attr('submit_url');
  formdata = form_to_dictionary(form_id);

  $.ajax({
    type : 'post'
  , url  : submit_url
  , dataType : 'html'
  , data: formdata
  , statusCode : {
      201 : function() { 
        //reload_fights();
        $('#dialog-add-fight').dialog('close');
      }
    , 200 : function(response, statusText, jqXHR) {
        $('#dialog-add-fight').html(response);

        //Because it hides itself all over again...
        $(this).dialog({
          modal : true
        , width : '80%'
        , buttons : {
          Submit : function() { submit_fight_form('#add-fight-form'); }
        , Cancel : function() { $(this).dialog("close"); }
        }
        });
      }
    } 
  });

  return submit_url;
}

$( document ).ready(function() {
  $('#button-add-fight').click(show_fight_form);
});
