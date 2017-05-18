def main(j, args, params, tags, tasklet):
    id = args.getTag('id')

    if not id:
        out = 'Missing ID'
        params.result = (out, args.doc)
        return params

    group = j.portal.tools.models.system.Group.get(id)
    if not group:
        out = 'Could not find Group: %s' % id
        params.result = (out, args.doc)
        return params

    obj = group.to_dict()
    args.doc.applyTemplate(obj)
    params.result = (args.doc, args.doc)

    return params
