
def main(j, args, params, tags, tasklet):
    """
    {{spaces}}
    """
    params.merge(args)

    doc = params.doc

    out = "{{datatables_use}}\n"

    bullets = params.tags.labelExists("bullets")
    table = params.tags.labelExists("table")
    isgitlab = j.portal.tools.server.active.authentication_method == 'gitlab'
    addSpinner = isgitlab

    spaces = j.portal.tools.server.active.getUserSpaces(params.requestContext)
    if isgitlab:
        gitlabnonclonedspaces = [s[s.index('portal_'):]
                                 for s in j.portal.tools.server.active.getNonClonedGitlabSpaces(params.requestContext)]
        spaces = {}
        for s in j.portal.tools.server.active.getUserSpacesObjects(params.requestContext):
            if s['namespace']['name']:
                spaces[s['name']] = "%s_%s" % (s['namespace']['name'], s['name'])
            else:
                spaces[s['name']] = s['name']
    else:
        spaces = {}
        for spaceid in j.portal.tools.server.active.getUserSpaces(params.requestContext):
            space = j.portal.tools.server.active.getSpace(spaceid, ignore_doc_processor=True)
            if space.model.hidden:
                continue
            spaces[spaceid] = space.model.name

    excludes = []
    if params.tags.tagExists("exclude"):
        excludes = params.tags.tagGet("exclude").split(",")
        excludes = [item.strip().lower() for item in excludes]

    for spaceid, name in sorted(iter(spaces.items()), key=lambda x: x[1]):
        spaceid = spaceid.lower()
        if spaceid not in excludes:
            anchor = spaceid.strip("/")
            if table:
                out += "|[%s|/%s]|" % (name, anchor)
            else:
                if item[0] != "_" and item.strip() != "" and item.find("space_system") == -1:
                    if bullets:
                        out += "* [%s|/%s]" % (item, anchor)
                    else:
                        out += "[%s|/%s]" % (item, anchor)

            if addSpinner:
                if item.startswith("portal_"):
                    classname = "loadspace"
                    if item in gitlabnonclonedspaces:
                        classname += " new-repo"
                    out += '{{div:class=%s}}|' % classname
                else:
                    out += '{{div}}|'
            out += '\n'

    if addSpinner:
        out += '{{html:<script src="/jslib/spin.min.js"></script>}}'
        out += '{{html:<script src="/jslib/gitlab/loadUserSpacesAsyncronously.js"></script>}}'

    params.result = (out, doc)

    return params


def match(j, args, params, tags, tasklet):
    return True
