function attach_mechlist_autocomplete(mech_input, parent_class, model_select_class) {
  mech_input.autocomplete({
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
          option_html += "<option value=\"" + encodeURIComponent(val) + "\">" + val + "</value>";
        }); 
                                                             
        inputbox.parents(parent_class).find(model_select_class).html(option_html);               
      });
    }
  });
}

function preview_mech(chassis, model) {
  $('#dialog-mechpreview').load('/reference/mechs/' + chassis + '/' + model + ' div.body');
  $('#dialog-mechpreview').dialog ({
    modal: true,
    width: (window.innerWidth * 0.75),
    height: (window.innerHeight * 0.75),
    buttons: {
      Close: function() { $( this ).dialog("close"); }
    }
  });
}

function select_chassis_handler(parent_class, chassis_input_css, cost_class, preview_class) {
  return function() {
    type = $(this).val();
    chassis = $(this).parents(parent_class).find(chassis_input_css).val();
    cost = $(this).parents(parent_class).find(cost_class);

    $.ajax( {
      type : 'get',
      url  : '/reference/ajax/mech/price-of',
      dataType : 'json',
      data : {
        chassis : encodeURIComponent(chassis)
      , type    : type 
      },
    }).done(function(json) {
      cost.html('-' + json);

      preview = cost.parents(parent_class).find(preview_class);
      preview.prop('disabled', false);

      preview.click(function() {
        preview_mech(chassis, type);
      });
    }); 
  }
}

$( document ).ready(function() {
  $('#browse-next-week.create-post').click( function() {
    $.ajax({
      type : 'post'
    , url  : '/stable/create'
    , dataType : 'json'
    , data : {
        view : $(this).attr('viewname')
      , week : $(this).attr('week')
      }
    , beforeSend: function(jqXHR, plainObj) {
        $('#browse-next-week .spinner').show();
        $('#browse-next-week .action').hide();
      } 
    , complete: function(jqXJR, plainObj) {
        $('#browse-next-week .spinner').hide();
        $('#browse-next-week .action').show();
      } 
    }).done( function(newpage) {
      window.location.href = newpage;
    });
  });

});
