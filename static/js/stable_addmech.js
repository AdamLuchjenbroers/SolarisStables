$( document ).ready(function() {
  $('span.mech-name input').autocomplete({
      source: "/stable/query/list-produced",
      minLength: 3
  });
});