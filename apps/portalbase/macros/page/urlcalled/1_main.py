
def main(j, args, params, tags, tasklet):

    params.merge(args)
    page = args.page
    e = args.requestContext.env

    addr = j.portal.tools.server.active.addr

    querystr = e["QUERY_STRING"]
    querystr = querystr.replace("&format=text", "")
    querystr = querystr.replace("&authkey=,", "")
    querystr = querystr.replace("&authkey=", "")
    querystr = querystr.replace("authkey=,", "")
    querystr = querystr.replace("authkey=", "")
    querystr += "authkey=???"  # TODO: fill in use authenticator

    if "machine" in args:
        url = "http://" + addr +\
            e["PATH_INFO"].strip("/") + "?" + querystr
        page.addLink(url, url)
    else:
        url = "http://" + addr + "/restmachine/" +\
            e["PATH_INFO"].replace("/rest/", "").strip("/") + "?" + querystr

        page.addLink(url, url)
        page.addMessage("Be carefull generated authkey above has been generated for you as administrator.")

    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True
