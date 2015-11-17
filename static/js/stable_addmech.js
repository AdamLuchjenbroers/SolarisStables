$( document ).ready(function() {

    $('span.mech-name input').autocomplete({
        source: "/stable/query/list-produced",
        minLength: 3,
        select: function (event, ui) {
            var inputbox = $(this);
                    
            $.ajax( {
                type : 'get',
                url  : '/stable/query/list-variants',
                dataType : 'json',
                data : {
                    mech : ui.item.value
                },
            }).done(function(json) {
                var option_html="";
                
                $.each(json, function(index, val) {
                    option_html += "<option value=\"" + val + "\">" + val + "</value>";
                }); 
                                                                   
                inputbox.parents('fieldset.mech_purchase').find('span.mech-code select').html(option_html);               
            });
        }
  });
});