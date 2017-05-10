$(document).ready(function () {
var fields = [
         { name: "title", type: "string" },
         { name: "status", map: "state", type: "string" },
         { name: "text", map: "title", type: "string" },
         { name: "tags", type: "string" },
         { name: "color", map: "hex", type: "string" },
         { name: "resourceId", type: "number" }
];
var source =
 {
     localData: {{issues}},
     dataType: "array",
     dataFields: fields
 };
var dataAdapter = new $.jqx.dataAdapter(source);
var resourcesAdapterFunc = function () {
    var resourcesSource =
    {
        localData: {{users}},
        dataType: "array",
        dataFields: [
             { name: "id", type: "number" },
             { name: "name", type: "string" },
             { name: "image", type: "string" },
             { name: "common", type: "boolean" }
        ]
    };
    var resourcesDataAdapter = new $.jqx.dataAdapter(resourcesSource);
    return resourcesDataAdapter;
}
var getIconClassName = function () {
    return "jqx-icon-plus-alt";
}

var templateContent = { status: "new", text: "New text", content: "New content", tags: null, color: "green", resourceId: 0, className: ""};

$('#kanban1').jqxKanban({
    templateContent: templateContent,
    template: "<div class='jqx-kanban-item' id=''>"
            + "<div class='jqx-kanban-item-color-status'></div>"
            + "<div style='display: none;' class='jqx-kanban-item-avatar'></div>"
            + "<div class='jqx-icon jqx-icon-close jqx-kanban-item-template-content jqx-kanban-template-icon'></div>"
            + "<div class='jqx-kanban-item-text'></div>"
            + "<div class='jqx-kanban-item-footer'></div>"
    + "</div>",
    resources: resourcesAdapterFunc(),
    source: dataAdapter,
    // render items.
    itemRenderer: function (item, data, resource) {
        $(item).find(".jqx-kanban-item-color-status").html("<span style='line-height: 23px; margin-left: 5px;'>" + resource.name + "</span>");
        $(item).find(".jqx-kanban-item-text").css('background', item.color);
        item.on('dblclick', function (event) {
            var input = $("<textarea placeholder='(No Title)' style='border: none; width: 100%%;' class='jqx-input'></textarea>");
            var addToHeader = false;
            var header = null;
            if (event.target.nodeName == "SPAN" && $(event.target).parent().hasClass('jqx-kanban-item-color-status')) {
                var input = $("<input placeholder='(No Title)' style='border: none; background: transparent; width: 80%%;' class='jqx-input'/>");
                // add to header
                header = event.target;
                header.innerHTML = "";
                input.val($(event.target).text());
                $(header).append(input);
                addToHeader = true;
            }
            if (!addToHeader) {
                var textElement = item.find(".jqx-kanban-item-text");
                input.val(textElement.text());
                textElement[0].innerHTML = "";
                textElement.append(input);
            }
            input.mousedown(function (event) {
                event.stopPropagation();
            });
            input.mouseup(function (event) {
                event.stopPropagation();
            });
            input.blur(function () {
                var value = input.val();
                if (!addToHeader) {
                    $("<span>" + value + "</span>").appendTo(textElement);
                }
                else {
                    header.innerHTML = value;
                }
                input.remove();
            });
            input.keydown(function (event) {
                if (event.keyCode == 13) {
                    if (!header) {
                        $("<span>" + $(event.target).val() + "</span>").insertBefore($(event.target));
                        $(event.target).remove();
                    }
                    else {
                        header.innerHTML = $(event.target).val();
                    }
                }
            });
            input.focus();
        });
    },
    columns: [
        { text: "Backlog", iconClassName: getIconClassName(), dataField: "new", maxItems: 100 },
        { text: "In Progress", iconClassName: getIconClassName(), dataField: "inprogress", maxItems: 100 },
        { text: "Question", iconClassName: getIconClassName(), dataField: "question", maxItems: 100 },
        { text: "Verification", iconClassName: getIconClassName(), dataField: "verification", maxItems: 100 },
        { text: "Done", iconClassName: getIconClassName(), dataField: "closed", maxItems: 100 }
    ],
    // render column headers.
    columnRenderer: function (element, collapsedElement, column) {
        var columnItems = $("#kanban1").jqxKanban('getColumnItems', column.dataField).length;
        // update header's status.
        element.find(".jqx-kanban-column-header-status").html(" (" + columnItems + "/" + column.maxItems + ")");
        // update collapsed header's status.
        collapsedElement.find(".jqx-kanban-column-header-status").html(" (" + columnItems + "/" + column.maxItems + ")");
    }
});
// handle item clicks.
$('#kanban1').on("itemAttrClicked", function (event) {
    var args = event.args;
    if (args.attribute == "template") {
        $('#kanban1').jqxKanban('removeItem', args.item.id);
    }
});
// handle column clicks.
var itemIndex = 0;
$('#kanban1').on('columnAttrClicked', function (event) {
    var args = event.args;
    if (args.attribute == "button") {
        args.cancelToggle = true;
        if (!args.column.collapsed) {
            var colors = ['#f19b60', '#5dc3f0', '#6bbd49', '#dddddd']
            $('#kanban1').jqxKanban('addItem', { status: args.column.dataField, text: "<textarea placeholder='(No Title)' style='width: 96%%; margin-top:2px; border-radius: 3px; border:none; line-height:20px; height: 50px;' class='jqx-input' id='newItem" + itemIndex + "' value=''></textarea>", tags: "new task", color: colors[Math.floor(Math.random() * 4)], resourceId: null });
            var input = $("#newItem" + itemIndex);
            input.mousedown(function (event) {
                event.stopPropagation();
            });
            input.mouseup(function (event) {
                event.stopPropagation();
            });
            input.keydown(function (event) {
                if (event.keyCode == 13) {
                    $("<span>" + $(event.target).val() + "</span>").insertBefore($(event.target));
                    $(event.target).remove();
                }
            });
            input.focus();
            itemIndex++;
        }
    }
});
});