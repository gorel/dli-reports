$(function() {
  // Datepickers
  $('.datepicker').datepicker({
    endDate: 'today',
    format: 'yyyy-mm-dd',
    autoclose: 'true'
  });



  // Anchor tag override
  $('a[data-method]').click(function(e) {
    method = $(this).data('method');
    action = $(this).attr('href');
    csrf   = $('meta[name=csrf-token]').attr('content');

    // Allow GET requests to go through normally
    if(method == 'GET') return true;
    // Prevent default request actions from executing
    e.preventDefault();

    // Create a form object with the appropriate method and action
    var form = $('<form></form>');
    form.attr('method', method);
    form.attr('action', action);
    form.append('<input type="hidden" name="csrf_token" value="'+csrf+'" />');

    // Require confirm if specified
    confirm_message = $(this).data('confirm');
    if(confirm_message && !window.confirm(confirm_message)) return true;

    // Submit the form
    $(document.body).append(form);
    form.submit();
  });



  // Report and Chart form fun
  $('.field-selector .selected-fields')
    .sortable({
      axis: 'y',
      items: '.department-field',
      opacity: 0.4,
      containment: 'parent',
      tolerance: 'pointer',
      handle: '.handle',
      receive: function(event, ui) {
        dropped = $(ui.helper);
        text = dropped.text();
        dropped
          .attr('id', dropped.data('id'))
          .empty()
          .removeAttr('style')
          .append('<div class="handle"><span class="fa fa-th"></span></div>')
          .append('<div class="content"><span class="name">' + text + '</span"><span class="department">' + dropped.data('department') + '</span></div>')
          .append('<div class="actions-cell"><div class="actions"><a class="btn btn-blank text-danger remove-field-btn"><span class="fa fa-remove"></span></a></div></div>');

        return dropped;
      }
    })
    .disableSelection();

  // Programmatically add selected fields to the "selected" side
  $('.field-selector .department-field .add-field-btn').click(function() {
    // Add the field
    selected_fields = $('.field-selector .selected-fields');
    sortable_insert = selected_fields.sortable('option','receive');
    selected_fields.append(sortable_insert(null, {
      helper: $(this).closest('.department-field').clone()
    }));

    // Change the action to "remove" and disable the element
    $(this).closest('.department-field').removeClass('unadded').addClass('added');
  });

  // Programmatically remove selected fields from the "selected" side
  $('.field-selector .department-field .remove-field-btn').click(function() {
    // Remove the field
    selected_fields = $('.field-selector .selected-fields');
    selected_fields.children().remove('[data-id='+$(this).closest('.department-field').data('id')+']');

    // Change the action to "add" and re-enable the element
    $(this).closest('.department-field').removeClass('added').addClass('unadded');
  });

  $('#create_report_form, #edit_report_form, #create_chart_form, #edit_chart_form').submit(function() {
    form = $(this);
    $(this).children('.field-selector').each(function() {
      fields = $(this).find('.selected-fields');
      form.append('<input type="hidden" name="' + $(this).data('form-name') + '" value="' + fields.sortable('toArray') + '">');
    });
  });
});
