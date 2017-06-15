def main(j, args, params, tags, tasklet):
    doc = args.doc
    actors = j.portal.tools.server.active.getActors()

    out = ""

    groups = dict()
    for actor in actors:
        group_name = actor.split('__')[0]
        if group_name not in groups.keys():
            groups[group_name] = [actor]
        groups[group_name].append(actor)

    for group in sorted(groups.keys()):
        out += "|[%(gr)s actors|/system/ActorApi?group=%(gr)s]|\n" % {'gr': group}

    params.result = (out, doc)
    return params
