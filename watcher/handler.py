from pathlib import Path
from watchdog.events import FileSystemEventHandler, FileClosedEvent, FileSystemMovedEvent

from .config_dto import WatchRule


class Handler(FileSystemEventHandler):
    """
    mv 2.mp4 0.mp4
    > moved ./tmp/2.mp4
    cp 0.mp4 2.mp4
    > created ./tmp/2.mp4
    > modified ./tmp/2.mp4
    > closed ./tmp/2.mp4

    """

    def __init__(self, watch_rule: WatchRule):
        self.watch_rule = watch_rule
        self.creating_files = []

    def _is_match(self, file_path: str):

        try:
            path = Path(file_path)
            print(path.stat(), self.watch_rule.match_rule)
            return True
        except Exception as e:
            print(e)
            return False

    def on_moved(self, event: FileSystemMovedEvent):
        """
        new file moved
        """
        if event.is_directory:
            return
        if not self._is_match(event.dest_path):
            return
        print(event)

    def on_closed(self, event: FileClosedEvent):
        """
        new file created.
        """
        if event.is_directory:
            return
        if not self._is_match(event.src_path):
            return
        print(event)
