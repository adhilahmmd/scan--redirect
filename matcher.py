"""
matcher.py
"""
import re
from collections import Counter
from typing import Dict, Any, List
from database import LessonDatabase

class LessonMatcher:
    def __init__(self, db: LessonDatabase):
        self.db = db

    def _process_context(self, raw_text: str) -> Dict[str, Any]:
        text_lower = raw_text.lower()
        
        # Word Counts
        words = re.findall(r'\b[a-z]+\b', text_lower)
        clean_words = [w for w in words if not self.db.is_stop_word(w)]
        word_counts = Counter(clean_words)
        
        # Char Counts (Only uppercase for headers/tracing)
        upper_chars = [c for c in raw_text if c.isupper() and c.isalpha()]
        char_counts = Counter(upper_chars)

        return {
            "word_counts": word_counts,
            "char_counts": char_counts,
            "raw_text": raw_text
        }

    def identify_lesson(self, raw_text: str, visual_features: Dict[str, Any]) -> Dict[str, Any]:
        context = self._process_context(raw_text)
        candidates = []
        
        # Get EVERYTHING (Standing lines, Stories, Letter A, Letter B...)
        all_lessons = self.db.get_all_lessons()

        for lesson in all_lessons:
            score = 0
            reasons = []

            # --- 1. Visual Checks (Mainly for Lines) ---
            if "visuals" in lesson:
                if "vertical_lines" in lesson["visuals"] and visual_features["vertical_lines"]:
                    score += 50
                    reasons.append("Visual: Vertical lines detected")
                if "horizontal_lines" in lesson["visuals"] and visual_features["horizontal_lines"]:
                    score += 50
                    reasons.append("Visual: Horizontal lines detected")

            # --- 2. Title/Name Checks ---
            # Checks if "The Thirsty Crow" or "Standing Lines" is in text
            if lesson["name"].lower() in context["raw_text"].lower():
                score += 40
                reasons.append(f"Title detected: '{lesson['name']}'")

            # --- 3. Alphabet Specific Logic ---
            if lesson['type'] == 'alphabet':
                target_char = lesson['letter']
                # Check for "A A A" patterns
                char_freq = context["char_counts"].get(target_char, 0)
                if char_freq > 2:
                    score += (char_freq * 3)
                    reasons.append(f"Letter '{target_char}' frequency: {char_freq}")
                
                # Check if grid exists (Writing pages)
                if score > 10 and visual_features['grid_detected']:
                    score += 10
                    reasons.append("Visual: Grid detected")

            # --- 4. Keyword Overlap (Universal) ---
            matches = 0
            for kw in lesson["keywords"]:
                if context["word_counts"][kw] > 0:
                    matches += 1
                    reasons.append(f"Keyword: '{kw}'")
            
            if matches > 0:
                score += (matches * 15)

            # --- 5. Add to Candidates ---
            if score > 0:
                candidates.append({
                    "lesson_id": lesson["id"],
                    "name": lesson["name"],
                    "score": score,
                    "reasons": reasons
                })

        # Sort results
        candidates.sort(key=lambda x: x['score'], reverse=True)

        result = {
            "top_match": candidates[0] if candidates else None,
            "confidence": "LOW"
        }

        if result['top_match']:
            s = result['top_match']['score']
            if s >= 40: result['confidence'] = "HIGH"
            elif s >= 20: result['confidence'] = "MEDIUM"

        return result