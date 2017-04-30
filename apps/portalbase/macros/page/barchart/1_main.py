import random
from itertools import count


def main(j, args, params, tags, tasklet):
    page = args.page

    page._addChartJS()
    hrd = j.data.hrd.get(content=args.cmdstr)
    title = hrd.title
    height = hrd.getInt('height')
    width = hrd.getInt('width')
    headers = hrd.getList('headers')
    try:
        onclickfunction = hrd.get('onclickfunction')
    except:
        onclickfunction = ''

    data = []
    legends = []
    for i in count(1):
        key = 'data_%s' % i
        try:
            legend = hrd.get(key + '_legend')
        except RuntimeError:
            break
        else:
            item_data = [int(x) for x in hrd.getList(key + '_data')]
            data.append(item_data)
            legends.append(legend)

    chart_id = 'chart-%s' % random.randint(1, 99999)
    page.addJS(jsContent='''$(function () {
onclickfunction = function(){ %(onclickfunction)s }
    var bar = new RGraph.Bar('%(chart_id)s', %(data)s);

    bar.Set('chart.title', '%(title)s');
    bar.Set('chart.labels', %(headers)s);
    bar.Set('chart.key', %(legends)s);
    bar.Set('chart.gutter.left', 90);
    bar.Set('chart.events.click', onclickfunction);

    bar.Draw();


});''' % {'chart_id': chart_id, 'data': [list(t) for t in zip(*data)], 'title': title, 'headers': headers, 'legends': legends, 'onclickfunction': onclickfunction})

    page.addMessage('<canvas id="%s" width="%s" height="%s">[No Canvas Support!]</canvas>' % (chart_id, height, width))
    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True
