
def main(j, args, params, tags, tasklet):
    def chunks(l, n):
        """ Yield successive n-sized chunks from l.
        """
        for i in range(0, len(l), n):
            yield l[i:i + n]

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
<a href="#" class="dropdown-toggle pull-right {klass}" data-toggle="dropdown">{name}<b class="caret"></b></a>
<ul class="dropdown-menu mega-menu" style="min-width: {widthsize}px;">
{items}
</ul>
</li>
"""

    items = ""
    header = args.tags.tagGet("name", "Admin")
    klass = args.tags.tagGet("class", "")

    contents = j.data.hrd.get(content=args.cmdstr + '\n')
    columns = contents.getDictFromPrefix('column')

    amountcolumns = 0

    for title, rows in columns.items():
        if not isinstance(rows, dict):
            continue
        chunkedrows = list(chunks(list(rows.items()), 12))
        amountcolumns += len(chunkedrows)
        for idx, tenrow in enumerate(chunkedrows):
            items += '<li class="mega-menu-column" style="width: {colpercent}%; float: left; padding-left: 10px;">'
            if idx == 0:
                items += '<ul>'
                items += '<li class="dropdown-header">%s</li>' % title
            else:
                items += '<ul style="padding-top: 34px;">'
            for name, target in tenrow:
                external = ""
                if target.endswith(':external'):
                    external = "target=\"_blank\""
                    target = target.rstrip(':external')
                if name != "" and name[0] != "#":
                    name = name.strip()
                    line = "<li><a href=\"%s\" %s>%s</a></li>" % (target, external, name)
                    items += "%s\n" % line
            items += '</ul></li>'

    colpercent = 100 / (amountcolumns or 1)
    items = items.format(colpercent=colpercent)
    ddcode = ddcode.format(items=items, name=header, klass=klass, widthsize=180 * amountcolumns)
    ddcode += '$$$menuright'

    page.body = page.body.replace(keyword, ddcode)

    return params


def match(j, args, params, tags, tasklet):
    return True
