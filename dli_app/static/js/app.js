$(function() {
  $('.datepicker').datepicker({
    endDate: 'today',
    format: 'yyyy-mm-dd',
    autoclose: 'true'
  });

  $('a[data-method]').click(function(e) {
    method = $(this).data('method');
    action = $(this).attr('href');
    csrf   = $('meta[name=csrf-token]').attr('content');

    // Allow GET requests to go through normally
    if(method == 'GET') return true;
    // Prevent all other requests from executing
    e.preventDefault();

    // Create a form object with the appropriate method and action
    var form = $('<form></form>');
    form.attr('method', method);
    form.attr('action', action);
    form.append('<input type="hidden" name="csrf_token" value="'+csrf+'" />');

    $(document.body).append(form);
    form.submit();
  });
});
