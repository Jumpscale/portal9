import re
import urllib.request
import urllib.parse
import urllib.error


def main(j, args, params, tags, tasklet):
    page = args.page
    doc = args.doc
    page.addCSS('/jslib/old/breadcrumbs/breadcrumbs.css')

    data = "<ul class='breadcrumb'>%s</ul>"
    breadcrumbs = []
    space = j.portal.tools.server.active.getSpace(doc.getSpaceName())
    if 'breadcrumbdata' in args.requestContext.params:
        for breadcrumb in args.requestContext.params['breadcrumbdata'][::-1]:
            for name, link in breadcrumb.items():
                breadcrumbs.insert(0, (link, name, {}))
    else:
        title_replace = j.data.regex.findOne('\$\$.*', doc.title).strip('$$')
        title_replace = args.requestContext.params.get(title_replace)
        doc.title = j.data.regex.replace('.*\$\$.*', '\$\$.*', title_replace, doc.title)
        breadcrumbs.append((doc.original_name, doc.title, {}))
        while doc.parent:
            doc = space.docprocessor.name2doc.get(doc.parent)
            if not doc:
                break
            args = {}
            for arg in doc.requiredargs:
                if arg in doc.appliedparams:
                    args[arg] = doc.appliedparams[arg]
            breadcrumbs.insert(0, (doc.original_name, doc.title, args))

    innerdata = ""
    breadcrumbs.insert(0, ('/%s' % space.model.id, space.model.name, {}))
    for link, title, args in breadcrumbs[:-1]:
        if args:
            link = "%s?%s" % (link, urllib.parse.urlencode(args))
        innerdata += "<li><a href='%s'>%s</a><span style='opacity: 0.5; margin-right: 8px; margin-left: 2px;' class='icon-chevron-right'></span></li>" % (
            link, title)
    innerdata += "<li class='active'>%s</li>" % breadcrumbs[-1][1]

    page.addMessage(data % innerdata)
    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True
