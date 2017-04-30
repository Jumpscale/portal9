[actor] @dbtype:mem #tasklets
	"""
	this actor manages all content on the wiki
	can e.g. notify wiki/appserver of updates of content
	"""    
    method:notifyFiledir
		"""		
		"""
		var:path str,,path of content which got changed
        result:bool    

    method:getSpaces
		"""		
		"""
        result:list(str)
		
    method:getSpacesWithPaths
		"""		
		"""
        result:list([name,path])

    method:getContentDirsWithPaths
		"""		
		return root dirs of content (actors,buckets,spaces)
		"""
        result:list([name,path])

    method:getBucketsWithPaths
		"""		
		"""
        result:list([name,path])
 
    method:getActorsWithPaths
        """		
        """
        result:list([name,path])
 
    method:getBuckets
		"""		
		"""
        result:list(str)

    method:getActors
		"""		
		"""
        result:list(str)


    method:notifySpaceModification
		"""		
		"""
		var:id str,,id of space which changed# @tags: optional
        #var:name str,,name of space which changed @tags: optional
        result:bool    

    method:notifySpaceNew
		"""		
		"""
		var:path str,,path of content which got changed
		var:name str,,name 
		result:bool    

    method:notifySpaceDelete
		"""		
		"""
		var:id str,,id of space which changed
		result:bool    

    method:notifyBucketDelete
		"""		
		"""
		var:id str,,id of bucket which changed
		result:bool  

    method:notifyBucketModification
		"""		
		"""
		var:id str,,id of bucket which changed
        result:bool    

    method:notifyBucketNew
		"""		
		"""
		var:path str,,path of content which got changed
		var:name str,,name 
		result:bool    

    method:notifyActorNew
		"""		
		"""
		var:path str,,path of content which got changed
		var:name str,,name 
		result:bool 

    method:notifyActorModification
		"""		
		"""
		var:id str,,id of actor which changed
        result:bool  

    method:notifyActorDelete
		"""		
		"""
		var:id str,,id of space which changed
		result:bool 


    method:prepareActorSpecs
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

    method:modelobjectlist @noauth returnformat:jsonraw
        """
        TODO: describe what the goal is of this method
        """
        var:namespace str,,
        var:category str,,
        var:key str,,
        result:list

    method:bitbucketreload @noauth
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

    method:notifySpaceNewDir @noauth tasklets
        """
        """
        var:spacename str,,
        var:spacepath str,"",
        var:path str,,

    method:notifyActorNewDir @noauth
        """
        """
        var:actorname str,,
        var:actorpath str,"",
        var:path str,,



