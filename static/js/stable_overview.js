function attach_tech_input(form, button, input) {
  $('#add-tech-input').autocomplete({
    source: window.location.href + '/list-techs'
  , minLength: 3
  });

  $('#add-tech-submit').click( function() {
    $.ajax({
      type : 'post',
      url  : window.location.href + '/add-tech',
      dataType : 'json',
      data : {
        tech : $('#add-tech-input').val()
      },
      beforeSend: function(jqXHR, plainObj) {
        $('#add-tech-form .spinner').show();
        $('#add-tech-form .action').hide();
      }, 
      complete: function(jqXJR, plainObj) {
        $('#add-tech-form .spinner').hide();
        $('#add-tech-form .action').show();
      }, 
    }).done(function(newState) {
      $("#stable-tech-list").load(window.location.href + '/tech-list')    
      attach_tech_input();
    });
  });
}

$( document ).ready(function() {
  attach_tech_input('#add-tech-input');
});
