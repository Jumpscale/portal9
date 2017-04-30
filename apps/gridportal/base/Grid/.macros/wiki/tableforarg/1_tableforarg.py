def main(j, args, params, tags, tasklet):
    params.merge(args)
    doc = params.doc
    data = args.getTag('data')
    title = args.getTag('title')

    out = "*%s*\n" % title
    try:    
        objargs = j.data.serializer.json.loads(data)
        for key,value in objargs.items():
            if not value:
                value = ''
            out += "|%s|%s|\n"%(str(key),j.portal.tools.html.escape(str(value)))
    except Exception:
        out = ''
    params.result = (out, doc)
    return params
    

def match(j, args, params, tags, tasklet):
    return True
