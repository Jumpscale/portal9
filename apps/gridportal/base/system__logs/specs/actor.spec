#obsolete is now in https://bitbucket.org/jumpscale/jumpscale_grid/src/tip/apps/gridportal/base/system__gridmanager/specs/actor.spec

[actor] @dbtype:mem #tasklets
    method: listJobs
        """
        Gets jobs that match criteria
        """
        var:ffrom str,,format -4h, -3d, etc @tags: optional
        var:to str,,format -4h, -3d, etc @tags: optional
        var:nid int,, @tags: optional
        var:gid int,, @tags: optional
        var:parent str,, @tags: optional
        var:state str,, @tags: optional
        var:jsorganization str,, @tags: optional
        var:jsname str,, @tags: optional
        var:nip str,, @tags: optional
        var:roles str,, @tags: optional
        result:dict


    method: listNodes
        """
        Gets nodes for grid
        """
        result:dict


    method: listECOs
        """
        Gets ECOs for node
        """
        var:nid int,, @tags: optional
        result:dict

    method: listLogs
        """
        Gets logs (for node)
        """
        var:nid int,, @tags: optional
        result:dict
