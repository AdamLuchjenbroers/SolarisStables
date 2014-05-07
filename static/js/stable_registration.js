$( document ).ready(function() {
  select_list = $('#id_discipline_1 option');
  
  house_disciplines = [];
  
  select_list.each( function(i, item) {
     console.log( $( this ).attr('value') + ": " + $( this ).text() );
  });
  
  function update_disciplines() {
    console.log('update_disciplines()');
    selected = [];
    
    $.each( ['#id_discipline_1', '#id_discipline_2'], function(i, id) {
       val = $(id + ' option:selected');
         
       if (val.attr('value') != '') {
         selected.push( {
           field : id,
           id : val.attr('value'),
           title : val.text()
         });
       };                 
     });
    
    console.log('  selected list built');
     
    $.each( house_disciplines, function(i, item) {
      console.log('Update HD: ' + item['name']);
                   
      $.each(selected, function(j,option) {
        if(selected[j]['id'] == item['id']) {
           $(selected[j]['field']).val('');
           selected.splice(j);
        }
      });     
    });    
       
     $.each(selected, function(i, d) {
       console.log(d['title'] + '[' + d['id'] + '] in field ' + d['field']);
     });
  }
  
  $('#id_house').on('change', function() {         
     $.ajax( {
       type : 'get',
       url  : '/reference/ajax/house_disciplines/' + $('#id_house option:selected').text(),
       dataType : 'json'
     }).done(function(json) {
       $('#House').attr('class', 'field_info')
       
       infostr = 'House Disciplines<ul>';
       
       $.each( json, function(i, item) {
          infostr += '<li>' + item['name'] + '</li>';
       });
       
       infostr += '</ul>';
       $('#House_message').html(infostr);
       
       house_disciplines = json;
       update_disciplines();       
     
     });
     
  });
});