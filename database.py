"""
database.py
Stores lesson definitions based on the 'Magic Seeds LKG Literacy' textbook.
"""

from typing import List, Dict, Set

class LessonDatabase:
    def __init__(self):
        # Words to IGNORE (Generic instructions found on almost every page)
        self.stop_words: Set[str] = {
            "trace", "colour", "color", "write", "practise", "date", "name", 
            "class", "literacy", "lkg", "activity", "time", "page", "skills",
            "say", "these", "words", "that", "begin", "with", "the", "letter",
            "circle", "tick", "objects", "magic", "seeds", "password", "publishing"
        }

        # The Lesson Definitions
        self.lessons: List[Dict] = [
            # --- STROKES & LINES (Pages 8-13) ---
            {
                "id": "LKG_LINE_01",
                "topic": "Standing Lines",
                "type": "strokes",
                "keywords": ["standing", "lines", "rain", "top", "down"],
                "visual_cues": ["vertical_lines"]
            },
            {
                "id": "LKG_LINE_02",
                "topic": "Sleeping Lines",
                "type": "strokes",
                "keywords": ["sleeping", "lines", "road", "flat"],
                "visual_cues": ["horizontal_lines"]
            },
            {
                "id": "LKG_LINE_03",
                "topic": "Slanting Lines",
                "type": "strokes",
                "keywords": ["slanting", "lines", "cloud", "rain"],
                "visual_cues": ["slanting_lines"] # Custom logic needed
            },

            # --- LETTER 'A' SERIES (Pages 16-18) ---
            {
                "id": "LKG_ALPHA_A_INTRO",
                "topic": "Letter A - Intro",
                "type": "alphabet_oral",
                "letter": "A",
                "keywords": ["oral", "language", "development", "apple", "ant", "anchor", "alligator", "axe", "anthill", "arrow"],
                "visual_cues": ["large_char"] # Look for massive 'Aa'
            },
            {
                "id": "LKG_ALPHA_A_ACT",
                "topic": "Letter A - Activity",
                "type": "alphabet_activity",
                "letter": "A",
                "keywords": ["phonological", "awareness", "sight", "words", "an", "as", "at", "am", "apple", "ant"],
                "visual_cues": [] 
            },
            {
                "id": "LKG_ALPHA_A_WRITE",
                "topic": "Letter A - Writing",
                "type": "alphabet_writing",
                "letter": "A",
                "keywords": ["modelled", "writing", "independent", "sing", "along", "sound"],
                "visual_cues": ["grid_detected"]
            },

            # --- LETTER 'B' SERIES (Pages 19-21) ---
            {
                "id": "LKG_ALPHA_B_INTRO",
                "topic": "Letter B - Intro",
                "type": "alphabet_oral",
                "letter": "B",
                "keywords": ["bee", "beehive", "boat", "butterfly", "banana", "book", "boy", "bus"],
                "visual_cues": ["large_char"]
            },
            {
                "id": "LKG_ALPHA_B_ACT",
                "topic": "Letter B - Activity",
                "type": "alphabet_activity",
                "letter": "B",
                "keywords": ["sight", "words", "be", "by", "bye", "but", "big", "ball", "balloon"],
                "visual_cues": []
            },
            {
                "id": "LKG_ALPHA_B_WRITE",
                "topic": "Letter B - Writing",
                "type": "alphabet_writing",
                "letter": "B",
                "keywords": ["modelled", "writing", "bat", "sound"],
                "visual_cues": ["grid_detected"]
            },

            # --- STORIES ---
            {
                "id": "LKG_STORY_CROW",
                "topic": "The Thirsty Crow",
                "type": "story",
                "keywords": ["thirsty", "crow", "pot", "water", "pebbles", "drank", "flew", "hot", "sunny"],
                "visual_cues": []
            },

            # --- CONCEPTS ---
            {
                "id": "LKG_CONCEPT_MYSELF",
                "topic": "Myself",
                "type": "concept",
                "keywords": ["myself", "name", "years", "old", "study", "boy", "girl"],
                "visual_cues": []
            }
        ]

    def get_lessons(self) -> List[Dict]:
        return self.lessons

    def is_stop_word(self, word: str) -> bool:
        return word.lower() in self.stop_words