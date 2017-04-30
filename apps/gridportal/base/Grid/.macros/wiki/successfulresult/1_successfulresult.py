def main(j, args, params, tags, tasklet):
    params.merge(args)
    doc = params.doc
    result = args.getTag('result')
    if result == 'None':
        result = ''
    result = """{{code
%s
}}""" % result
    params.result = (result, doc)
    return params
    

def match(j, args, params, tags, tasklet):
    return True
