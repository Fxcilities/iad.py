from dataclasses import dataclass
from datetime import datetime

@dataclass
class Upload:
    name: str
    user: str
    url: str
    created_at: datetime