[actor] @dbtype:fs
	"""
	alerts handling
	"""    
    method:update
		"""	
		update alert state and history
		"""
		var:username str,,username @tags: optional
		var:state str,,state ["NEW","ALERT", 'ACCEPTED',  'RESOLVED',  'UNRESOLVED', 'CLOSED']
		var:alert str,,alert ID
        var:comment str,,comment @tags: optional
        result:bool


    method:escalate
		"""	
        Escalte an event to the next level
		"""
		var:username str,,username @tags: optional
		var:alert str,,alert ID
        var:comment str,,comment @tags: optional
        result:bool
