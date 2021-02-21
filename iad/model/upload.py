from datetime import datetime

class Upload:
    def __init__(self, json, time=None):
        self._json = json or {}
        self.name = json.get('filename')
        self.user = json.get('username')
        self.url = json.get('url', '').replace("\\", "")
        self.time = time or datetime.now()
    
    def __dict__(self):
        return self._json
    
    def __getitem__(self, key):
        return self._json[key]
    
    def __repr__(self):
        return f"<Upload name={self.name} user={self.user} url={self.url}>"