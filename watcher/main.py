import time
import argparse
import dataclasses


@dataclasses.dataclass(frozen=True)
class CommandArgs:
    config: str


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
        config=args.config
    )


def main():
    command_args = parse_args()
    print('start watch', command_args)
    while True:
        time.sleep(1)

