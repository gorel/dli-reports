$(function() {
  $('.datepicker').datepicker({
    endDate: 'today',
    format: 'yyyy-mm-dd',
    autoclose: 'true'
  });

  $('#loading_spinner').hide();

  $('#search_text').on('keyup', function() {
    form_data = {
      'filter_choices': $('#filter_choices').val(),
      'search_text': $(this).val(),
      'csrf_token': $('#csrf_token').val()
    };

    $('#loading_spinner').show();
    $('#search_target').load('/reports/search/', form_data, function() {
      $('#loading_spinner').hide();
    });
  });
});
