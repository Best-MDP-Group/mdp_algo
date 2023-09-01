from enum import Enum

class TurnType(Enum):
    SMALL = "Jockey by one cell, facing the same direction"
    MEDIUM = "90 degree turn"
    LARGE = "180 degree turn"
