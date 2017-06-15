[actor] @dbtype:mem #tasklets
    """
    this actor manages all content on the wiki
    can e.g. notify wiki/appserver of updates of content
    """

    method:notifyFiledir @method:get,post
        """
         """
        var:path str,,path of content which got changed
        result:bool

    method:getSpaces @method:get,post
        """
        """
        result:list(str)

    method:getSpacesWithPaths @method:get,post
        """
        """
        result:list([name,path])

    method:getContentDirsWithPaths @method:get,post
        """
        return root dirs of content (actors,buckets,spaces)
        """
        result:list([name,path])

    method:getBucketsWithPaths @method:get,post
        """
        """
        result:list([name,path])

    method:getActorsWithPaths @method:get,post
        """
        """
        result:list([name,path])

    method:getBuckets @method:get,post
        """
        """
        result:list(str)

    method:getActors @method:get,post
        """
        """
        result:list(str)


    method:notifySpaceModification @method:get,post
        """
        """
        var:id str,,id of space which changed# @tags: optional
        #var:name str,,name of space which changed @tags: optional
        result:bool

    method:notifySpaceNew @method:get,post
        """
        """
        var:path str,,path of content which got changed
        var:name str,,name
        result:bool

    method:notifySpaceDelete @method:get,post
        """
        """
        var:id str,,id of space which changed
        result:bool

    method:notifyBucketDelete @method:get,post
        """
        """
        var:id str,,id of bucket which changed
        result:bool

    method:notifyBucketModification @method:get,post
        """
        """
        var:id str,,id of bucket which changed
        result:bool

    method:notifyBucketNew @method:get,post
        """
        """
        var:path str,,path of content which got changed
        var:name str,,name
        result:bool

    method:notifyActorNew @method:get,post
        """
        """
        var:path str,,path of content which got changed
        var:name str,,name
        result:bool

    method:notifyActorModification @method:get,post
        """
        """
        var:id str,,id of actor which changed
        result:bool

    method:notifyActorDelete @method:get,post
        """
        """
        var:id str,,id of space which changed
        result:bool

    method:prepareActorSpecs @method:get,post
        """
        compress specs for specific actor and targz in appropriate download location
        """
        var:app str,,name of app
        var:actor str,,name of actor
        result:bool

    method:wikisave @noauth
        """
        """
        var:cachekey str,,key to the doc
        var:text str,,content of file to edit
        result:bool

    method:modelobjectlist @noauth returnformat:jsonraw method:get
        """
        TODO: describe what the goal is of this method
        """
        var:namespace str,,
        var:category str,,
        var:key str,,
        result:list

    method:bitbucketreload @noauth method:get,post
        """
        Reload all spaces from bitbucket post
        """
        var:spacename str,,
        result:list

    method:modelobjectupdate @noauth returnformat:html
        """
        post args with ref_$id which refer to the key which is stored per actor in the cache
        """
        var:appname str,,
        var:actorname str,,
        var:key str,,
        result:html

    method:notifySpaceNewDir @noauth tasklets method:get,post
        """
        """
        var:spacename str,,
        var:spacepath str,"",
        var:path str,,

    method:notifyActorNewDir @noauth method:get,post
        """
        """
        var:actorname str,,
        var:actorpath str,"",
        var:path str,,

    method:checkEvents @method:get
        """
        Check for events
        """
        var:cursor int,,cursor to get from
        result:dict
