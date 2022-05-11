from pathlib import Path
from watchdog.events import FileSystemEventHandler, FileClosedEvent, FileSystemMovedEvent

from .config_dto import WatchRule
from .matcher import SQLMatcher


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
        self.matcher = SQLMatcher()

    def _is_match(self, file_path: str):

        try:
            path = Path(file_path)
            result = self.matcher.match(
                target=self.stat_to_json(path),
                condition=self.watch_rule.match_rule
            )
            return result
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

    @staticmethod
    def stat_to_json(path: Path) -> dict:
        s_obj = path.stat()
        stats = {k.split('st_')[1]: getattr(s_obj, k) for k in dir(s_obj) if k.startswith('st_')}
        stats['name'] = path.name
        return stats
