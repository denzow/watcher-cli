import time
import argparse
from watcher.watcher import CommandArgs, WatcherBase


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c',
        '--config',
        help='config yaml file',
        default=None,
        required=True,
    )
    args = parser.parse_args()
    return CommandArgs(
        config_file_name=args.config
    )


def main():
    command_args = parse_args()
    print('start watch', command_args)
    watcher = WatcherBase(command_args)
    watcher.run()

