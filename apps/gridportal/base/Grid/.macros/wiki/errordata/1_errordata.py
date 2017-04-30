def main(j, args, params, tags, tasklet):
    params.merge(args)
    doc = params.doc
    result = args.getTag('result')
    result = result
    if result == 'None':
        result = ''
    else:
        result = '{{code: \n%s\n}}' % result
    params.result = (result, doc)
    return params
    

def match(j, args, params, tags, tasklet):
    return True