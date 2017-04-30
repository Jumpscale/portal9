[actor] @dbtype:fs
	"""
	An actor to perform actions for gitlab users
	"""    
    method:updateUserSpaces
		"""		
        Update gitlab user spaces
		"""
		result:int
		
	method:updateUserSpace
		"""		
        Update gitlab user spaces
		"""
		var:spacename str,,Space name [Must be valid gitlab space]
		result:int

    method:checkUpdateUserSpaceJob
        """
        Check Update gitlab user spaces job status
        """
        var:jobid str,, Update JOB ID
        result:str
