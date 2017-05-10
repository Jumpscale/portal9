
def main(j, args, params, tags, tasklet):
    doc = args.doc
    out = "{{kanban: \n"
    yaml = []
    constants = {}
    dynamics = {}

    macrostr = args.macrostr.strip().strip('{{').strip('}}')
    tags = j.data.tags.getObject(macrostr, keepcase=True)
    tags = tags.getDict()

    if 'assignees' in tags and tags['assignees'] == '$$assignees':
        tags.pop('assignees')

    datatype = tags.pop('kanbandata').strip()
    if datatype == 'issue' or not datatype:
        collection = j.tools.issuemanager.getIssueCollectionFromDB()
    if datatype == 'user':
        collection = j.tools.issuemanager.getUserCollectionFromDB()
    if datatype == 'org' or datatype == 'organization':
        collection = j.tools.issuemanager.getOrgCollectionFromDB()
    if datatype == 'repo' or datatype == 'repository':
        collection = j.tools.issuemanager.getRepoCollectionFromDB()

    user_collection = j.tools.issuemanager.getUserCollectionFromDB()
    repo_collection = j.tools.issuemanager.getRepoCollectionFromDB()

    def emptyInYaml(results, yaml):
        for result in results:
            result = result.dictFiltered
            title_link = '<a href="'+ result['gitHostRefs'][0]['url'] + '" target="_blank">' + result["title"] + '</a>'
            # body = result.get('content', '')
            body = result.get('content', "").replace('{', '').replace('}', '')
            data = {'title': title_link,
                    'content': body,
                    'key': result['key'],
                    'state': 'done' if result['isClosed'] else 'new'}
            data['assignees'] = result['assignees'] if result['assignees'] else [0]
            data['state'] = result['state']
            if data['state'] in ['resolved', 'wontfix']:
                data['state'] = 'closed'
            result['labels'] = result.get('labels', [])
            data['priority'] = result['priority']
            data['tags'] = ",".join(result['labels'])
            yaml += [data]

    if datatype in ['issue']:
        if 'assignees' in tags:
            userid = user_collection.find(name=tags['assignees'])
            if userid:
                userid = userid[0].key
                tags['assignees'] = userid

    for tag, val in tags.items():
        if isinstance(val, bool):
            instances = [val]
        else:
            if ',' not in val:
                constants[tag] = val
                continue
            instances = val.split(',')
        for instance in instances:
            dynamics[tag] = instance
            results = collection.find(**dynamics, **constants)
            emptyInYaml(results, yaml)

    if not dynamics:
        results = collection.find(**dynamics, **constants)
        emptyInYaml(results, yaml)

    out += j.data.serializer.yaml.dumps(yaml) + "\n}}"
    params.result = (out, doc)

    return params


def match(j, args, params, tags, tasklet):
    return True
