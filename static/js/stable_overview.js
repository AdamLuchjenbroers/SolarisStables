function attach_tech_input(form, button, input) {
  $('#add-tech-input').autocomplete({
    source: window.location.href + '/list-techs'
  , minLength: 3
  });

  $('#add-tech-submit').click( function() {
    $.ajax({
      type : 'post',
      url  : $('#add-tech-form').attr('action'),
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
      $('#stable-tech-section').load(window.location.href + '/tech-list', function() {    
        attach_tech_input('#add-tech-input');
      });
    });
  });

  $('#stable-tech-list .tech-delete').click(function() {
    $.ajax({
      type : 'post',
      url  : $('#stable-tech-section').attr('remove_url'),
      dataType : 'json',
      data : {
        tech : $(this).attr('tech')
      }
    }).done(function(newState) {
      $('#stable-tech-section').load(window.location.href + '/tech-list', function() {    
        attach_tech_input('#add-tech-input');
      });
    });
    
  });
}

function modify_reputation(action) {
  $.ajax({
    type : 'post'
  , url  : window.location.href + '/alter-rep'
  , dataType : 'json'
  , data : { change : action }
  }).success(function(response) {
    new_rep  = '<span id=\"stable-reputation\" class=\"';
    new_rep += response['class'] + '\">';
    new_rep += response['text'] + '</span>';

    $('#stable-reputation').replaceWith(new_rep);
  });
}

$( document ).ready(function() {
  attach_tech_input('#add-tech-input');

  $('#stable-reputation-minus').click( function() { modify_reputation('minus'); } );
  $('#stable-reputation-plus').click( function() { modify_reputation('plus'); } );
});
