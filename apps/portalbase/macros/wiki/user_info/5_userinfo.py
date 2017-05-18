

def main(j, args, params, tags, tasklet):
    id = args.getTag('id')
    if not id:
        out = 'Missing ID'
        params.result = (out, args.doc)
        return params

    user = j.portal.tools.models.system.User.get(id)
    if not user:
        out = 'Could not find user with ID: %s' % id
        params.result = (out, args.doc)
        return params

    obj = user.to_dict()
    obj['breadcrumbname'] = obj['name']
    args.doc.applyTemplate(obj)
    params.result = (args.doc, args.doc)
    return params
