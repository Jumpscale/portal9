
def main(j, args, params, tags, tasklet):
    params.merge(args)

    doc = params.doc
    tags = params.tags

    out = ""
    cmdstr = params.macrostr.split(":", 1)[1].replace("}}", "").strip()
    md5 = j.data.hash.md5_string(cmdstr)
    j.sal.fs.createDir(j.sal.fs.joinPaths(j.portal.tools.server.active.filesroot, "dot"))
    path = j.sal.fs.joinPaths(j.portal.tools.server.active.filesroot, "dot", md5)
    if not j.sal.fs.exists(path + ".png"):
        j.sal.fs.writeFile(path + ".dot", cmdstr)
        cmd = "dot -Tpng %s.dot -o %s.png" % (path, path)

        # for i in range(5):
        rescode, result = j.system.process.execute(cmd)
        # if result.find("warning")==011:

        if result.find("warning") != -1:
            out = result
            out += '\n'
            out += "##DOT FILE WAS##:\n"
            out += cmdstr
            out += "##END OF DOT FILE##\n"
            out = "{{code:\n%s\n}}" % out

            params.result = out

            return params

    out = "!/files/dot/%s.png!" % md5

    params.result = (out, doc)

    return params


def match(j, args, params, tags, tasklet):
    return True
