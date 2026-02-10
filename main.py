"""
main.py
Entry point. 
"""

import sys
from database import LessonDatabase
from processor import PageProcessor
from matcher import LessonMatcher

# --- MOCK DATA FOR TESTING WITHOUT IMAGES ---
# This data comes directly from your PDF dump
MOCK_PAGE_16_A_INTRO = """
Oral Language Development
Aa
ant anchor alligator anthill
Note to the teacher: A few words that are not so familiar to the children are labelled.
"""

MOCK_PAGE_18_A_WRITE = """
Modelled Writing & Independent Writing
Trace and Colour. Say and Write.
A A A
a a a
Letter Art: Use crayons to trace the letter.
Sing along: /a/ is the sound of Letter A
"""

MOCK_PAGE_8_STANDING = """
Standing Lines
Trace and practise.
Rain Rain
"""

def run_test_cases():
    print("=== RUNNING SIMULATION TEST CASES ===")
    db = LessonDatabase()
    matcher = LessonMatcher(db)

    # Test 1: Letter A Intro (Page 16)
    print("\n--- Test 1: Page 16 (Letter A Intro) ---")
    # Simulate visuals: No grid, no lines
    vis = {"vertical_lines": False, "horizontal_lines": False, "grid_detected": False}
    res = matcher.identify_lesson(MOCK_PAGE_16_A_INTRO, vis)
    print_result(res)

    # Test 2: Letter A Writing (Page 18)
    print("\n--- Test 2: Page 18 (Letter A Writing) ---")
    # Simulate visuals: Grid detected for writing boxes
    vis = {"vertical_lines": False, "horizontal_lines": False, "grid_detected": True}
    res = matcher.identify_lesson(MOCK_PAGE_18_A_WRITE, vis)
    
    print_result(res)

    # Test 3: Standing Lines (Page 8)
    print("\n--- Test 3: Page 8 (Standing Lines) ---")
    # Simulate visuals: Vertical lines detected
    vis = {"vertical_lines": True, "horizontal_lines": False, "grid_detected": False}
    res = matcher.identify_lesson(MOCK_PAGE_8_STANDING, vis)
    print_result(res)

def print_result(result):
    if result['top_match']:
        m = result['top_match']
        print(f"✅ MATCH: {m['topic']} (ID: {m['lesson_id']})")
        print(f"   Confidence: {result['confidence']} (Score: {m['score']})")
        print("   Reasoning:")
        for r in m['reasons']:
            print(f"   - {r}")
    else:
        print("❌ NO MATCH FOUND")

def run_live_image(image_path):
    import cv2
    print(f"\n=== PROCESSING IMAGE: {image_path} ===")
    
    # 1. Setup
    db = LessonDatabase()
    # Path to Tesseract - UPDATE THIS FOR YOUR SYSTEM
    # Linux: '/usr/bin/tesseract'
    # Windows: r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    processor = PageProcessor() 
    matcher = LessonMatcher(db)

    # 2. Load
    img = cv2.imread(image_path)
    if img is None:
        print("Error: Could not load image")
        return

    # 3. Process
    print("Step 1: Extracting Text & Features...")
    text = processor.extract_text(img)
    visuals = processor.analyze_visual_features(img)
    print(f"   > Visuals Detected: {visuals}")
    
    # 4. Match
    print("Step 2: Identifying Lesson...")
    result = matcher.identify_lesson(text, visuals)
    print_result(result)

if __name__ == "__main__":
    # If file argument provided, run live mode. Else run simulation.
    if len(sys.argv) > 1:
        run_live_image(sys.argv[1])
    else:
        run_test_cases()