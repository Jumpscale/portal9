from collections import OrderedDict


def main(j, args, params, tags, tasklet):
    name = args.getTag('aysname')
    ayspath = args.getTag('ayspath') or None

    if not ayspath:
        template = j.core.atyourservice.actorTemplates[name]
        services = []
    else:
        repo = j.core.atyourservice.repoGet(ayspath)
        template = repo.templates.get(name, None) if repo else None
        services = repo.servicesFind(actor=template.name)

    if template:
        info = {}
        code_bloks = {
            'schema.hrd': template.schemaHrd.content,
            'schema.capnp': template.schemaCapnpText
        }

        info = OrderedDict(sorted(info.items()))
        args.doc.applyTemplate({'data': info, 'services': services, 'code_bloks': code_bloks,
                                'template_name': name, 'reponame': j.sal.fs.getBaseName(ayspath) if ayspath else '',
                                'aysrepo': ayspath})
    else:
        args.doc.applyTemplate({'error': 'template does not exist'})

    params.result = (args.doc, args.doc)
    return params
