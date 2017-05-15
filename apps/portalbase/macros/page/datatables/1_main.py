
def main(j, args, params, tags, tasklet):

    page = args.page

    modifier = j.portal.tools.html.portalhtmlfactory.getPageModifierGridDataTables(page)
    namespace = args.getTag('namespace')
    category = args.getTag('category')
    url = args.getTag('url')
    fieldnames = args.getTag('fieldnames', '').split(',')
    fieldids = args.getTag('fieldids', '').split(',')

    if url:
        page = modifier.addTableFromURL(url, fieldnames)
    else:
        page = modifier.addTableForModel(namespace, category, fieldnames, fieldids)

    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True
