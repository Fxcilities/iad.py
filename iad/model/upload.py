from dataclasses import dataclass

@dataclass
class Upload:
    name: str
    user: str
    url: str