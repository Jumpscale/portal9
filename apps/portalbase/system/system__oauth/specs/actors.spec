[actor] @dbtype:fs
	"""
	An actor to perform actions for gitlab users
	"""
    method:authenticate @noauth method:get,post
        """
        """
        var:type str,, [default to github] @tags: optional
        result:str

    method:authorize @noauth method:get,post
        """
        """
        result:str

    method:getOauthLogoutURl @noauth method:get,post
        """
        """
        result:str
