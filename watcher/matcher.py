from typing import Any
import sqlite3 as sqlite


class SQLMatcher:

    def __init__(self):
        self.conn = sqlite.connect(':memory:', check_same_thread=False)
        self.conn.row_factory = sqlite.Row

    def match(self, target: dict, condition: str) -> bool:
        cur = self.conn.cursor()
        cur.execute(f"""
        with target as (
            select
                {','.join([f"{self._value_to_value(v)} as {k}"for k, v in target.items()])}
        )
        select count(*) as hit from target where {condition}
        """)
        result = cur.fetchone()
        return result['hit'] == 1

    @staticmethod
    def _value_to_value(value: Any):
        if isinstance(value, str):
            return f'\'{value}\''
        return value
