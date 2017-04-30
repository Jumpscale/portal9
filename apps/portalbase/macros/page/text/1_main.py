from JumpScale.portal.macrolib import div_base


def main(j, args, params, *other_args):
    return div_base.macro(j, args, params, self_closing=True, tag='input',
                          additional_tag_params={'type': 'text'})


def match(j, args, params, tags, tasklet):
    return True
