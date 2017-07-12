[actor] @dbtype:fs
	"""
	errorcondition handling
	"""    
    method:describeCategory
		"""	
        describe the errorcondition category (type)
        describe it as well as the possible solution
        is sorted per language	
		"""
		var:category str,,in dot notation e.g. pmachine.memfull
		var:language str,,language id e.g. UK,US,NL,FR  (TODO: chose right identication as used on internet and describe)
		var:description str,,describe this errorcondition category
        var:resolution_user str,,describe this errorcondition solution that the user can do himself
        var:resolution_ops str,,describe this errorcondition solution that the operator can do himself to try and recover from the situation
		result:bool
		
    method:delete
		"""	
		delete alert
		"""
		var:eco str,,eco ID
        result:bool

    method:purge
        """
        Remove ecos
        By default the logs en eco's older than than 1 week but this can be overriden
        """
        var:age str,, age of the records
        result: bool