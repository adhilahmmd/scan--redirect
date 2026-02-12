import mysql.connector

# --- CONFIGURATION ---
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',        # UPDATE THIS
    'password': 'Adhil123',# UPDATE THIS
    'database': 'lkg_literacy'
}

# --- 1. FULL ALPHABET DATA (A-Z) ---
ALPHABET_DATA = {
    "A": ["apple", "ant", "anchor", "alligator", "axe", "arrow", "anthill"],
    "B": ["ball", "bat", "boy", "balloon", "bear", "bus", "banana", "beehive"],
    "C": ["cat", "cap", "cup", "car", "cake", "candle", "camel", "cow"],
    "D": ["dog", "drum", "doll", "duck", "door", "dragonfly", "daisy"],
    "E": ["elephant", "egg", "engine", "elbow", "envelope", "eskimo"],
    "F": ["fish", "fan", "frog", "flower", "flag", "father", "fork"],
    "G": ["goat", "grapes", "girl", "gate", "grass", "guitar", "gift"],
    "H": ["hat", "hen", "house", "horse", "helicopter", "honey", "hill"],
    "I": ["ice", "igloo", "ink", "insect", "iguana", "inkpot"],
    "J": ["jug", "jeep", "jam", "joker", "jacket", "jellyfish", "jackfruit"],
    "K": ["kite", "key", "king", "kangaroo", "kettle", "kitten", "kiwi"],
    "L": ["lion", "leaf", "lamp", "lock", "lemon", "ladder", "lamb"],
    "M": ["mango", "moon", "monkey", "man", "mat", "milk", "mushroom"],
    "N": ["nest", "net", "nose", "nurse", "nib", "napkin", "nuts", "nightingale"],
    "O": ["orange", "owl", "ox", "octopus", "ostrich", "olive", "orchid"],
    "P": ["parrot", "pen", "pencil", "pig", "peacock", "panda", "pumpkin"],
    "Q": ["queen", "quill", "quilt", "queue", "quail"],
    "R": ["rat", "rose", "rabbit", "ring", "rainbow", "rocket", "rooster"],
    "S": ["sun", "star", "spoon", "snake", "socks", "snail", "squirrel"],
    "T": ["tiger", "tree", "tap", "top", "tomato", "table", "tent"],
    "U": ["umbrella", "urn", "uncle", "uniform", "umpire", "upstairs"],
    "V": ["van", "vase", "violin", "vegetables", "vulture", "volcano"],
    "W": ["watch", "wall", "well", "wheel", "watermelon", "wolf", "window"],
    "X": ["xray", "xylophone", "xmas", "box", "fox"],
    "Y": ["yak", "yo-yo", "yellow", "yatch", "yarn", "yolk"],
    "Z": ["zebra", "zip", "zero", "zoo", "zigzag"]
}

# --- 2. STATIC TOPICS (Lines, Stories, Concepts) ---
# Format: (Code, Name, Type, Letter, Keywords_List, Visuals_List)
STATIC_LESSONS = [
    ("LKG_TOPIC_STANDING", "Standing Lines", "topic", None, ["standing", "lines", "rain"], ["vertical_lines"]),
    ("LKG_TOPIC_SLEEPING", "Sleeping Lines", "topic", None, ["sleeping", "lines", "road"], ["horizontal_lines"]),
    ("LKG_TOPIC_SLANTING", "Slanting Lines", "topic", None, ["slanting", "lines", "cloud"], ["slanting_lines"]),
    ("LKG_TOPIC_CURVED", "Curved Lines", "topic", None, ["curved", "lines", "umbrella"], []),
    ("LKG_TOPIC_PATTERNS", "Patterns", "topic", None, ["patterns", "zig", "zag"], []),
    ("LKG_TOPIC_ACTION", "Action Words", "topic", None, ["action", "words", "eat", "run", "jump", "sleep"], []),
    ("LKG_TOPIC_THIS_THAT", "This and That", "topic", None, ["this", "that", "is", "a"], []),
    ("LKG_TOPIC_OPPOSITES", "Opposites", "topic", None, ["opposites", "tall", "short", "big", "small", "day", "night"], []),
    ("LKG_TOPIC_VOWELS", "Vowels", "topic", None, ["vowels", "sound", "a", "e", "i", "o", "u"], []),
    ("LKG_TOPIC_PRONOUNS", "I, We, You, He", "topic", None, ["we", "you", "he", "she", "it", "they"], []),
    ("LKG_TOPIC_MYSELF", "Myself", "topic", None, ["myself", "years", "old", "study", "name"], []),
    ("LKG_STORY_CROW", "The Thirsty Crow", "story", None, ["thirsty", "crow", "pot", "water", "pebbles"], [])
]

def seed_full_database():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("Connected to MySQL.")
        
        # Optional: Clear existing data to avoid duplicates
        print("Clearing old data...")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        cursor.execute("TRUNCATE TABLE lesson_keywords;")
        cursor.execute("TRUNCATE TABLE lesson_visuals;")
        cursor.execute("TRUNCATE TABLE lessons;")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

        # 1. Insert Static Lessons
        print("Inserting Static Topics...")
        for code, name, l_type, letter, kws, visuals in STATIC_LESSONS:
            cursor.execute(
                "INSERT INTO lessons (lesson_code, name, type, target_letter) VALUES (%s, %s, %s, %s)", 
                (code, name, l_type, letter)
            )
            lesson_id = cursor.lastrowid
            
            for kw in kws:
                cursor.execute("INSERT INTO lesson_keywords (lesson_id, keyword) VALUES (%s, %s)", (lesson_id, kw))
            
            for vis in visuals:
                cursor.execute("INSERT INTO lesson_visuals (lesson_id, visual_cue) VALUES (%s, %s)", (lesson_id, vis))

        # 2. Insert Alphabet Lessons
        print("Inserting Alphabet (A-Z)...")
        for letter, kws in ALPHABET_DATA.items():
            cursor.execute(
                "INSERT INTO lessons (lesson_code, name, type, target_letter) VALUES (%s, %s, %s, %s)", 
                (f"LKG_LETTER_{letter}", f"Letter {letter}", "alphabet", letter)
            )
            lesson_id = cursor.lastrowid
            
            for kw in kws:
                cursor.execute("INSERT INTO lesson_keywords (lesson_id, keyword) VALUES (%s, %s)", (lesson_id, kw))

        conn.commit()
        print("✅ SUCCESS: Database has been fully populated!")

    except mysql.connector.Error as err:
        print(f"❌ Error: {err}")
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

if __name__ == "__main__":
    seed_full_database()