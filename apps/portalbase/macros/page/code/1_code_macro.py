
def main(j, args, params, tags, tasklet):
    page = args.page
    template = args.getTag('template', 'python')
    theme = args.getTag('theme', 'monokai')
    autorefresh = args.getTag('autorefresh', False)
    linenr = 'nolinenr' not in args.tags.labels
    wrap = 'nowrap' not in args.tags.labels
    page.addBootstrap()
    macrostr = args.macrostr.strip()
    content = "\n".join(macrostr.split("\n")[1:-1])
    content = content.replace("\{", "{")
    content = content.replace("\}", "}")

    page.addCodeBlock(content, edit=False, exitpage=True, spacename='', pagename='', linenr=linenr,
                      linecolor="#eee", linecolortopbottom="1px solid black", template=template, wrap=wrap, theme=theme, autorefresh=autorefresh)

    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True
