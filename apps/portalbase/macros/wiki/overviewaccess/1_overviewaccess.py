
def main(j, args, params, tags, tasklet):
    params.merge(args)

    doc = params.doc
    space = params.paramsExtra.get('space')
    space = params.tags.tagGet('space', space)

    params.result = ""

    out = "{{datatables_use}}\n"
    singlespace = False
    if space != 'system':
        spaces = [space] if space else [params.paramsExtra['space']]
        out += 'h2. Access Overview of Space "%s"\n\n' % spaces[0]
        singlespace = True
    else:
        spaces = list(j.portal.tools.server.active.spacesloader.spaces.keys())
        out += "h2. Acess Overview of Spaces\n\n"

    if spaces:
        if not singlespace:
            out += "||Space"
        out += "||Name||Right||Emails||Groups||\n"
    for spacename in sorted(spaces):
        try:
            space = j.portal.tools.server.active.spacesloader.getSpaceFromId(spacename)
        except:
            params.result = "ERROR: Could not find space %s" % spacename
            return params

        memberace = {}
        for groupname in list(space.model.acl.keys()):
            try:
                group = j.portal.tools.server.active.auth.getGroupInfo(groupname)
            except:
                continue
            if group is not None:
                for membername in [user.name for user in j.portal.tools.models.system.User.find({"groups": group.name})]:
                    if membername not in memberace:
                        memberace[membername] = []
                    right = space.model.acl[groupname]
                    for rightItem in right:
                        if rightItem not in memberace[membername]:
                            memberace[membername].append(rightItem)
        msorted = sorted(memberace.keys())
        for name in msorted:
            right = ",".join(memberace[name])
            user = j.portal.tools.server.active.auth.getUserInfo(name)
            if not singlespace:
                out += "|%s" % spacename
            if isinstance(user.emails, str):
                user.emails = [user.emails]
            out += "|%s|%s|%s|%s|\n" % (name,
                                                        right,
                                                        ",".join(
                                                            user.emails),
                                                        ",".join(
                                                            user.groups))

    params.result = (out, doc)

    return params


def match(j, args, params, tags, tasklet):
    return True
