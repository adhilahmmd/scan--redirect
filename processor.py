"""
processor.py
Handles Image Processing (OpenCV) and Text Extraction (Tesseract).
"""

import cv2
import numpy as np
import pytesseract
from typing import Dict, Any

class PageProcessor:
    def __init__(self, tesseract_cmd: str = None):
        """
        :param tesseract_cmd: Path to tesseract binary (e.g., r'C:\Program Files\Tesseract-OCR\tesseract.exe')
        """
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    def extract_text(self, image: np.ndarray) -> str:
        """
        Preprocesses image and runs OCR.
        """
        if image is None:
            return ""
            
        # 1. Grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 2. Thresholding (Binarization) to remove shadows/noise
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # 3. OCR Configuration
        # --psm 6: Assume a single uniform block of text (good for worksheets)
        # --psm 11: Sparse text (good for scattered words)
        config = r'--oem 3 --psm 6'
        
        try:
            text = pytesseract.image_to_string(binary, config=config)
            return text.strip()
        except Exception as e:
            print(f"[Error] OCR Failed: {e}")
            return ""

    def analyze_visual_features(self, image: np.ndarray) -> Dict[str, Any]:
        """
        Extracts structural features like line orientation and grids.
        """
        features = {
            "vertical_lines_detected": False,
            "horizontal_lines_detected": False,
            "grid_detected": False
        }
        
        if image is None:
            return features

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)

        # --- A. Line Detection (Hough Transform) ---
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50, minLineLength=50, maxLineGap=10)
        
        vertical_count = 0
        horizontal_count = 0
        
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                angle = np.arctan2(y2 - y1, x2 - x1) * 180.0 / np.pi
                
                # Vertical: ~90 deg, Horizontal: ~0 or ~180 deg
                if 80 <= abs(angle) <= 100:
                    vertical_count += 1
                elif abs(angle) <= 10 or abs(angle) >= 170:
                    horizontal_count += 1
        
        # Heuristic: Need a minimum number of lines to declare detection
        if vertical_count > 5 and vertical_count > horizontal_count:
            features["vertical_lines_detected"] = True
        if horizontal_count > 5 and horizontal_count > vertical_count:
            features["horizontal_lines_detected"] = True

        # --- B. Grid/Box Detection (Contours) ---
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        rect_count = 0
        for cnt in contours:
            # Approximate the contour shape
            approx = cv2.approxPolyDP(cnt, 0.04 * cv2.arcLength(cnt, True), True)
            area = cv2.contourArea(cnt)
            # 4 corners and sufficient size -> likely a box
            if len(approx) == 4 and area > 500: 
                rect_count += 1
        
        if rect_count > 3:
            features["grid_detected"] = True

        return features