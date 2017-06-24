
def main(j, args, params, tags, tasklet):
    id = args.getTag('id')
    if not id:
        params.result = (args.doc, args.doc)
        args.doc.applyTemplate({})
        return params

    eco = j.portal.tools.models.system.Errorcondition.get(id)
    if not eco:
        params.result = (args.doc, args.doc)
        args.doc.applyTemplate({})
        return params

    args.doc.applyTemplate({'eco': eco})
    params.result = (args.doc, args.doc)
    return params
