"""
database.py
MySQL Implementation for LKG Literacy System.
"""
import mysql.connector
from typing import List, Dict, Set

class LessonDatabase:
    def __init__(self):
        # Database Configuration - UPDATE THESE VALUES
        self.db_config = {
            'host': 'localhost',
            'user': 'root',       # Your MySQL username
            'password': 'Adhil123', # Your MySQL password
            'database': 'lkg_literacy'
        }

        # Stop words remain hardcoded as they rarely change
        self.stop_words: Set[str] = {
            "trace", "colour", "color", "write", "practise", "date", "name", 
            "class", "literacy", "lkg", "activity", "time", "page", "skills",
            "say", "these", "words", "that", "begin", "with", "the", "letter",
            "circle", "tick", "objects", "contents", "magic", "seeds"
        }

    def _get_connection(self):
        return mysql.connector.connect(**self.db_config)

    def get_all_lessons(self) -> List[Dict]:
        """
        Fetches all lessons + keywords + visuals from MySQL 
        and reconstructs the dictionary structure.
        """
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)

        # 1. Fetch Basic Lesson Info
        query_lessons = "SELECT id, lesson_code, name, type, target_letter FROM lessons"
        cursor.execute(query_lessons)
        rows = cursor.fetchall()

        lessons_map = {}

        # Initialize the dictionary structure
        for row in rows:
            l_id = row['id']
            lessons_map[l_id] = {
                "id": row['lesson_code'],
                "name": row['name'],
                "type": row['type'],
                "letter": row['target_letter'],
                "keywords": [],
                "visuals": []
            }

        # 2. Fetch Keywords
        query_kw = "SELECT lesson_id, keyword FROM lesson_keywords"
        cursor.execute(query_kw)
        for row in cursor.fetchall():
            l_id = row['lesson_id']
            if l_id in lessons_map:
                lessons_map[l_id]['keywords'].append(row['keyword'])

        # 3. Fetch Visual Cues
        query_vis = "SELECT lesson_id, visual_cue FROM lesson_visuals"
        cursor.execute(query_vis)
        for row in cursor.fetchall():
            l_id = row['lesson_id']
            if l_id in lessons_map:
                lessons_map[l_id]['visuals'].append(row['visual_cue'])

        cursor.close()
        conn.close()

        # Convert map values to a list
        return list(lessons_map.values())

    def is_stop_word(self, word: str) -> bool:
        return word.lower() in self.stop_words

# --- HELPER SCRIPT TO SEED DATA (RUN ONCE) ---
def seed_database():
    """
    Utility function to insert the initial data into MySQL.
    Run this function once to populate your empty database.
    """
    db = LessonDatabase()
    conn = db._get_connection()
    cursor = conn.cursor()

    # Data from previous step
    static_lessons = [
        ("LKG_TOPIC_STANDING", "Standing Lines", "topic", None, ["standing", "lines", "rain"], ["vertical_lines"]),
        ("LKG_TOPIC_SLEEPING", "Sleeping Lines", "topic", None, ["sleeping", "lines", "road"], ["horizontal_lines"]),
        ("LKG_STORY_CROW", "The Thirsty Crow", "story", None, ["thirsty", "crow", "pot", "water"], [])
    ]
    
    # Alphabet Data A-Z (Simplified for example)
    alphabet_data = {
        "A": ["apple", "ant", "anchor"],
        "B": ["ball", "bat", "boy"],
        "C": ["cat", "cap", "cup"]
        # Add D-Z here...
    }

    print("Seeding Static Lessons...")
    for code, name, l_type, letter, kws, visuals in static_lessons:
        cursor.execute("INSERT INTO lessons (lesson_code, name, type, target_letter) VALUES (%s, %s, %s, %s)", (code, name, l_type, letter))
        lesson_id = cursor.lastrowid
        for kw in kws:
            cursor.execute("INSERT INTO lesson_keywords (lesson_id, keyword) VALUES (%s, %s)", (lesson_id, kw))
        for vis in visuals:
            cursor.execute("INSERT INTO lesson_visuals (lesson_id, visual_cue) VALUES (%s, %s)", (lesson_id, vis))

    print("Seeding Alphabet...")
    for letter, kws in alphabet_data.items():
        cursor.execute("INSERT INTO lessons (lesson_code, name, type, target_letter) VALUES (%s, %s, %s, %s)", 
                       (f"LKG_LETTER_{letter}", f"Letter {letter}", "alphabet", letter))
        lesson_id = cursor.lastrowid
        for kw in kws:
            cursor.execute("INSERT INTO lesson_keywords (lesson_id, keyword) VALUES (%s, %s)", (lesson_id, kw))

    conn.commit()
    print("Database Seeded Successfully!")
    cursor.close()
    conn.close()

if __name__ == "__main__":
    # UNCOMMENT THIS LINE ONLY ONCE TO FILL DATA
    #seed_database() 
    pass