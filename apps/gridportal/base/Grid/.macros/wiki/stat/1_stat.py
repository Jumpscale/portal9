
def main(j, args, params, tags, tasklet):
    params.merge(args)

    doc = params.doc

    #key always starts with n$nr.$key
    #e.g. n1.process....

    key = args.getTag('key')
    width = args.getTag('width', 800)
    height = args.getTag('height', 400)

    out = '!/restmachine/system/gridmanager/getStatImage?statKey=%s&width=%s&height=%s!'%(key,width,height)
    
    params.result = (out, doc)

    return params


def match(j, args, params, tags, tasklet):
    return True
