$( document ).ready(function() {
  
  $('#id_house').on('change', function() {
     ajaxurl='/reference/ajax/house_disciplines/' + $('#id_house option:selected').text()
     
     $.ajax( {
       type : 'get',
       url  : '/reference/ajax/house_disciplines/' + $('#id_house option:selected').text(),
       dataType : 'json'
     }).done(function(json) {
       $('#House').attr('class', 'field_info')
       
       infostr = 'House Disciplines<ul>';
       
       $.each( json, function(i, item) {
         infostr += '<li>' + item['name'] + '</li>'
       });
       
       infostr += '</ul>';
       $('#House_message').html(infostr);
     });
     
  });
});