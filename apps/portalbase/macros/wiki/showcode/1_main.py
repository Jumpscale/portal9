
def main(j, args, params, tags, tasklet):
    params.merge(args)

    codepaths = dict()

    actors = j.portal.tools.server.active.actorsloader.actors
    for actorname, info in actors.items():
        if j.sal.fs.exists(info.model.path):
            parent = j.sal.fs.getParent(info.model.path)
            parent = parent.replace(j.dirs.JSBASEDIR, '$JSBASEDIR')
            codepaths[parent] = '%s Actors' % j.sal.fs.getBaseName(parent).capitalize()

    codepaths[j.sal.fs.joinPaths('$JSBASEDIR', 'apps', 'osis', 'logic')] = 'Models'

    codepaths[j.sal.fs.joinPaths('$jumpscriptsdir', 'jumpscripts')] = 'JumpScripts'

    result = list()
    result.append('''{{html: <div class="panel-group" id="accordion" role="tablist" aria-multiselectable="true">}}''')
    for path, title in codepaths.items():
        sectionid = 'collapse_%s' % title.replace(' ', '_')
        headingid = 'heading_%s' % title
        result.append("""{{html:
            <div class="panel panel-default">
<div class="panel-heading" role="tab" id="%s">
  <h4 class="panel-title">
            """ % headingid)
        result.append(
            '<a data-toggle="collapse" data-parent="#accordion" href="#%s" aria-expanded="false" aria-controls="%s">}}' %
            (sectionid, sectionid))

        result.append(title)
        result.append("""{{html
            </a>
  </h4>
</div>
<div id="%s" class="panel-collapse collapse" role="tabpanel" aria-labelledby="%s">
  <div class="panel-body"> }}
            """ % (sectionid, headingid))

        result.append('{{explorer: ppath:%s}}' % path)
        result.append("""{{html
            </div></div></div>}}""")

    result.append("""{{html
        </div>
        }}""")
    result = '\n'.join(result)
    # result = 'test'
    print(result)

    params.result = (result, params.doc)
    return params


def match(j, args, params, tags, tasklet):
    return True
