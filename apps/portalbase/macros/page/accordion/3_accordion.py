def main(j, args, params, tags, tasklet):
    page = args.page

    macrostr = args.macrostr.strip()
    content = "\n".join(macrostr.split("\n")[1:-1])

    panels = j.data.serializer.yaml.loads(content)

    if not isinstance(panels, list):
        panels = [panels]

    page.addJS('/jslib/codemirror/autorefresh.js', header=False)
    page.addMessage('<div class="panel-group" id="accordion" role="tablist" aria-multiselectable="true">')

    for panel_data in panels:
        # hack to be able to pass yaml into the macro
        # the content is json serializer passed to the macro then deserialize here
        if panel_data is None:
            continue
        try:
            panel_data['content'] = j.data.serializer.json.loads(panel_data['content'])
        except:
            pass

        for item in ['header_id', 'section_id', 'label_id']:
            if item not in panel_data:
                panel_data[item] = j.data.idgenerator.generateXCharID(10)

        page.addMessage("""
        <div class="panel panel-default">
          <div class="panel-heading" role="tab" id="%(header_id)s">
            <h4 class="panel-title">
              <a data-toggle="collapse" data-parent="#accordion" href="#%(section_id)s" aria-expanded="true" aria-controls="%(section_id)s">%(title)s</a>
        """ % panel_data)

        if 'label_content' in panel_data:
            page.addMessage("""
            <a id=%(label_id)s class="label-archive label label-%(label_color)s glyphicon glyphicon glyphicon-%(label_icon)s pull-right">%(label_content)s</a>
            """ % panel_data)

        page.addMessage("""
            </h4>
          </div>
          <div id="%(section_id)s" class="panel-collapse collapse" role="tabpanel" aria-labelledby="%(header_id)s">
            <div class="panel-body">
            """ % panel_data)

        if panel_data.get('code', False):
            page.addCodeBlock(panel_data['content'], edit=False, exitpage=True, spacename='', pagename='', linenr=True, autorefresh=True)
        else:
            page.addMessage(panel_data['content'])

        page.addMessage("""
            </div> <!-- panel body-->
          </div> <!-- panel collapse-->
        </div> <!-- panel default-->""")

    page.addMessage('</div>')  # close panel-group
    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True
