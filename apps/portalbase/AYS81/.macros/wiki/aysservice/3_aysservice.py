from collections import OrderedDict


def main(j, args, params, tags, tasklet):
    role = args.getTag('aysrole')
    name = args.getTag('aysname')
    ayspath = args.getTag('ayspath') or ''

    repo = j.core.atyourservice.repoGet(ayspath)
    service = repo.serviceGet(role, name, die=False)
    if service:
        prods = {}
        for role, producers in service.producers.items():
            prods.setdefault(role, [])
            for producer in producers:
                prods[role].append('[{name}|/ays81/Service?aysrole={role}&aysname={name}&ayspath={path}]'.format(
                    role=role, path=ayspath, name=producer.model.dbobj.name))

        parent = {}
        if service.parent is not None:
            parent['link'] = '[{name}|/ays81/Service?aysrole={role}&aysname={name}&ayspath={path}]'.format(
                role=service.parent.model.role, path=ayspath, name=service.parent.model.dbobj.name)

        link_to_template = ('[%s|ays81/ActorTemplate?ayspath=%s&aysname=%s]' % (role,
                                                                                ayspath, role))

        # we prepend service path with '$codedir' to make it work in the explorer.
        # because of this line :
        # https://github.com/Jumpscale/jumpscale_portal8/blob/master/apps/portalbase/macros/page/explorer/1_main.py#L25

        hidden = ['key.priv', 'password', 'passwd', 'pwd', 'oauth.jwt_key', 'keyPriv']
        data = j.data.serializer.json.loads(service.model.dataJSON)
        data_revised = dict()
        for k, v in data.items():
            if k.strip() in hidden:
                continue
            else:
                data_revised[k] = v.replace('\\n', '') if isinstance(v, str) else v

        args.doc.applyTemplate({
            'service': service,
            'type': link_to_template,
            'data': data_revised,
            'name': name,
            'role': role,
            'producers': OrderedDict(sorted(prods.items())),
            'parent': parent,
            'actions': service.model.actions,
            'reponame': service.aysrepo.name,
        })

    else:
        args.doc.applyTemplate({'error': 'service not found'})

    params.result = (args.doc, args.doc)
    return params
