"""
database.py
Stores the static definitions for LKG Literacy lessons and domain-specific vocabulary.
"""

from typing import List, Dict, Set

class LessonDatabase:
    def __init__(self):
        # Words common in instructions that should NOT be used for identification
        self.stop_words: Set[str] = {
            "trace", "colour", "color", "write", "draw", "match", "circle",
            "the", "and", "is", "lesson", "page", "date", "name", "class",
            "activity", "worksheet", "grade", "literacy", "lkg"
        }

        # The core knowledge base
        self.lessons: List[Dict] = [
            {
                "id": "LKG_PRE_001",
                "grade": "LKG",
                "subject": "Literacy",
                "type": "prewriting",
                "subtype": "standing_lines",
                "keywords": ["standing", "straight", "rain", "top", "bottom", "down"],
                "visual_cues": ["vertical_lines"]
            },
            {
                "id": "LKG_PRE_002",
                "grade": "LKG",
                "subject": "Literacy",
                "type": "prewriting",
                "subtype": "sleeping_lines",
                "keywords": ["sleeping", "flat", "ladder", "floor", "bed"],
                "visual_cues": ["horizontal_lines"]
            },
            {
                "id": "LKG_ALPHA_A",
                "grade": "LKG",
                "subject": "Literacy",
                "type": "alphabet",
                "letter": "A",
                "keywords": ["apple", "ant", "aeroplane", "arrow", "axe", "arm"],
                "visual_cues": ["picture_grid", "large_char"]
            },
            {
                "id": "LKG_ALPHA_B",
                "grade": "LKG",
                "subject": "Literacy",
                "type": "alphabet",
                "letter": "B",
                "keywords": ["ball", "bat", "boy", "balloon", "bear", "bus"],
                "visual_cues": ["picture_grid", "large_char"]
            },
            {
                "id": "LKG_SIGHT_01",
                "grade": "LKG",
                "subject": "Literacy",
                "type": "sight_words",
                "subtype": "introduction",
                "keywords": ["am", "is", "are", "my", "he", "she"],
                "visual_cues": ["text_blocks"]
            }
        ]

    def get_lessons(self) -> List[Dict]:
        return self.lessons

    def is_stop_word(self, word: str) -> bool:
        return word.lower() in self.stop_words