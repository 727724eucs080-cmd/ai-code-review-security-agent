from dataclasses import dataclass


@dataclass
class Finding:

    title: str

    severity: str

    line_number: int

    description: str

    recommendation: str