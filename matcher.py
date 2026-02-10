"""
matcher.py
Deterministic logic engine.
Applies scoring rules to context to identify the correct lesson.
"""

import re
from collections import Counter
from typing import Dict, Any, List, Optional
from database import LessonDatabase

class LessonMatcher:
    def __init__(self, db: LessonDatabase):
        self.db = db

    def _analyze_text_context(self, raw_text: str) -> Dict[str, Any]:
        """
        Parses raw text into counts of words and individual letters.
        """
        # 1. Normalize
        text_lower = raw_text.lower()
        
        # 2. Extract Words
        words = re.findall(r'\b\w+\b', text_lower)
        clean_words = [w for w in words if not self.db.is_stop_word(w)]
        word_counts = Counter(clean_words)
        
        # 3. Extract Letters (Case sensitive often matters for worksheets, but we stick to upper for ID)
        letters_only = [c.upper() for c in raw_text if c.isalpha()]
        letter_counts = Counter(letters_only)

        return {
            "clean_words": clean_words,
            "word_counts": word_counts,
            "letter_counts": letter_counts,
            "raw_len": len(raw_text)
        }

    def match(self, raw_text: str, visual_features: Dict[str, Any]) -> Dict[str, Any]:
        """
        The Master Rule Engine.
        """
        context = self._analyze_text_context(raw_text)
        candidates = []
        lessons = self.db.get_lessons()

        for lesson in lessons:
            score = 0
            reasons = []

            # --- RULE 1: Lesson Type Filtering (Hard Visual Rules) ---
            if lesson['type'] == 'prewriting':
                if lesson['subtype'] == 'standing_lines' and visual_features['vertical_lines_detected']:
                    score += 50
                    reasons.append("Visual: Vertical lines match standing lines activity")
                elif lesson['subtype'] == 'sleeping_lines' and visual_features['horizontal_lines_detected']:
                    score += 50
                    reasons.append("Visual: Horizontal lines match sleeping lines activity")
                
                # Prewriting usually has very little text compared to stories
                if context['raw_len'] < 60:
                    score += 15
                    reasons.append("Context: Low text density consistent with prewriting")

            # --- RULE 2: Alphabet Matching (Letter Dominance) ---
            if lesson['type'] == 'alphabet':
                target_letter = lesson['letter']
                
                # Score based on how often the letter appears (e.g. "A A A a a a")
                letter_freq = context['letter_counts'].get(target_letter, 0)
                if letter_freq > 3:
                    score += (letter_freq * 3)
                    reasons.append(f"Letter dominance: '{target_letter}' count = {letter_freq}")

                # Visual confirmation
                if visual_features['grid_detected']:
                    score += 10
                    reasons.append("Visual: Picture/Tracing grid detected")

            # --- RULE 3: Keyword Overlap (The Semantic Bridge) ---
            # This applies to all lesson types
            keyword_hits = 0
            for kw in lesson['keywords']:
                if context['word_counts'][kw] > 0:
                    keyword_hits += 1
                    reasons.append(f"Keyword match: '{kw}'")
            
            score += (keyword_hits * 20) # High weight for explicit keywords

            # Add to candidates
            if score > 0:
                candidates.append({
                    "lesson_id": lesson['id'],
                    "type": lesson['type'],
                    "score": score,
                    "reasons": reasons
                })

        # --- FINAL ARBITRATION ---
        candidates.sort(key=lambda x: x['score'], reverse=True)

        result = {
            "status": "success",
            "confidence": "LOW",
            "top_match": None,
            "alternatives": []
        }

        if candidates:
            top = candidates[0]
            result['top_match'] = top
            
            # Confidence Thresholds
            if top['score'] >= 40:
                result['confidence'] = "HIGH"
            elif top['score'] >= 20:
                result['confidence'] = "MEDIUM"
                
            if len(candidates) > 1:
                result['alternatives'] = candidates[1:3]

        return result