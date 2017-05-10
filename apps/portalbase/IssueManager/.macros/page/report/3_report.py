
def main(j, args, params, tags, tasklet):
    import yaml
    page = args.page

    macrostr = args.macrostr.strip()
    content = "\n".join(macrostr.split("\n")[1:-1])
    try:
        data_collection = yaml.load(content)
    except yaml.error.YAMLError:
        page.addMessage('<h3> **ERROR : Incorrect YAML format , please adjust. </h3>')
        params.result = page
        return params

    if not data_collection:
        page.addMessage("Nothing to show with applied filters")
        params.result = page
        return params


    panels = list()
    for data, info in data_collection.items():
        panel_data = {'title': data}
        content = ""
        tables = []
        for state, issues in info.items():
            if info[state]:
                if state in ['closed', 'resolved', 'wontfix']:
                    state = "<red style='color:red'> {} </red>".format(state)
                elif state in 'new':
                    state = "<green style='color:green'> new </green>"
                else:
                    state = "<blue style='color:blue'> {} </blue>".format(state)


                content += "<h5> <li> {} </li> </h3>".format(state)
                content += "<table>"
                for issue in issues:
                    if issue['priority'] in ['critical']:
                        priority = "<critical style='color:#9e0e23'> CRITICAL </critical>"
                    elif issue['priority'] in ['major']:
                        priority = "<major style='color:#d87987'> MAJOR </major>"
                    elif issue['priority'] in ['normal']:
                        priority = "<normal style='color:#3085ad'> NORMAL </normal>"
                    else:
                        priority = "<prio style='color:#8b8f91'> {} </prio>".format(issue['priority'].upper())
                    content += '<tr><td>' + issue['repo']
                    content += '</td><td><a href="{}" target="_blank">{}</a></td>'.format(issue['gitHostRefs'][0]['url'], issue['title'])
                    content += '<td> %s </td><td>' % j.data.time.epoch2HRDateTime(issue['creationTime'])
                    content += priority + '</td></tr>'
                content += "</table>"
        panel_data['label_content'] = '#new:{} #resolved:{} #closed:{} #wontfix:{} #inprogress:{} #question:{}'.format(len(info['new']), len(info['resolved']), len(info['closed']), len(info['wontfix']), len(info['inprogress']), len(info['question']))
        panel_data['content'] = content
        panels.append(panel_data)

    page.addAccordion(panels)


    page.addCSS(cssContent="""table {
        width: 100%;
    }
    th, td {
        border: 1px solid black;
        padding: 8px;
    }
    th {
        background-color: #5d88b3;
        }
        td {
        /*min-width: 100px;*/
        max-width:170px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    }}
    """)
    params.result = page

    return params
