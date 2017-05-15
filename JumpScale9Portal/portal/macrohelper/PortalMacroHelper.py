
from js9 import j


class PortalMacroHelper():

    def push2doc(self, args, params, objFetchManipulate):
        params.merge(args)
        doc = params.doc

        idd = args.getTag("id")
        if not idd:
            params.result = ('Missing id param "id"', doc)
            return params

        obj = objFetchManipulate(idd)

        if args.tags.labelExists("show"):
            out = ""
            keys = sorted(obj.keys())
            for key in keys:
                value = obj[key]
                r = 0
                for item in str(value).split("\n"):
                    if r == 0:
                        out += "- %-20s : %s\n" % (key, item)
                    else:
                        out += "- %-20s   %s\n" % (" ", item)
                    r += 1
            params.result = ("{{code:\n%s\n}}" % out, doc)
            return params

        objparams = {str(k).lower(): v for k, v in list(obj.items())}

        # apply the properties of the object as parameters to the active wiki document
        doc.content = doc.applyParams(objparams, content=doc.content)

        # IMPORTANT return 2x doc (not (out,doc)) but return (doc,doc) this tells
        # the appserver that the doc was manipulated
        params.result = (doc, doc)
        return params
