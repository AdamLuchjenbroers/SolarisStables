$( document ).ready(function() {
  $('#browse-next-week.create-post').click( function() {
    $.ajax({
      type : 'post'
    , url  : '/stable/create'
    , dataType : 'json'
    , data : {
        view : $(this).attr('viewname')
      , week : $(this).attr('week')
      }
    }).done( function(newpage) {
      window.location.href = newpage;
    });
  });
});
