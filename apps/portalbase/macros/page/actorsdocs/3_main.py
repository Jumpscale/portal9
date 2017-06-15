def main(j, args, params, tags, tasklet):
    page = args.page
    actors = args.tags.tagGet('actors', '')
    group = args.tags.tagGet('group', '')

    page.addCSS('/jslib/swagger/css/typography.css', media='screen')
    page.addCSS('/jslib/swagger/css/reset.css', media='screen')
    page.addCSS('/jslib/swagger/css/screen.css', media='screen')

    page.addCSS('/jslib/swagger/css/typography.css', media='print')
    page.addCSS('/jslib/swagger/css/reset.css', media='print')
    page.addCSS('/jslib/swagger/css/screen.css', media='print')

    page.addJS('/jslib/swagger/lib/jsoneditor.min.js')
    page.addJS('/jslib/swagger/lib/swagger-oauth.js')
    page.addJS('/jslib/swagger/lib/jquery-1.8.0.min.js')
    page.addJS('/jslib/swagger/lib/jquery.slideto.min.js')
    page.addJS('/jslib/swagger/lib/jquery.wiggle.min.js')
    page.addJS('/jslib/swagger/lib/jquery.ba-bbq.min.js')
    page.addJS('/jslib/swagger/lib/handlebars-2.0.0.js')
    page.addJS('/jslib/swagger/lib//lodash.min.js')
    page.addJS('/jslib/swagger/lib/backbone-min.js')
    page.addJS('/jslib/swagger/swagger-ui.min.js')
    page.addJS('/jslib/swagger/lib/highlight.9.1.0.pack.js')
    page.addJS('/jslib/swagger/lib/highlight.9.1.0.pack_extended.js')
    page.addJS('/jslib/swagger/lib/marked.js')
    page.addJS('/jslib/swagger/lib/object-assign-pollyfill.js')
    page.addJS('/jslib/swagger/lib/js-yaml.min.js')

    head = """
    <title>Swagger UI</title>
    <script type="text/javascript">
    $(function () {
        window.swaggerUi = new SwaggerUi({
                url:"/restmachine/system/docgenerator/prepareCatalog?actors=%s&group=%s&format=jsonraw",
                validatorUrl: null,
                dom_id:"swagger-ui-container",
                supportHeaderParams: false,
                supportedSubmitMethods: ['get', 'post', 'put'],
                onComplete: function(swaggerApi, swaggerUi){
                    if(console) {
                        console.log("Loaded SwaggerUI")
                        console.log(swaggerApi);
                        console.log(swaggerUi);
                    }
                  $('pre code').each(function(i, e) {hljs.highlightBlock(e)});
                },
                onFailure: function(data) {
                    if(console) {
                        console.log("Unable to Load SwaggerUI");
                        console.log(data);
                    }
                },
                docExpansion: "none",
                sorter : "alpha",
                apisSorter : "alpha",
                operationsSorter: "alpha"
            });

            window.swaggerUi.load();
        });

    </script>
    """ % (j.portal.tools.html.htmlfactory.escape(actors), j.portal.tools.html.htmlfactory.escape(group))

    body = """
    <div class="swagger-section">
    <div id="message-bar" class="swagger-ui-wrap">
        &nbsp;
    </div>

    <div id="swagger-ui-container" class="swagger-ui-wrap">

    </div>
    </div>
    """

    page.addHTMLHeader(head)
    page.addHTMLBody(body)

    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True
