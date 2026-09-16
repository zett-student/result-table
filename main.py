from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class TimeRecord:
    name: str
    start: datetime
    finish: datetime

    def dur(self):
        s = int((self.finish - self.start).total_seconds())
        return f"{s // 3600:02d}:{s % 3600 // 60:02d}:{s % 60:02d}"

class Table:
    def __init__(self, path):
        p = re.compile(
            r"([^:]+):(\d{1,2}:\d{2}(?::\d{2})?):(\d{1,2}:\d{2}(?::\d{2})?)"
        )
        t = lambda x:datetime.strptime(
            x, "%H:%M:%S" if x.count(":") == 2 else "%H:%M"
        )

        with open(path, encoding="utf-8") as f:
            self.rows = [
                TimeRecord(m[1].strip(), t(m[2]), t(m[3]))
                for l in f
                if (m:= p.match(l.strip()))
            ]

    def result(self):
        return [
            (
                r.name,
                r.start.time().isoformat(),
                r.finish.time().isoformat(),
                r.dur(),

            )
            for r in self.rows
        ]

for row in Table("data.txt").result():
    print(*row)