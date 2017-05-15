import os


def main(j, args, params, tags, tasklet):
    params.result = page = args.page

    keywords = args.expandParamsAsDict()
    search_space = keywords.get('space', args.doc.getSpaceName())
    space = j.portal.tools.server.active.spacesloader.spaces.get(search_space, None)
    if not space:
        page.addMessage('ERROR: space {} does not exist'.format(search_space))
        return params

    space_path = space.model.path
    search_term = keywords.get('search_term') or keywords.get('text') or ''

    if not search_term:
        return params

    result_files = []
    for root, _, files in os.walk(space_path):
        for f in files:
            if f.endswith('.wiki') and '.space' not in root and search_term.lower(
            ) in open(os.path.join(root, f)).read().lower():
                result_files.append(os.path.join(root, f))

    if result_files:
        page.addMessage('<dl><dt>Found in {} file(s)</dt><dd><ul class="col3">'.format(len(result_files)))

    for f in result_files:
        page_name = os.path.splitext(os.path.basename(f))[0]
        page.addMessage(
            '<li><a target="_blank" href="/{space}/{page}">{page}</a></li>'.format(space=search_space, page=page_name))

    page.addMessage('</ul></dd></dl>')

    page.addCSS(cssContent='''ul.col3 {
        -moz-column-count: 3;
        -webkit-column-count: 3;
    } ''')

    return params


def match(j, args, params, tags, tasklet):
    return True
