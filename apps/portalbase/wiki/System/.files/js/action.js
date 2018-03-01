
function js_action_button() {

    $('.js_action').click(function(){
        var $this = $(this);
        var action = $this.data('action');
        var modal = $("#"+action);
        modal.parents('form').data('extradata', $this.data('extradata'));
        modal.parents('form').data('extracallback', function() {
            if ($this.data('deleterow')) {
                $this.parents('tr').remove();
            }
        });
        modal.modal('show');
    });
}


$(document).ready(
function(){
    js_action_button();
    $('.dataTables_paginate li').on("click", js_action_button);
});
