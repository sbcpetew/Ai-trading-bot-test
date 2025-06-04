import os
from pathlib import Path


class KillSwitch:
    """Simple kill switch triggered by existence of a file."""

    def __init__(self, path: str = "./KILL"):  # kill file path
        self.path = Path(path)

    def armed(self) -> bool:
        return self.path.exists()

    def engage(self):
        self.path.touch()

    def disarm(self):
        if self.path.exists():
            self.path.unlink()
