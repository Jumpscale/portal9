
def main(j, args, params, tags, tasklet):

    params.merge(args)
    doc = params.doc

    actor = j.apps.actorsloader.getActor("system", "gridmanager")
    
    out = []

    #this makes sure bootstrap datatables functionality is used
    out.append("{{datatables_use}}\n")

    #[u'otherid', u'description', u'roles', u'mem', u'netaddr', u'ipaddr', u'nid', u'lastcheck', u'state', u'gid', u'active', u'cpucore', u'type', u'id', u'name']
    fields = ['name', 'organization', 'category', 'descr']

    out.append('||Name||Organization||Category||Description||')

    for jscript in actor.getJumpscripts():

        line = [""]

        for field in fields:
            # add links
            value = jscript[field]
            if field == 'name':
                line.append('[%s|/grid/jumpscript?organization=%s&name=%s]' % (value, jscript['organization'], value))
            else:
                text = str(value).replace('\n', '')
                line.append(str(text))

        line.append("")
        out.append("|".join(line))

    params.result = ('\n'.join(out), doc)

    return params


def match(j, args, params, tags, tasklet):
    return True
