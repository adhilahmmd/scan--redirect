"""
processor.py
Handles Image Processing (OpenCV) and Tesseract OCR.
"""

import cv2
import numpy as np
import pytesseract
from typing import Dict, Any

class PageProcessor:
    def __init__(self, tesseract_cmd: str = None):
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    def extract_text(self, image: np.ndarray) -> str:
        """
        Standard OCR extraction pipeline.
        """
        if image is None: return ""
        
        # 1. Grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 2. Denoise (Essential for book pages with background art)
        # Using bilateral filter to keep edges sharp (text) but smooth noise
        denoised = cv2.bilateralFilter(gray, 9, 75, 75)
        
        # 3. Threshold (Otsu)
        _, binary = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # 4. Run Tesseract
        # --psm 6 assumes a single uniform block of text.
        # --psm 3 is fully automatic (sometimes better for complex pages)
        try:
            text = pytesseract.image_to_string(binary, config=r'--oem 3 --psm 3')
            return text
        except Exception as e:
            print(f"OCR Error: {e}")
            return ""

    def analyze_visual_features(self, image: np.ndarray) -> Dict[str, Any]:
        """
        Detects structural features: Lines (Standing/Sleeping) and Grids.
        """
        features = {
            "vertical_lines": False,
            "horizontal_lines": False,
            "grid_detected": False,
            "complexity": "low" # High complexity = Story/Picture, Low = Writing
        }
        
        if image is None: return features

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)

        # 1. Line Detection (Hough)
        # Threshold=100 means a line must be quite long to count (ignoring letter strokes)
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, minLineLength=100, maxLineGap=10)
        
        v_count, h_count = 0, 0
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                angle = np.arctan2(y2 - y1, x2 - x1) * 180.0 / np.pi
                if 80 <= abs(angle) <= 100: v_count += 1
                elif abs(angle) <= 10 or abs(angle) >= 170: h_count += 1

        if v_count > 3 and v_count > h_count: features["vertical_lines"] = True
        if h_count > 3 and h_count > v_count: features["horizontal_lines"] = True

        # 2. Grid Detection (Contours)
        # Useful for identifying "Modelled Writing" pages (boxes for letters)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        rect_count = 0
        for cnt in contours:
            approx = cv2.approxPolyDP(cnt, 0.04 * cv2.arcLength(cnt, True), True)
            area = cv2.contourArea(cnt)
            # Look for medium/large rectangles
            if len(approx) == 4 and area > 1000:
                rect_count += 1
        
        if rect_count > 2: features["grid_detected"] = True
        
        return features