def main(j, args, params, tags, tasklet):
    import yaml
    import ujson as json
    import re

    params.result = (args.doc, args.doc)
    id = args.getTag('id')

    if not id:
        args.doc.applyTemplate({})
        return params

    audit = j.portal.tools.models.system.Audit.get(id)
    if not audit:
        args.doc.applyTemplate({'id': None})
        return params
    r = re.search(r'eco-\d+-(?P<ecoguid>\w{8}-\w{4}-\w{4}-\w{4}-\w{12})', audit.result)
    link = ""
    if r:
        link = r.group('ecoguid')
    for key in ('kwargs', 'args', 'result'):
        obj = json.loads(audit[key])
        if key == 'result' and isinstance(obj, list) and len(obj) == 1:
            obj = obj[0]
            try:
                obj = json.loads(obj)
            except:
                pass
        audit[key] = yaml.safe_dump(obj, default_flow_style=False)

    args.doc.applyTemplate({'audit': audit, 'ecolink': link})
    return params
