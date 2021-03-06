class IADError(Exception): pass


class RequestError(IADError):
    def __init__(self, json):
        self.json = json or {}
        super().__init__(json.get("error", "fatal error getting upload info."))

    def __repr__(self):
        return f"<RequestError json={repr(self.json)}>"

    def __dict__(self):
        return self.json
    
    def __getitem__(self, key):
        return self.json[key]

class InvalidContentType(IADError):
    def __init__(self, _type):
        super().__init__(f"{_type} is an API blacklisted file extension.")

class JsonDecodeException(IADError):
    def __init__(self, raw):
        self.raw = raw
        super().__init__(f"Failed to decode json from API. Raw content:\n{self.raw}")
    
    def __str__(self):
        return self.raw.decode('utf-8')
    
    def __repr__(self):
        return f"<JsonDecodeException raw={repr(self.raw)}>"
    
    def __bytes__(self):
        return self.raw
