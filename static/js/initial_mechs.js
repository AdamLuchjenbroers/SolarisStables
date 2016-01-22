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

$( document ).ready(function() {

    attach_mechlist_autocomplete( $('input#id_form-0-mech_name'), '.mech-purchase', '.mech-code select' );

    $('.mech-purchase span.mech-code select').change(
      select_chassis_handler('.mech-purchase', 'span.mech-name input', '.mech-cost', '.mech-preview input')
    );

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
        attach_mechlist_autocomplete( $('input#id_form-' + form_id + '-mech_name'), '.mech-purchase' );
        $(this).hide();
    });
});

$( document ).ajaxStop( recalc_total );
