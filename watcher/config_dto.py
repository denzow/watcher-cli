import dataclasses
import enum


class ModeType(enum.Enum):
    replace = 'replace'
    copy = 'copy'


@dataclasses.dataclass(frozen=True)
class WatchRule:
    dir: str
    recursive: bool
    match_rule: str
    mode: ModeType
    action: str

    @classmethod
    def from_config(cls, data: dict):
        return cls(
            dir=data['dir'],
            recursive=data['recursive'],
            match_rule=data['match_rule'],
            mode=ModeType[data['mode']],
            action=data['action'],
        )


@dataclasses.dataclass(frozen=True)
class WatchConfig:
    rules: list[WatchRule]

    @classmethod
    def from_config(cls, data: dict):
        return cls(
            rules=[
                WatchRule.from_config(d)
                for d in data.get('rules', [])
            ]
        )
