function to_number_input(field, sender) {
  oldvalue = field.html();
  value = parseInt(field.text());

  input = "<input type=\"number\" value=\"" + value +"\"></input>";
  field.html(input);
  input = field.find('input');
  input.focusout(function() {
    sender(field, value);
  });
}

function send_changed_tp(field, oldvalue) {
  new_tp = field.find('input').val();

  $.ajax({
    type : 'post'
  , url  : window.location.href + '/set-tp'
  , dataType : 'json'
  , data : { 'training-points' : new_tp }
  }).success(function(response) { 
    $('#training-rookie-tp').text(response['rookie-tp']);    
    $('#training-contender-tp').text(response['contender-tp']);

    total_html = response['total-tp'] + "<span class=\"icon-right\">&#x270E;</span>";        
    $('#training-total').html(total_html);    
  }).fail(function(response) {
    field.text(oldvalue);
  }).always(function() {
    field.one('click', function() {
      to_number_input( $(this), send_changed_tp );
    });
  });
}

$( document ).ready(function() {
  $('#training-total.editable').one('click', function() {
    to_number_input( $(this), send_changed_tp );
  });
});
