

def main(j, args, params, tags, tasklet):
    def alphabetical(bp):
        return bp.name

    ayspath = args.getTag('ayspath')
    repo = j.core.atyourservice.repoGet(ayspath)
    bps = list()
    repo._load_blueprints()
    blueprints = repo.blueprints + repo.blueprintsDisabled

    blueprints = sorted(blueprints, key=alphabetical)
    for blueprint in blueprints:
        bp = dict()
        if not blueprint.active:
            label_color = 'warning'
            label_content = 'archived'
            icon = 'saved'

        elif not blueprint.is_valid:
            label_color = 'danger'
            label_content = 'error'
            icon = 'remove'

        else:
            label_color = 'success'
            label_content = 'active'
            icon = 'ok'

        bp['title'] = blueprint.name
        bp['label_content'] = label_content
        bp['icon'] = icon
        bp['label_color'] = label_color
        bp['content'] = j.data.serializer.json.dumps(blueprint.content)
        bps.append({blueprint.name: bp})

    args.doc.applyTemplate({'data': bps, 'reponame': repo.name})

#     result.append("""
# {{html:
# <script src='/jslib/codemirror/autorefresh.js'></script>
# }}
# {{jscript
#   $(function() {
#       $('.label').click(function() {
#         var that = this
#         var ss = this.id.split('-')
#         var repo = ss.shift()
#         var bp = ss.join('-')
#         if (this.innerText == 'enable'){
#             var url = '/restmachine/ays81/atyourservice/archiveBlueprint';
#         }else{
#             var url = '/restmachine/ays81/atyourservice/restoreBlueprint';
#         }
#         $.ajax({
#           type: 'GET',
#           data: 'repository='+repo+'&blueprint='+bp,
#           success: function(result,status,xhr) {
#             // restore
#             if (that.innerText == 'archived'){
#                 that.classList.remove('glyphicon-saved');
#                 that.classList.remove('label-warning');
#                 that.classList.add('glyphicon-ok');
#                 that.classList.add('label-sucess');
#                 that.innerText = 'enable'
#             }else{ // archive
#                 that.classList.remove('glyphicon-ok');
#                 that.classList.remove('label-sucess');
#                 that.classList.add('label-warning');
#                 that.classList.add('glyphicon-saved');
#                 that.innerText = 'archived'
#             }
#           },
#           error: function(xhr,status,error){ alert('error:'+ error) },
#           url: url,
#           cache:false
#         });
#       });
#     });
# }}
# {{cssstyle
# a.label-archive{
#     color: white;
# }
# }}""")
    # result = '\n'.join(result)

    params.result = (args.doc, args.doc)
    return params
