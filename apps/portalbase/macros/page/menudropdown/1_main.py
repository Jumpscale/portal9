
def main(j, args, params, tags, tasklet):
    page = args.page
    params.result = page

    if not page._hasmenu:
        page.addMessage(
            "**error: Cannot create page because menudropdown macro can only be used if beforehand a menu macro was used")
        return params

    keyword = args.tags.tagGet('marker', "$$$menuright")

    # todo what does this do? (4kds)
    if page.body.find(keyword) == -1:
        return params

    ddcode = """
<li class="dropdown">
  <a href="#" class="dropdown-toggle pull-right $$class" data-toggle="dropdown">$$name<b class="caret"></b></a>
  <ul class="dropdown-menu">
       $$items
  </ul>
</li>
"""

    # <li><a href="#">Action</a></li>
    # <li><a href="#">Another action</a></li>
    # <li><a href="#">Something else here</a></li>
    #<li class="divider"></li>
    #<li class="nav-header">Nav header</li>
    # <li><a href="#">Separated link</a></li>
    # <li><a href="#">One more separated link</a></li>

    items = ""
    name = args.tags.tagGet("name", "Admin")
    klass = args.tags.tagGet("class", "")
    for line in args.cmdstr.split("\n"):
        line = line.strip()
        if line != "" and line[0] != "#":
            # print line
            if line.find("name:") != -1:
                devnull, name = line.split(":", 1)
                name = name.strip()
            elif line.find("---") != -1:
                items += "<li class=\"divider\"></li>\n"
            else:
                name2, target = line.split(":", 1)
                line2 = "<li><a href=\"%s\">%s</a></li>" % (target, name2)
                items += "%s\n" % line2

    ddcode = ddcode.replace("$$items", items)
    ddcode = ddcode.replace("$$name", name)
    ddcode = ddcode.replace("$$class", klass)
    ddcode += '$$$menuright'

    page.body = page.body.replace(keyword, ddcode)

    return params


def match(j, args, params, tags, tasklet):
    return True
