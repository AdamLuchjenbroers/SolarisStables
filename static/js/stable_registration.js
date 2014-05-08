function SelectList(selector) {
  this.src_html = $(selector).clone();
  
  options = [];
  
  src_html.each( function(i, item) {	  
	  options.push( {
		  element : item,
		  id : item.value,
		  text : item.text,
		  visible : true,
	  });
  });
  
  this.hide = function( entry ) {
     $.each(this.options, function(i, option) {
    	 if ((entry == option['id']) || (entry == option['text'])) {
    		 option['visible'] = false;
    	 };
     });
  };
  
  this.reset = function() {
	  $.each(this.options, function(i, option) {
		option['visible'] = true;
	  }); 
  }
  
  this.render = function(selected) {
	  var output = '';
	  console.log('render(' + selected + ')');
	  
	  $.each(this.options, function(i, option) {
		  option['element'].selected = (
		    (selected == option['id']) || (selected == option['text'])
		  );
		  
		  if(option['visible'] || option['element'].selected) {
			  output += '<option value=\"' + option['id'] + '\"';
			  if (option['element'].selected) {
				  output += ' selected=\"selected\"';
			  }
			  output += '>' + option['text'] + '</option>\n';
		  }
	  });
	  
	  return output;
  };
  
  return this;
};

$( document ).ready(function() {
  var select_list = SelectList('#id_discipline_1 option');  
  var house_disciplines = [];
  
  console.log(select_list);
  
  function get_selected_disciplines() {
    selected = [];
  
    $.each( ['#id_discipline_1', '#id_discipline_2'], function(i, id) {
       val = $(id + ' option:selected');
         
       if (val.attr('value') != '') {
         selected[id] = {
           field : id,
           id : val.attr('value'),
           title : val.text()
         };
       };                 
     });
     
     return selected;
  }
  
  /*
   If Discipline 2 has a value and Discipline 1
   is blank, move the selection from Discipline 2
   up to Discipline 1
  */
  function rotate_selected_disciplines() {
    if ($('#id_discipline_1 option:selected').attr('value') != '') {
      console.log('V:[' + $('#id_discipline_1 option:selected').attr('value') + ']')
      return;
    }
    
    disc_id = $('#id_discipline_2 option:selected').attr('value');
    
    if ( disc_id != '') {
      $('#id_discipline_1').val(disc_id);
      $('#id_discipline_2').val('');
    };    
  }
  
  function update_disciplines() {
    console.log('update_disciplines()');
    
    selected = get_selected_disciplines();
    
    select_list.reset();
     
    $.each( house_disciplines, function(i, item) {
      select_list.hide(item['id']);
      
      $.each( ['#id_discipline_1', '#id_discipline_2'], function(j,id) {
    	  val = $(id + ' option:selected');
    	  
    	  if (val.attr('value') == item['id']) {
    		  $(id).prop('selectedIndex', 0);
    	  };
      });       
    });  
    
    // Move up the disciplines so empty entries are at the bottom of the list;
    rotate_selected_disciplines();
    
    $.each( ['#id_discipline_1', '#id_discipline_2'], function(i, id) {
        val = $(id + ' option:selected');
         
        console.log(id + ' Selected:' + val.attr('value'));
        console.log(val);
        
        if (val.attr('value') != '') {
          select_list.hide(val.attr('value'));
        };
        
        $(id).html(
        	select_list.render(val.attr('value'))
        )
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
  
$('#id_discipline_1').on('change', update_disciplines);
$('#id_discipline_2').on('change', update_disciplines);
});