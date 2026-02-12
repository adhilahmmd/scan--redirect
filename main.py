"""
main.py
"""
import sys
import cv2
from database import LessonDatabase
from processor import PageProcessor
from matcher import LessonMatcher

def print_result(result):
    if result['top_match']:
        m = result['top_match']
        print("-" * 40)
        print(f"✅ LESSON FOUND: {m['name']}")
        print(f"   ID        : {m['lesson_id']}")
        print(f"   Confidence: {result['confidence']} (Score: {m['score']})")
        print("   Reasoning :")
        for r in m['reasons']:
            print(f"   - {r}")
        print("-" * 40)
    else:
        print("❌ No matching lesson found. Please rescan.")

def run_live_image(image_path):
    print(f"\nProcessing: {image_path}...")
    
    # Init System
    db = LessonDatabase()
    processor = PageProcessor()
    matcher = LessonMatcher(db)

    # Load
    img = cv2.imread(image_path)
    if img is None:
        print("Error: Could not load image. Check path.")
        return

    # Process
    text = processor.extract_text(img)
    visuals = processor.analyze_visual_features(img)
    
    # Match
    result = matcher.identify_lesson(text, visuals)
    print_result(result)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Join args to handle spaces in folder names
        full_path = " ".join(sys.argv[1:])
        # Strip quotes if user added them
        full_path = full_path.strip('"').strip("'")
        run_live_image(full_path)
    else:
        print("Please provide an image path.")
        print('Usage: python main.py "C:\\Path\\To\\Image.jpg"')