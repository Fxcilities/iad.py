class IADError(Exception):
    """Base Exception"""
    pass

class RequestError(IADError):
    """Request failed"""
    pass