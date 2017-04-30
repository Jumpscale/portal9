from JumpScale.portal.macrolib.plantuml import run_plant_uml, GraphVizNotInstalled


def main(j, args, params, tags, tasklet):
    page = args.page

    space_name = args.doc.getSpaceName()
    try:
        img_name = run_plant_uml(space_name, args.cmdstr, output_path='.files/img/plantuml')
    except GraphVizNotInstalled:
        page.addMessage('<i class="alert alert-error">GraphViz is not installed</i>')
    else:
        page.addMessage('<img src="/$$space/.files/img/plantuml/{}">'.format(img_name))

    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True
