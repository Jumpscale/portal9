def main(j, args, params, tags, tasklet):
    params.merge(args)

    doc = params.doc
    tags = params.tags

    docs = doc.preprocessor.findDocs(filterTagsLabels=tags)
    docs = [d for d in docs if d.name.lower() != doc.name.lower() and 'docs' not in d.name.lower()]

    out = ""
    for child_doc in docs:
        out += "* [%s]\n" % child_doc.pagename

    params.result = (out, doc)

    out = ""
    for tagdoc in docs:
        tagdoc.preprocess()
        out += "* [%s]\n" % tagdoc.pagename
    params.result = (out, doc)

    return params


def match(j, args, params, tags, tasklet):
    return True
