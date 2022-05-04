from watchdog.events import FileSystemEventHandler, FileSystemEvent


class Handler(FileSystemEventHandler):

    def __int__(self, match_rule):
        self.match_rule = match_rule

    def _is_match(self, event: FileSystemEvent):
        if event.is_directory:
            return False
        return True

    def on_created(self, event: FileSystemEvent):
        if not self._is_match(event):
            return
        print(event)

    def on_modified(self, event: FileSystemEvent):
        if not self._is_match(event):
            return
        print(event)
