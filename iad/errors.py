class IADError(Exception):
    """Base Exception"""
    pass

class RequestError(IADError):
    """Request failed"""
    pass

##########################################

class JsonDecodeException(RequestError): ...

class InvalidToken(RequestError): ...

class InvalidContentType(RequestError): ...