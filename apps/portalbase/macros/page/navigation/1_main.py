
def main(j, args, params, tags, tasklet):

    page = args.page
    if "." in args.doc.name:
        if args.doc.name.split('.')[1] != "md":
            page.addBootstrap()
    else:
        page.addBootstrap()

    navStr = args.cmdstr

    page._hasSidebar = True
    if "." in args.doc.name:
        if args.doc.name.split('.')[1] == "md":
            menuStr = "<div style='list-style-type: none;'>"
    else:
        menuStr = "<button class='c-hamburger c-hamburger--htla' title='Topics'><span>toggle hamburger</span></button><div class='well sidebar-nav hide'>"

    if args.doc.navigation != "":
        if navStr.strip() == "":
            navStr = args.doc.navigation + "\n"
        if navStr.strip() != "" and navStr[-1] != "\n":
            navStr += "\n"
            navStr += args.doc.navigation
        if navStr[-1] != "\n":
            navStr += "\n"

    def clean(txt):
        lines = txt.split("\n")
        lines = [item.strip() for item in lines if item.strip() != ""]
        if lines[0] == "<p></p>":
            lines.pop(0)
        if lines[0] == "<ul>":
            lines.pop(0)
        if lines[-1] == "</ul>":
            lines.pop()
        return "\n".join(lines)

    items = ""
    # out=""
    for line in navStr.split("\n"):
        line = line.strip()

        if line == "" or line[0] == "#":
            continue

        if line != "":
            if line.find("include:") == 0:
                name = line.replace("include:", "").strip()
                doc = args.doc.preprocessor.docGet(name)
                line, doc2 = doc.executeMacrosDynamicWiki()
                html = clean(doc.getHtmlBody())
                menuStr += html
            if line.find("{{") == 0:
                try:
                    line, doc2 = args.doc.preprocessor.macroexecutorWiki.execMacrosOnContent(content=line, doc=args.doc)
                    line = line.replace('.md', '')
                except Exception:
                    import traceback
                    traceback.print_exc()
                    raise RuntimeError(
                        "**ERROR: error executing macros for line:%s and for doc:%s, this happens inside navigation macro." % (line, args.doc.name))

                convertor = j.portal.tools.docgenerator.portaldocgeneratorfactory.getConfluence2htmlConvertor()
                convertor.convert(line, args.page, args.doc)
            # out+=line+"\n"
            else:
                if len(line.split(":")) > 2:
                    name, target, icon = line.split(":", 2)
                elif len(line.split(":")) > 1:
                    name, target = line.split(":", 1)
                    icon = ""
                else:
                    name = line
                    target = ""
                    icon = ""
                if target.strip().split('/')[-1].lower() == args.doc.name:
                    line2 = "<li class='nav-page-active'><a href=\"%s\"><i class=\"%s\"></i>%s</a></li>" % (
                        target.strip(), icon.strip(), name.strip())
                else:
                    line2 = "<li><a href=\"%s\"><i class=\"%s\"></i>%s</a></li>" % (
                        target.strip(), icon.strip(), name.strip())

                items += "%s\n" % line2

    menuStr += items
    menuStr += "</div>"

    # Add the sidebar only when there are items to show
    if items:
        page.addMessage(menuStr)

    params.result = page

    return params


def match(j, args, params, tags, tasklet):
    return True
