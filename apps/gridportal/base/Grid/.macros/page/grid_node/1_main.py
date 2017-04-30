def main(j, args, params, tags, tasklet):

    page = args.page
    page.addHTML('<br><br><br><br><br>')

    qsparams = args.requestContext.params
    nip = qsparams.pop('nip', None)
    nid = qsparams.pop('nid', None)

    if nip:
        print(nip)

    page.addHeading('Node ECOs', 3)
    modifier = j.portal.tools.html.getPageModifierGridDataTables(page)
    url = '/restmachine/system/logs/listECOs?nid=%s' % nid

    fieldnames = ('appname', 'category', 'epoch', 'errormessage', 'jid', 'level', 'backtrace', 'nid', 'pid')
    page = modifier.addTableFromURL(url, fieldnames)

    page.addHTML('<br><br><br><br><br>')

    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True
