
$( document ).ready(function() {
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
        tech : $("#add-tech-input").val()
      },
    }).done(function(newState) {
      $("#stable-tech-list").load(window.location.href + '/tech-list')    
    });
  });
})
