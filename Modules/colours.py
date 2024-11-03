from dataclasses import dataclass


@dataclass
class BallColours:
    primary_colour: str
    secondary_colour: str
    name: str
    already_used: bool