
def main(j, args, params, tags, tasklet):
    params.result = page = args.page
    page.addJS(jsLink='/jslib/old/numberedheadings/numberedheadings.js')
    js_content = '$(function(){$().numberedHeadings()});'
    if js_content not in page.head:
        page.addJS(jsContent=js_content)
    return params


def match(j, args, params, tags, tasklet):
    return True
