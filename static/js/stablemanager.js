function attach_mechlist_autocomplete(mech_input, parent_class, model_select_class) {
  src_url = "/stable/query/list-produced";
  if ($('#id_allmechs:checked').length > 0) {
    src_url = "/stable/query/list-produced?all=T";
  }

  mech_input.autocomplete({
    source: src_url,
    minLength: 3,
    select: function (event, ui) {
      var inputbox = $(this);
                
      $.ajax( {
        type : 'get',
        url  : '/stable/query/list-variants',
        dataType : 'json',
        data : {
          mech : ui.item.value
        , all  : ($('#id_allmechs:checked').length > 0)
        },
      }).done(function(json) {
        var option_html="<option value=\"\">--</value>";
        $.each(json, function(index, val) {
          option_html += "<option loadout=\"" + val['loadout'] 
                      + "\"value=\"" + val['code'] 
                      + "\" preview_url=\"" + val['url'] + "\">" 
                      + val['name'] + "</value>";
        }); 
                                                             
        inputbox.parents(parent_class).find(model_select_class).html(option_html);               
      });
    }
  });
}

function handle_preview_config_select() {
  $('#dialog-mechpreview .loadouts a').click( function() {
    $('#dialog-mechpreview').load( $(this).attr('href') + ' div.body', handle_preview_config_select);
        
    return false;
  });   
}

function preview_mech(mech_url) {
  $('#dialog-mechpreview').load(mech_url + ' div.body', function() {
    /* Handle omni-mech browsing within preview pane */
    handle_preview_config_select()
      
    $('#dialog-mechpreview').dialog ({
      modal: true,
      width: (window.innerWidth * 0.75),
      height: (window.innerHeight * 0.75),
      buttons: {
        Close: function() { $( this ).dialog("close"); }
      }
    });
  });
}

function to_ordinal(number) {
  if (number == 1) {
    return number + 'st';
  } else if (number == 2) {
    return number + 'nd';
  } else if (number == 3) {
    return number + 'rd';
  } else {
    return number + 'th';
  }
}

function select_chassis_handler(parent_class, chassis_input_css, cost_class, preview_class) {
  return function() {
    code = $(this).val();
    preview_url = $(this).find(':selected').attr('preview_url');
    loadout = $(this).find(':selected').attr('loadout');
    preview_url = $(this).find(':selected').attr('preview_url');    
    
    chassis = $(this).parents(parent_class).find(chassis_input_css).val();
    cost = $(this).parents(parent_class).find(cost_class);

    $.ajax( {
      type : 'get',
      url  : '/reference/ajax/mech/price-of',
      dataType : 'json',
      data : {
        chassis : encodeURIComponent(chassis)
      , code    : code
      , loadout : loadout
      },
    }).done(function(json) {
      cost.html('-' + json);

      preview = cost.parents(parent_class).find(preview_class);
      preview.prop('disabled', false);

      preview.click(function() {
        preview_mech(preview_url);
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

$( document ).ajaxStop( function() {
  $.ajax({
    type : 'get',
    url  : $('#actionbar-stabledata').attr('data_url'),
    dataType : 'json',
    global : false
  }).done(function(data) {
     $('#actionbar-funds').text(data['funds']);
     $('#actionbar-prominence').text(data['prominence']);
     $('#actionbar-mechs').text(data['mechs']);
     $('#actionbar-pilots').text(data['pilots']);
  });
});
