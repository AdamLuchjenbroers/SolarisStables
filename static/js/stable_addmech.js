function recalc_total() {
  var total = parseInt( $('#initial-mechs-balance').html() )

  $('div.mech-purchase span.mech-cost').each( function() {
    cost = parseInt( $(this).text())

    if (!isNaN(cost)) {
      total += cost;
    }
  });

  $('#initial-mechs-total').text(total);
}

$(window).unload(function() {
  //It's a hack - but since the formset gets reset on page reload
  //we should reset the form count too
  $('#id_form-TOTAL_FORMS').val(1);
});


function attach_autocomplete(jObject) {
  jObject.autocomplete({
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
}

$( document ).ready(function() {

    attach_autocomplete( $('input#id_form-0-mech_name') );

    $('.mech-purchase span.mech-code select').change(function() {
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

          preview = cost.parents('.mech-purchase').find('span.mech-preview input');
          preview.prop('disabled', false);

          preview.click(function() {
              $('#dialog-mechpreview').load('/reference/mechs/' + chassis + '/' + type + ' div.body');
              $('#dialog-mechpreview').dialog ({
                  modal: true,
                  width: (window.innerWidth * 0.75),
                  height: (window.innerHeight * 0.75),
                  buttons: {
                       Close: function() { $( this ).dialog("close"); }
                  }
              });
          });

          recalc_total();
       }); 
    });

    $('form#initial-mechs-form span.form-action input.add-item').click(function() {
        new_form=$('#initial-mechs-template').clone(true);
        form_id=parseInt($('#id_form-TOTAL_FORMS').val());

        new_form.removeClass('template-form');
        new_form.removeAttr('id');


        new_form.find(':input[name]').each(function() {
            var name = $(this).attr('name').replace('__prefix__',form_id);
            
            $(this).attr('name', name);
            $(this).attr('id', 'id_' + name);
        });

        $('#id_form-TOTAL_FORMS').val(form_id + 1);
 
        $('#initial-mechs-formbody').append(new_form);
        attach_autocomplete( $('input#id_form-' + form_id + '-mech_name') );
        $(this).hide();
    });
});
