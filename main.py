"""
main.py
Entry point for the LKG Literacy Lesson Identifier.
"""

import sys
# Note: In a real environment with a camera, you would import cv2 here to load images.
from database import LessonDatabase
from processor import PageProcessor
from matcher import LessonMatcher

def print_result(result):
    print("-" * 40)
    print(f"CONFIDENCE: {result['confidence']}")
    if result['top_match']:
        m = result['top_match']
        print(f"LESSON ID : {m['lesson_id']} ({m['type']})")
        print(f"SCORE     : {m['score']}")
        print("REASONING :")
        for r in m['reasons']:
            print(f"  > {r}")
    else:
        print("No suitable lesson found.")
    print("-" * 40)

def run_simulation():
    """
    Simulates the pipeline without needing physical images.
    Useful for testing logic without a camera.
    """
    print("Running Simulation Mode...\n")
    
    # Init Pipeline
    db = LessonDatabase()
    matcher = LessonMatcher(db)
    # Processor not strictly needed for simulation, but instantiated for completeness
    # processor = PageProcessor() 

    # --- Scenario 1: Alphabet 'B' Page ---
    print("SCENARIO 1: User scans 'Letter B' tracing page")
    
    # Mock OCR output
    ocr_text_1 = """
    Name: _______  Date: ______
    Trace and colour.
    B B B B B
    Ball  Bat  Balloon
    b b b b b
    """
    # Mock Visuals (Grid detected for tracing boxes)
    visuals_1 = {
        "vertical_lines_detected": False,
        "horizontal_lines_detected": False,
        "grid_detected": True
    }
    
    result_1 = matcher.match(ocr_text_1, visuals_1)
    print_result(result_1)


    # --- Scenario 2: Prewriting Vertical Lines ---
    print("\nSCENARIO 2: User scans 'Standing Lines' worksheet")
    
    ocr_text_2 = """
    Practice standing lines.
    Start from the top.
    Rain
    """
    # Mock Visuals (Dominant vertical lines)
    visuals_2 = {
        "vertical_lines_detected": True,
        "horizontal_lines_detected": False,
        "grid_detected": False
    }
    
    result_2 = matcher.match(ocr_text_2, visuals_2)
    print_result(result_2)

def run_real_image(image_path: str):
    """
    Runs the pipeline on a real image file.
    """
    import cv2
    
    print(f"Processing Image: {image_path}")
    
    # 1. Setup
    db = LessonDatabase()
    processor = PageProcessor() # Add tesseract_cmd arg here if needed
    matcher = LessonMatcher(db)
    
    # 2. Load
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Could not load image.")
        return

    # 3. Process (Perception)
    print("Extracting text and features...")
    raw_text = processor.extract_text(image)
    visuals = processor.analyze_visual_features(image)
    
    # 4. Match (Logic)
    print("Identifying lesson...")
    result = matcher.match(raw_text, visuals)
    
    # 5. Output
    print_result(result)

if __name__ == "__main__":
    # To run simulation: python main.py
    # To run real image: python main.py /path/to/image.jpg
    
    if len(sys.argv) > 1:
        run_real_image(sys.argv[1])
    else:
        run_simulation()