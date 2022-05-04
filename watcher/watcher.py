import time
import pathlib
import dataclasses

import ruamel.yaml
from watchdog.observers import Observer

from .config_dto import WatchConfig
from .handler import Handler


yaml = ruamel.yaml.YAML()


@dataclasses.dataclass(frozen=True)
class CommandArgs:
    config_file_name: str


class WatcherBase:

    def __init__(self, args: CommandArgs):
        self.config = self._get_config_data(args.config_file_name)
        self._observers = []

    def run(self):
        for rule in self.config.rules:
            observer = Observer()
            handler = Handler()
            observer.schedule(handler, rule.dir, recursive=rule.recursive)
            observer.start()
            self._observers.append(observer)

        try:
            while True:
                time.sleep(1)
        finally:
            self._clear_observer()

    def _clear_observer(self):
        for observer in self._observers:
            observer.stop()
            observer.join()

    def _get_config_data(self, file_name: str):
        yaml_path = pathlib.Path(file_name)
        if not yaml_path.exists():
            raise Exception(f'{file_name} is not exist')

        with open(file_name) as f:
            data = yaml.load(f)
            watch_config = WatchConfig.from_config(data)
        return watch_config

