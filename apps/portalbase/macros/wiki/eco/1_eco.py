
def main(j, args, params, tags, tasklet):
    id = args.getTag('id')
    ukey = args.getTag('ukey')
    if not id and not ukey:
        params.result = (args.doc, args.doc)
        args.doc.applyTemplate({})
        return params

    eco = None
    if id:
        eco = j.portal.tools.models.system.Errorcondition.get(id)
    elif ukey:
        eco = j.portal.tools.models.system.Errorcondition.objects(uniquekey=ukey).first()
    if not eco:
        params.result = (args.doc, args.doc)
        args.doc.applyTemplate({})
        return params

    args.doc.applyTemplate({'eco': eco})
    params.result = (args.doc, args.doc)
    return params
