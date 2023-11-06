class BymaDataAPIError(Exception):
    """BYMADATA API error."""
    
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

class UnexpectedResponseError(BymaDataAPIError):
    pass