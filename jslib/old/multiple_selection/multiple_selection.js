(function($) {

    function addUL(parent) {
        var $ul = $("<ul/>");
        var baseId = "_" + $(parent).attr("id");
        $(parent).children("option,optgroup").each(function(index, tag) {
            if (tag.tagName.toLowerCase() === "option") {
                var $option = $(this);
                var id = baseId + index;
                var $li = $("<li/>").appendTo($ul);
                var $checkbox = $("<input type='checkbox' id='" + id + "'/>").appendTo($li).change(function() {
                    if ($(this).is(":checked")) {
                        $option.attr("selected", "selected");
                    } else {
                        $option.removeAttr("selected");
                    }
                });
                if ($option.is(":selected")) {
                    $checkbox.attr("checked", "checked");
                }
                $checkbox.after("<label for='" + id + "'>" + $option.text() + "</label>");
            } else {
                var optGroupUL = addUL(this);
                var $li = $('<li>' + this.label + '</li>').appendTo($ul)
                optGroupUL.appendTo($ul);
            }
        });
        return $ul;
    }
 
    var methods = {
        init: function() {
            var ul = addUL(this);
            ul.insertAfter(this);
            ul.addClass('multiple_selection');
            $(this).hide();
        }
    };
 
    $.fn.multiSelectToCheckboxes = function(method) {
        if (methods[method]) {
            return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
        } else if (typeof method === 'object' || !method) {
            return methods.init.apply(this, arguments);
        } else {
            $.error('Method ' + method + ' does not exist on jQuery.multiSelectToCheckboxes');
        }
 
    };
 
})(jQuery);

$(function(){
    $('select[multiple]').multiSelectToCheckboxes();
});