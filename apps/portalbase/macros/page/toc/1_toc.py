import random


def main(j, args, params, *other_args):
    page = params.result = args.page
    try:
        macro_params = dict([p.strip() for p in param_pair.split('=')] for param_pair in args.cmdstr.split('|'))
    except:
        macro_params = {}
    id = 'toc_' + str(random.randint(0, 9999))
    page.addJS(jsLink='/jslib/old/tableofcontents/jquery.tableofcontents.min.js')
    page.addJS(jsContent='''
                        $(document).ready(function(){{
                          $("#{0}").tableOfContents(
                            $("#{0}").parent(),
                            {{
                              startLevel:           {1},
                              depth:                {2}
                            }}
                          );
                        }});'''.format(id, macro_params.get('start', 1), macro_params.get('depth', 6)))

    page.addMessage('<ul id="{0}"></ul>'.format(id))

    return params


def match(j, args, params, tags, tasklet):
    return True
