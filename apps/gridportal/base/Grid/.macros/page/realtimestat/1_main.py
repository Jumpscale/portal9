def main(j, args, params, tags, tasklet):

    page = args.page
  
    nid = args.getTag('nid')
    statistic = args.getTag('statistic')
    
    out = ''
    missing = False
    for k, v in (('nid', nid), ('statistic', statistic)):
        if not v:
            out += 'Missing param "%s".<br>' % k
            missing = True

    if missing:
        page.addMessage(out)
        params.result = page
        return params



    page.addBodyAttribute('ng-app="jumpscale"')

    page.addJS("/jslib/jquery/jquery-1.10.1.js")

    page.addCSS("/jslib/jqplot/jquery.jqplot.min.css")

    page.addJS("/jslib/jqplot/jquery.jqplot.min.js")
    page.addJS("/jslib/jqplot/plugins/jqplot.cursor.min.js")
    page.addJS("/jslib/jqplot/plugins/jqplot.canvasTextRenderer.min.js")
    page.addJS("/jslib/jqplot/plugins/jqplot.canvasAxisTickRenderer.js")

    page.addJS("/jslib/jqplot/plugins/jqplot.canvasAxisLabelRenderer.min.js")
    page.addJS("/jslib/jqplot/plugins/jqplot.dateAxisRenderer.js")

    page.addJS("/jslib/jqplot/plugins/jqplot.enhancedLegendRenderer.min.js")

    page.addJS("/jslib/angular/angular.js")
    page.addJS(".files/app.js")
    page.addJS(".files/directives.js")

    if nid:
        print(nid)

    url = '/restmachine/system/gridmanager/getNodeSystemStats?nid=%s' % nid
    import random
    randomid = random.randint(1, 999999999999)
    page.addHTML('<div id="statisticsChart%s" data-chart ng-model="statisticsData" ng-url="%s" ng-stat="%s" style="width: 100%%;"></div>' % (randomid, url, statistic))

    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True
