def main(j, args, params, tags, tasklet):
    params.merge(args)
    doc = params.doc

    id = args.getTag('ecoid')

    out = "[*Error Condition Object Details*|error condition?id=%s]" % id

    params.result = (out, doc)
    return params
    

def match(j, args, params, tags, tasklet):
    return True
