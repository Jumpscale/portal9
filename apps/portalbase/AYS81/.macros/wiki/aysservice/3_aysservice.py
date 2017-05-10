from collections import OrderedDict


def main(j, args, params, tags, tasklet):
    try:
        role = args.getTag('aysrole')
        name = args.getTag('aysname')
        reponame = args.getTag('reponame')

        ctx = args.requestContext
        aysactor = j.apps.actorsloader.getActor('system', 'atyourservice')
        client = aysactor.get_client(ctx=ctx)
        service = client.getServiceByName(name, role, reponame).json()
        if service:
            link_to_template = ('[%s|ays81/ActorTemplate?aysname=%s]' % (role, role))

            # we prepend service path with '$codedir' to make it work in the explorer.
            # because of this line :
            # https://github.com/Jumpscale/jumpscale_portal8/blob/master/apps/portalbase/macros/page/explorer/1_main.py#L25

            hidden = ['key.priv', 'password', 'passwd', 'pwd', 'oauth.jwt_key', 'keyPriv']
            data_revised = dict()
            for k, v in service.items():
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
                'reponame': reponame,
            })

        else:
            args.doc.applyTemplate({'error': 'service not found'})

    except Exception as e:
        args.doc.applyTemplate({'error': e.__str__()})

    params.result = (args.doc, args.doc)
    return params
