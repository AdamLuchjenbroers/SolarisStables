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
                var option_html="<option value=\"\">--</value>";
                
                $.each(json, function(index, val) {
                    option_html += "<option value=\"" + val + "\">" + val + "</value>";
                }); 
                                                                   
                inputbox.parents('.mech-purchase').find('span.mech-code select').html(option_html);               
            });
        }
    });

    $('span.mech-code select').change(function() {
       type = $(this).val();
       chassis = $(this).parents('.mech-purchase').find('span.mech-name input').val();
       cost = $(this).parents('.mech-purchase').find('span.mech-cost');

       $.ajax( {
           type : 'get',
           url  : '/reference/ajax/mech/price-of',
           dataType : 'json',
           data : {
               chassis : chassis,
               type    : type
           },
       }).done(function(json) {
          cost.html('-' + json);
       }); 
    });
});
