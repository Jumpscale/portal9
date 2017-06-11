
def main(j, args, params, tags, tasklet):
    params.merge(args)

    name = params.tags.tagGet("spacename")

    out = "Space \"%s\" succesfully deleted." % name

    if name.find("$$") != -1:
        out = "ERROR: could not delete the space because param was not specified (need to have param spacename)."
        params.result = out

        return params

    try:
        space = j.portal.tools.server.active.deleteSpace(name)

    except Exception as e:
        error = e
        out = "ERROR: could not reload the docs for space %s, please check event log." % params.tags.tagGet("spacename")
        eco = j.errorhandler.processPythonExceptionObject(e)
        eco.process()
        print(eco)

    params.result = (out, params.doc)

    return params


def match(j, args, params, tags, tasklet):
    return True
