
def main(j, args, params, tags, tasklet):
    params.merge(args)

    name = params.tags.tagGet("name")

    out = "space %s succesfully reloaded." % name

    if name.find("$$") != -1:
        out = "ERROR: could not reload the docs for space because param was not specified (need to have param name)."
        params.result = out

        return params

    try:
        space = j.portal.tools.server.active.loadSpace(name, force=True)

    except Exception as e:
        error = e
        out = "ERROR: could not reload the docs for space %s, please check event log." % params.tags.tagGet("name")
        eco = j.errorhandler.processPythonExceptionObject(e)
        eco.process()
        print(eco)

    params.result = (out, params.doc)

    return params


def match(j, args, params, tags, tasklet):
    return True
