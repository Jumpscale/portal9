def main(j, args, params, tags, tasklet):

    page = args.page
    pars = args.expandParamsAsDict()
    hostname = pars.get('hostname', '')
    contentpage = pars.get('contentpage', '')
    divid = pars.get('divid', '')
    j.portal.tools.docgenerator.portaldocgeneratorfactory.getConfluence2htmlConvertor()

    scriptcontent = """
        (typeof(tocheck) == "undefined")? tocheck = [] : tocheck=tocheck;
        tocheck.push({"hostname":"%s", "divid":"%s"});""" % (hostname, divid)

    page.addJS(jsContent=scriptcontent)
    space = j.portal.tools.server.active.spacesloader.spaces[args.doc.getSpaceName()]
    if space.docprocessor.docExists(contentpage):
        doc = space.docprocessor.docGet(contentpage)
        htmlcontent = doc.getHtmlBody()
    else:
        htmlcontent = ""
    pagecontent = """<div id="%s" style="visibility:hidden; display:none;">%s</div>""" % (divid, htmlcontent)
    page.addMessage(pagecontent)
    page.addHostBasedContent()
    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True
