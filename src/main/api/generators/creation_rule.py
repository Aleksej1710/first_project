from dataclasses import dataclass

@dataclass(frozen=True)
class CreationRule:
    regex: str

