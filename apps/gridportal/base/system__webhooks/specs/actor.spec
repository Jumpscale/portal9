[actor] @dbtype:mem,fs
    """
    """    
    method:mandrill @noauth
        """
        """
        var:mandrill_events str,,
        result:json

    method:github @noauth
        """
        """
        var:payload str,,
        result:json
