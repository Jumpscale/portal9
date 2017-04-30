def main(j, args, params, tags, tasklet):
    page = args.page

    page.addCSS("/jslib/old/jquery-ui.css")
    page.addJS("/jslib/old/jquery-ui.js")
    page.addJS("/jslib/old/jquery.facetview.js")
    C = r"""
<script type="text/javascript">
jQuery(document).ready(function($) {
  function pad(num) {
    var s = "0" + num;
    return s.substr(s.length-2);
  };

  function epochToStr(val) {
    var date = new Date(val * 1000);
    return pad(date.getDay()) + "/" + pad(date.getMonth()) + " " + date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds();

  };
  window.filterfunction = function(event, val, filtertype){
    event.defaultPrevented = true;
    if ($('a.facetview_filterchoice[rel='+filtertype+'][href='+val+']').length > 0) {
      if ($('.facetview_filterselected[rel='+filtertype+'][href='+val+']').length == 0){
        $('a.facetview_filterchoice[rel='+filtertype+'][href='+val+']')[0].click();
      }
    }
  };
  function linkify(id) {
      return function(val, inFilter) {
          if (inFilter)
            return val;
          var ancor = $("<a>");
          ancor.attr('id', id);
          ancor.attr('href', '#');
          ancor.attr('title', val);
          ancor.attr('onclick', "filterfunction(event, '"+ val +"', this.id)");
          ancor.html(val);
          return ancor[0].outerHTML;
      };
  };

  function columnFormatter(size) {
      return function(val, inFilter) {
        if (inFilter) {
            return val;
        }
        var container = $('<div>');
        container.html(val);
        container.css('max-width', size)
                 .css('white-space', 'nowrap')
                 .css('overflow', 'hidden')
                 .css('text-overflow', 'ellipsis');

        return container[0].outerHTML;
      }
  }

  function formatJID(val, inFilter) {
      if (!val) {
        return "";
      }
      val = linkify('jid')(val, inFilter);
      return columnFormatter('40px')(val, inFilter);
  };

  var hostname = window.location.hostname;
  $('.facet-view-simple').facetview({
    search_url: 'http://'+hostname+':9200/clusterlog/_search?',
    search_index: 'elasticsearch',
    display_header: true,
    resultwrap_start: '<tr>',
    resultwrap_end: '</tr>',
    display_columns: true,
    default_freetext_fuzzify: '*',
    enable_rangeselect: false,
    pushstate:true,
    linkify: false,
    facets: [
        {'field': 'epoch', 'display': 'Time', 'size': 100},
        {'field': 'appname', 'display': 'App Name'},
        {'field': 'category', 'display': 'Category'},
        {'field': 'level', 'display': 'Level'},
        {'field': 'message', 'display': 'Message'},
        {'field': 'jid', 'display': 'JID'},
        {'field': 'gid', 'display': 'GID'},
        {'field': 'nid', 'display': 'NID'},
        {'field': 'pid', 'display': 'PID'},
        {'field': 'aid', 'display': 'AID'},
    ],
    result_display: [[{field: "epoch", formatter: epochToStr},
                      {field: "appname", formatter: columnFormatter('90px')},
                      {field: "category", formatter: columnFormatter('90px')},
                      {field: "level"},
                      {field: "message", formatter: columnFormatter('300px')},
                      {field: "jid", formatter: formatJID},
                      {field: "gid", formatter: linkify('gid')},
                      {field: "nid", formatter: linkify('nid')},
                      {field: "pid", formatter: linkify('pid')},
                      {field: "aid", formatter: linkify('aid')}
                      ]],
    paging: {
      size: 100
    },
  });

});

$('body').on('click', '#facetview_results tr', function(e){
        e.preventDefault(); e.stopPropagation();
        data = '';
        children = $(this).children();
        headers = ['Time: ', 'Application Name: ', 'Category: ', 'Level: ', 'Message: ', 'Job ID: ', 'Grid ID: ', 'Node ID: ', 'Process ID: ', 'Application ID: '];
        for (var i=0;i<children.length;i++){
            data += headers[i] + $(children[i]).text() + '</br>';
        }
        $("#dialog-message").html(data);
        $("#dialog-message").dialog({
            modal: true,
            draggable: true,
            resizable: false,
            position: ['center'],
            width: 400
        });
        return false;
   });


// Put ellipsis on the 'message' column
setInterval(function() {
  $('#facetview_pid').hide();
  $('#facetview_message').hide();
  $('#facetview_epoch').hide();

  $('#facetview_results tr').each(function() {
      var elt = $(this);
      elt.find('td').attr('title', elt.text());
    });
  }, 500)

  </script>

<div class="facet-view-simple"></div>
<div id="dialog-message" style="display:none;"></div>
    """

    page.addMessage(C)
    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True
