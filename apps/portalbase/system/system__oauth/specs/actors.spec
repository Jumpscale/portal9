[actor] @dbtype:fs
	"""
	An actor to perform actions for gitlab users
	"""    
    method:authenticate @noauth
        """
        """
        var:type str,, [default to github] @tags: optional
        result:str
        
    method:authorize @noauth
        """
        """
        result:str

    method:getOauthLogoutURl @noauth
        """
        """
        result:str
