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
    if ( $(this).is('[type=checkbox]:not(:checked),[type=radio]:not(:checked)')) {
      // This element is an unchecked checkbox or radio-button, so skip it.
      return true;
    }
    dict[$(this).attr('name')] = $(this).val();
  });

  return dict;
}

function no_handler(form_group_id) {
  // No-Op - Exists for documentation / code clarity only
}

function update_form_count(form_count_id, form_group_id, child_selector) {
  count = renumber_forms( $(form_group_id).find(child_selector) );
  $(form_count_id).attr('value', count);
}

function add_inline_form(form_group_id, template_id, before_id, child_selector, form_count_id, form_handler) {
  newform = $(template_id).clone(true);
  newform.removeClass('template-form');
  newform.removeAttr('id');

  $(before_id).before(newform);

  update_form_count(form_count_id, form_group_id, child_selector);

  form_handler(form_group_id);
} 

function to_number_input(field, sender) {
  oldvalue = field.html();
  value = parseInt(field.text());

  input = '<input type=\'number\' value=\'' + value +'\'></input>';
  field.html(input);
  input = field.find('input');
  input.on('focusout', function() {
    sender(field, value);
  });
}
