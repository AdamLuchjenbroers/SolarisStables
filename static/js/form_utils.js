$.fn.hasAttr = function(name) {
  return $(this).is('['+name+']');
}

function renumber_forms( formset ) {
  $.each(formset, function( index, element ) {
    $(element).find('[name], [id]').each( function( item ) {
      old_name = $(this).attr('name');
      if ( old_name != undefined ) {
        $(this).attr('name', replace_field(old_name, '-', 1, index));
      }

      old_id = $(this).attr('id');
      if ( old_id != undefined ) {
        $(this).attr('id', replace_field(old_id, '-', 1, index));
      }
    });
  });

  return formset.length;
}

function replace_field(str, sep, field, newval) {
  split_str = str.split(sep);
  split_str[field] = newval;
  return split_str.join(sep);
}

function form_to_dictionary(form_id) {
  dict = {};
  $(form_id).find('[name]').each( function (i) {
    dict[$(this).attr('name')] = $(this).val();
  });

  return dict;
}

function no_handler(form_group_id) {
  // No-Op - Exists for documentation / code clarity only
}

function add_inline_form(form_group_id, template_id, before_id, child_selector, form_count_id, form_handler) {
  newform = $(template_id).clone(true);
  newform.removeClass('template-form');
  newform.removeAttr('id');

  $(before_id).before(newform);
  
  count = renumber_forms( $(form_group_id).find(child_selector) );
  $(form_count_id).attr('value', count);

  form_handler(form_group_id);
} 
