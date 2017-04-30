from JumpScale.portal.macrolib import div_base


def main(j, args, params, *other_args):
    return div_base.macro(j, args, params, tag='button',
                          additional_tag_params={'type': 'submit'})


def match(j, args, params, tags, tasklet):
    return True
