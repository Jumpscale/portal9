
def main(j, args, params, tags, tasklet):
    params.merge(args)

    doc = params.doc
    tags = params.tags

    id = 0

    def addNode(name, descr, id):
        C = """
subgraph cluster$id {
    node [style=filled,color=white];
    style=filled;
    color=lightgrey;
    label = "$descr";
$items
}
"""
        if descr == "":
            descr = name
        defmanager = j.portal.tools.defmanager.portaldefmanager
        name = defmanager.replaceDefWithProperName(name)
        C = C.replace("$descr", name)
        C = C.replace("$id", str(id))
        return C

    def addComponents(out, components):
        comps = ""
        for key in list(components.keys()):
            comps += "    %s;\n" % key
        out = out.replace("$items", comps)
        return out

    out = "size=\"7.5,10\";\n"
    out += "ratio=auto;\n"
    cmdstr = params.macrostr.split(":", 1)[1].replace("}}", "").strip()
    node = ""
    state = "start"
    connections = []
    components = {}
    componentsall = {}
    componentpernode = {}
    componentscounter = {}
    nodes = {}
    compsym = {}  # keeps track betweek compname & compid which can get auto nr
    for line in cmdstr.split("\n"):
        line = line.replace("  ", " ").replace("  ", " ")
        # print line
        # print state
        line = line.strip()
        if line == "" or line[0] == "#":
            continue

        if line.find("<-") != -1 or line.find("<->") != -1 or line.find("->") != -1:
            # connections
            connections.append(line)
            continue

        if state == "node" and line[0] != "-":
            state = "start"
            out = addComponents(out, components)
            components = {}

        # COMPONENT
        if state == "node" and line[0] == "-":
            line = line[1:].strip()
            # found component of node
            if line.find(" ") > 0:
                comp = line.strip().split(" ", 1)[0]
                compdescr = line.strip().split(" ", 1)[1]
            else:
                comp = line.strip().split(" ", 1)[0]
                compdescr = ""
            if comp in componentsall:
                componentscounter[comp] += 1
                comp2 = "%s_nr%s" % (comp, componentscounter[comp])
                if comp not in compsym:
                    compsym[comp] = []
                compsym[comp].append(comp2)
                comp = comp2

            else:
                componentscounter[comp] = 1
            components[comp] = compdescr
            componentsall[comp] = compdescr
            continue

        # NODE
        if state == "start" and line[0] != "-":

            if line.find(" ") > 0:
                node = line.strip().split(" ", 1)[0]
                nodedescr = line.strip().split(" ", 1)[1]
            else:
                node = line.strip().split(" ", 1)[0]
                nodedescr = ""
            nodes[node] = nodedescr
            state = "node"
            id += 1
            out += addNode(node, nodedescr, id)
            continue

    if state == "node":
        out = addComponents(out, components)

    # process connections
    for conn in connections:
        # print conn
        try:
            if conn.find("<->") != -1:
                ffrom, tto = conn.split("<->")
            elif conn.find("->") != -1:
                ffrom, tto = conn.split("->")
            elif conn.find("<-") != -1:
                tto, ffrom = conn.split("<-")
            tto = tto.strip()
            ffrom = ffrom.strip()
            out += "%s->%s [arrowsize=0];\n" % (ffrom, tto)
            if tto in compsym:
                for tto in compsym[tto]:
                    out += "%s->%s [arrowsize=0];\n" % (ffrom, tto)
            if ffrom in compsym:
                for ffrom in compsym[ffrom]:
                    out += "%s->%s [arrowsize=0];\n" % (ffrom, tto)

        except Exception as e:
            print(e)
            out = "ERROR: could not process, error %s, line trying to parse was %s" % (e, conn)

    defmanager = j.portal.tools.defmanager.portaldefmanager

    # set the descriptions
    for key in list(componentsall.keys()):
        descr = componentsall[key]
        if key.find("_nr") != -1:
            key2 = key.split("_nr")[0]
        else:
            key2 = key
        descr = defmanager.replaceDefWithProperName(key2)
        out += "%s [shape=box,label=\"%s\"];\n" % (key, descr)

    out = "{{graph:\ndigraph G {\n%s\n}\n}}\n\n" % out

    if len(list(nodes.keys())) > 0:
        out += 'h4. nodes\n'
        for key in list(nodes.keys()):
            descr = nodes[key]
            link = defmanager.getLink(key)
            if link is None:
                link = key
            if descr != "":
                out += '* %s:%s\n' % (link, descr)
            else:
                out += '* %s\n' % link

    if len(list(componentsall.keys())) > 0:
        out += 'h4. components\n'
        for key in list(componentsall.keys()):
            if key.find("_nr") != -1:
                continue
            descr = componentsall[key]
            link = defmanager.getLink(key)
            if link is None:
                link = key
            if descr != "":
                out += '* %s:%s\n' % (link, descr)
            else:
                out += '* %s\n' % link

    params.result = (out, doc)

    return params


def match(j, args, params, tags, tasklet):
    return True
