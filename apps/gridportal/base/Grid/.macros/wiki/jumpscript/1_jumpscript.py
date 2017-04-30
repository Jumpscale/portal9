
def main(j, args, params, tags, tasklet):

    params.merge(args)
    doc = params.doc
    # tags = params.tags

    actor=j.apps.actorsloader.getActor("system","gridmanager")

    organization = args.getTag("organization")
    name = args.getTag("jsname")

    out = ''
    missing = False
    for k,v in {'organization':organization, 'name':name}.items():
        if not v:
            out += 'Missing param %s.\n' % k
            missing = True

    if not missing:
        obj = actor.getJumpscript(organization=organization, name=name)

        out = ['||Property||Value||']

        for k,v in obj.items():
            if k in ('args', 'roles'):
                v = ' ,'.join(v)
            if k == 'source':
                continue
            v = j.data.text.toStr(v)
            out.append("|%s|%s|" % (k.capitalize(), v.replace('\n', '') if v else v))

        out.append('\n{{code:\n%s\n}}' % obj['source'])
        out = '\n'.join(out)
    doc.applyTemplate({'name': name})

    params.result = (out, doc)
    return params


def match(j, args, params, tags, tasklet):
    return True
