def main(j, args, params, tags, tasklet):
    page = args.page
    data = {'action': args.getTag('id'),
            'class': args.getTag('class') or '',
            'deleterow': args.getTag('deleterow') or 'false',
            'label': args.getTag('label') or '',
            }

    extradata = {}
    tags = j.data.tags.getObject(args.cmdstr, None)
    for tagname, tagvalue in tags.getDict().items():
        if tagname.startswith('data-'):
            extradata[tagname[5:]] = tagvalue

    data['data'] = j.data.serializer.json.dumps(extradata)

    if data['class']:
        data['label'] = "<span class='%(class)s'></span> %(label)s" % data
    element = "<a class='js_action'" \
              " data-action='%(action)s'" \
              " data-extradata='%(data)s'" \
              " data-deleterow='%(deleterow)s'" \
              "href='javascript:void(0);'>%(label)s</a>" % data
    page.addMessage(element)

    page.addJS('/system/.files/js/action.js', header=False)
    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True
