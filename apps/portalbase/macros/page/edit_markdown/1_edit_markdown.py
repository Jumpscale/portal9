
def main(j, args, params, tags, tasklet):

    import urllib.parse
    import urllib.request
    import urllib.parse
    import urllib.error
    # import urllib.request, urllib.error

    querystr = args.requestContext.env['QUERY_STRING']
    querytuples = urllib.parse.parse_qsl(querystr)
    for item in querytuples[:]:
        if item[0] in ['space', 'page']:
            querytuples.remove(item)
    spaceName = querystr.split('&')[0].split('=')[1]
    querystr = urllib.parse.urlencode(querytuples)
    page = args.page
    page.addCSS('/jslib/bootstrap/css/bootstrapmarkdown/bootstrap-markdown.min.css')
    page.addCSS(cssContent='''
        .md-editor.md-fullscreen-mode .md-input, .md-editor.md-fullscreen-mode .md-preview{
            font-size: 15px!important;
        }
        .form-btn{
            padding: 2px 40px !important;
            margin-right: 15px;
        }
    ''')

    page_name = ''
    import re
    page_match = re.search(r"page\s*:\s*([^:}]*)", args.macrostr)
    if page_match:
        page_name = page_match.group(1)

    args = args.tags.getValues(path="", page="", space="")
    space = j.portal.tools.server.active.getSpace(spaceName)
    doc = space.docprocessor.docGet(page_name)
    path = doc.path

    content = j.sal.fs.fileGetContents(path)
    content = content.replace("'", "\\'").replace('"', '\\"').replace("\n", "\\n").replace('{{', '\\\{\\\{')
    guid = j.base.idgenerator.generateGUID()
    contents = {'path': doc.path, 'querystr': '', 'page': page_name, 'space': spaceName}
    j.apps.system.contentmanager.dbmem.cacheSet(guid, contents, 60)
    page.addJS('/jslib/bootstrap/js/bootstrapmarkdown/bootstrap-markdown.js')
    page.addMessage('''
        <form name="editFileForm" method="post" action="/restmachine/system/contentmanager/wikisave?cachekey={guid}">
            <textarea id="markdownEditor" name="text" data-provide="markdown" cols='60' rows='8'></textarea>
            <div style="text-align: center; margin: 30px 0;">
                <input type="submit" class="btn btn-lg btn-primary form-btn" value="Save">
                <input type="submit" href="../{spaceName}/{pageName}" class="btn btn-lg form-btn" value="Cancel">
            </div>
        </form>
        <script>
            jQuery("#markdownEditor").val("{content}");
            jQuery("#markdownEditor").markdown({{hiddenButtons:'cmdPreview', autofocus:false, savable:false, height: 700}});
        </script>
    '''.format(content=content, guid=guid, pageName=page_name, spaceName=spaceName))
    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True
