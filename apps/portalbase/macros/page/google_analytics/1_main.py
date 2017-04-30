def main(j, args, params, tags, tasklet):
    params.result = page = args.page

    google_analytics_id = args.cmdstr or args.doc.docparams.get('google_analytics_id', None)
    if not google_analytics_id:
        return params

    js_content = '''
      var _gaq = _gaq || [];
      _gaq.push(['_setAccount', '{google_analytics_id}']);
      _gaq.push(['_trackPageview']);

      (function() {{
        var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
        ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
        var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
      }})();
    '''.format(google_analytics_id=google_analytics_id)

    if js_content not in page.head:
        page.addJS(jsContent=js_content)

    return params


def match(j, args, params, tags, tasklet):
    return True
