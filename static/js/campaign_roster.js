function load_fight_form() {
  $('#dialog-add-fight').load( $('#button-add-fight').attr('form_url'), display_fight_form);
}

function display_fight_form() {
  $(this).dialog({
    modal : true
  , width : '36em'
  , buttons : {
    Submit : function() { submit_fight_form('#add-fight-form'); }
  , Cancel : function() { $(this).dialog("close"); }
    }
  });
}

function setup_fight_list() {
  //Stub
}

function reload_part(list_id, setup_func) {
  url = $(list_id).attr('source_url');

  $(list_id).load(url + ' ' + list_id, setup_func);
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
        reload_part('#fight-roster-list', setup_fight_list);
      }
    , 200 : function(response, statusText, jqXHR) {
        $('#dialog-add-fight').html(response);

        //Because it hides itself all over again...
        display_fight_form()
      }
    } 
  });

  return submit_url;
}

$( document ).ready(function() {
  $('#button-add-fight').click(load_fight_form);
});
