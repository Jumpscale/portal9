[actor] @dbtype:mem #tasklets
    method: prepareCatalog
        """
        Initializes the swagger entry point for listing the available APIs
        """
        result:dict

    method:getDocForActor
        """
        Gets the json doc of the given actor
        """
        var:actorname str,,name of the actor to get documentation for
        result:dict 