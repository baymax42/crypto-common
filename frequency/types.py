from enum import Enum
from typing import NewType, Dict

NGramCountMap = NewType("NGramMap", Dict[str, int])
NGramFrequencyMap = NewType("NGramFrequencyMap", Dict[str, float])


class Language(Enum):
    ENGLISH = 'en'


class NGramType(Enum):
    MONOGRAM = 1
    BIGRAM = 2
    TRIGRAM = 3
    QUADRAGRAM = 4
