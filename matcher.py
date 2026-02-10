"""
matcher.py
Logic Engine: Matches text/visuals to the LKG Literacy Database.
"""

import re
from collections import Counter
from typing import Dict, Any, List
from database import LessonDatabase

class LessonMatcher:
    def __init__(self, db: LessonDatabase):
        self.db = db

    def _process_context(self, raw_text: str) -> Dict[str, Any]:
        """
        Cleans text and counts words.
        """
        # Normalize
        text_lower = raw_text.lower()
        
        # Extract meaningful words
        words = re.findall(r'\b[a-z]+\b', text_lower)
        clean_words = [w for w in words if not self.db.is_stop_word(w)]
        word_counts = Counter(clean_words)
        
        # Extract isolated single letters (A, B, C)
        # Tesseract often reads "A A A" as "A A A".
        # We look for UPPERCASE letters in the raw text specifically.
        upper_chars = [c for c in raw_text if c.isupper() and c.isalpha()]
        char_counts = Counter(upper_chars)

        return {
            "word_counts": word_counts,
            "char_counts": char_counts,
            "raw_text": text_lower
        }

    def identify_lesson(self, raw_text: str, visual_features: Dict[str, Any]) -> Dict[str, Any]:
        context = self._process_context(raw_text)
        candidates = []
        lessons = self.db.get_lessons()

        for lesson in lessons:
            score = 0
            reasons = []

            # --- RULE 1: Visual Structure (Hard Rule for Strokes) ---
            if lesson['type'] == 'strokes':
                # Strong visual match required for lines
                if "vertical_lines" in lesson['visual_cues'] and visual_features['vertical_lines']:
                    score += 50
                    reasons.append("Visual: Vertical lines detected")
                elif "horizontal_lines" in lesson['visual_cues'] and visual_features['horizontal_lines']:
                    score += 50
                    reasons.append("Visual: Horizontal lines detected")
                
                # Check for Title in text (e.g. "Standing Lines")
                # We check raw strings for multi-word phrases
                if lesson['topic'].lower() in context['raw_text']:
                    score += 40
                    reasons.append(f"Title match: '{lesson['topic']}' found")

            # --- RULE 2: Alphabet Logic ---
            elif 'alphabet' in lesson['type']:
                target_char = lesson['letter']
                
                # A. Letter Dominance
                # Does 'A' appear frequently?
                char_freq = context['char_counts'].get(target_char, 0)
                if char_freq > 2:
                    score += (char_freq * 2)
                    reasons.append(f"Letter dominance: '{target_char}' appeared {char_freq} times")

                # B. Page Type Differentiation (The tricky part)
                # 1. Intro Page ("Oral Language Development", Big Pictures)
                if lesson['type'] == 'alphabet_oral':
                    if "oral" in context['word_counts'] or "language" in context['word_counts']:
                        score += 30
                        reasons.append("Context: 'Oral Language' section detected")
                
                # 2. Activity Page ("Phonological", "Tick", "Circle")
                elif lesson['type'] == 'alphabet_activity':
                    if "phonological" in context['word_counts'] or "sight" in context['word_counts']:
                        score += 30
                        reasons.append("Context: 'Phonological/Sight Words' detected")

                # 3. Writing Page ("Modelled Writing", "Trace", Grids)
                elif lesson['type'] == 'alphabet_writing':
                    if "modelled" in context['word_counts'] or "writing" in context['word_counts']:
                        score += 30
                        reasons.append("Context: 'Modelled Writing' detected")
                    if visual_features['grid_detected']:
                        score += 20
                        reasons.append("Visual: Writing grid detected")

            # --- RULE 3: Keyword Overlap (Universal) ---
            # Used for Stories and to confirm Letters (e.g., "Ant" confirms "A")
            matches = 0
            for kw in lesson['keywords']:
                if context['word_counts'][kw] > 0:
                    matches += 1
                    reasons.append(f"Keyword match: '{kw}'")
            
            score += (matches * 10)

            if score > 0:
                candidates.append({
                    "lesson_id": lesson['id'],
                    "topic": lesson['topic'],
                    "score": score,
                    "reasons": reasons
                })

        # Sort results
        candidates.sort(key=lambda x: x['score'], reverse=True)

        result = {
            "top_match": candidates[0] if candidates else None,
            "confidence": "LOW",
            "alternatives": candidates[1:3] if len(candidates) > 1 else []
        }

        # Determine Confidence Level
        if result['top_match']:
            s = result['top_match']['score']
            if s >= 40: result['confidence'] = "HIGH"
            elif s >= 20: result['confidence'] = "MEDIUM"
        
        return result