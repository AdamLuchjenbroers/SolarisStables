$( document ).ready(function() {
  var selected = [];
  var choose_limit = 2;

  // Reset this field on page reload.
  $('#id_house').val("");

  $('#id_house').on('change', function() {         
    $.ajax( {
        type : 'get',
        url  : '/stable/mechs/house_disciplines/' + $('#id_house option:selected').text(),
        dataType : 'json'
    }).done(function(json) {
        selected = $('#id_stable_disciplines').val();

        $('#id_stable_disciplines option.house').removeClass('house').removeAttr("disabled");
       
        $.each(json, function(i, item) {
            if (item['choose-limit'] !== undefined) {
                choose_limit = item['choose-limit'];
                $('#id_stable_disciplines').attr('size', choose_limit);
            } else {
                $('#id_stable_disciplines option[value=' + item.id + ']').addClass('house').attr("disabled", "yes");
            
                if ($.inArray(item.id, selected) != -1) {                
                  selected.splice( $.inArray(item.id, selected), 1 );
                }
            }
        });
                           
        $('#id_stable_disciplines').val(selected)
     });
  });
  
  $('#id_stable_disciplines').on('change', function() {
        if ($(this).val().length > choose_limit) {
            $('#id_stable_disciplines').val(selected) ; 
        } else {
            selected = $('#id_stable_disciplines').val();
        }
        
  });
});