
def main(j, args, params, tags, tasklet):
    params.merge(args)

    doc = params.doc
    tags = params.tags

    docs = doc.preprocessor.findDocs(filterTagsLabels=tags)
    # In order to avoid recursive document inclusion, remove itself from selected docs
    docs = sorted(d for d in docs if d.name.lower() != doc.name.lower() and not d.name.endswith('docs'))
    if tags.tagExists("prefix"):
        prefix = tags.tagGet("prefix")
    else:
        prefix = ""

    for doc2 in docs:
        doc.children.append(doc2)
        doc2.preprocess()

    params.result = "", doc

    return params


def match(j, args, params, tags, tasklet):
    return True
