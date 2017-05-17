
def main(j, args, params, tags, tasklet):
    params.result = args.page
    tags = args.tags
    disable_filters = tags.tagExists('disable_filters') and tags.tagGet('disable_filters').lower() == 'true'
    autosort = tags.tagExists('autosort') and tags.tagGet('autosort').lower() == 'true'
    displaylength = tags.tagExists('displaylength') and tags.tagGet('displaylength')
    if displaylength:
        displaylength = int(displaylength)

    modifier = j.portal.tools.html.htmlfactory.getPageModifierGridDataTables(args.page)
    modifier.prepare4DataTables(autosort, displaylength)
    if not disable_filters:
        modifier.addSearchOptions()

    return params


def match(j, args, params, tags, tasklet):
    return True
