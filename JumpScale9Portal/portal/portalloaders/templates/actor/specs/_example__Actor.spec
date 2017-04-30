[actor] @dbtype:mem,redis,fs
	"""
	this is an example actor
	"""    
    method:dosomething
		"""		
		"""
		var:path str,,path of content which got changed
		var:id int,,an int
		var:bool int,,a bool
		result:bool    

    method:returnlist
		"""		
		"""
        result:list(str)
