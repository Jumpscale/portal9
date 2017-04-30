from JumpScale.portal.macrolib import div_base


def main(j, args, params, *other_args):
    params.result = page = args.page
    page.addMessage('''<a href='#' onclick="$(this).parents('form')[0].reset(); return false;">Reset</a>''')
    return params


def match(j, args, params, tags, tasklet):
    return True
