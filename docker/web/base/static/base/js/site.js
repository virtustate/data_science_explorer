/*
function wireUpAutoSubmit() {
  $(".autoSubmit").each(function (index) {
    $(this).change(function () {
      $(this).closest('form').submit();
    })
  });
}
*/

$(document).ready(function(){
    //alert('jqyuery start')
    //wireUpAutoSubmit();
    // enable bootstrap 4 tooltips
    $(function () {$('[data-toggle="tooltip"]').tooltip()})
    // handler for dataframe selection
    $('#DatasetSelect').change(function() {this.form.submit();})
    $('#HideRunDatasets').change(function() {this.form.submit();})
    // wire up tag edit links
    $(".tag_edit").each(function () {
        $(this).modalForm({formURL: $(this).data('id')});
    });
    // execute any page specific documentready javascript
    pagejq();
    //alert('jquery done')
});

// redirect to a papermill view that serves up a parameterized jupyterlab.sh template
function redirectToJupyter(template,id,option) {
    url='/papermill/' + template + '/' + id + '/' +  option
    window.open(url,'_blank');
}

