def main(j, args, params, tags, tasklet):

    params.merge(args)
    doc = params.doc
    # tags = params.tags
    cachekey = args.getTag('cache')

    db = j.servers.kvs.getMemoryStore('cache')
    try:
        obj = db.cacheGet(cachekey)
    except:
        out = "Cache not found did you add \{\{testrun_getdata}} on your page?"
        params.result = (out, doc)
        return params

    out = """{{jscript

$( function () {
    $(".testruncontainer").hide();
    $('h4').click(function() { $(this).next(".testruncontainer").toggle("fast") });
});
}}
"""
    if obj['output']:
        for testname, output in obj['output'].items():
            teststate = obj['teststates'].get(testname, 'UNKNOWN')
            out += "h4. [Test: %s %s|#]\n" % (testname, teststate)
            out += "{{div: class=testruncontainer}}\n"
            out += "h5. Source\n"
            out += "{{code\n%s\n}}\n" % obj['source'].get(testname, '')
            if teststate == 'OK':
                out += "h5. Result\n"
                out += "{{code\n%s\n}}\n" % obj['result'].get(testname, '')
            elif testname in obj['result']:
                out += "h5. ECO\n"
                out += "{{grid.eco id:%s}}\n" % obj['result'][testname]

            out += "h5. Output\n"
            out += "{{code\n%s\n}}\n" % output
            out += "{{div}}\n"

    params.result = (out, doc)

    return params


def match(j, args, params, tags, tasklet):
    return True
