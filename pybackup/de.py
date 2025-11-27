from dataclasses import dataclass
from pathlib import Path


@dataclass(order=True)
class FSe:
    sz: int
    mt: float

    def __hash__(self):
        return hash((self.sz, round(self.mt)))

    def __eq__(self, other):
        return self.sz == other.sz and round(self.mt) == round(other.mt)


@dataclass(order=True)
class DE:
    nm: Path
    i: FSe

    def __hash__(self):
        return hash((self.nm, self.i.sz, round(self.i.mt)))

    def __eq__(self, other):
        return self.nm == other.nm and self.i == other.i
