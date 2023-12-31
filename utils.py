import cv2
import tkinter as tk
from tkinter.simpledialog import askinteger, askstring
from constants import *

def draw_menu(frame, detections):
    text_offset = TOP_TEXT_OFFSET
    text_spacing = TEXT_SPACING

    for idx, detection in enumerate(detections):
        status, bbox, color, name = detection
        idx += 1
        text_offset += text_spacing  # Increase the offset for the next line

        # Draw text labels on detections
        cv2.putText(frame, name, (bbox[0], bbox[1] - 10), FONT, FONT_SCALE,
                    color, FONT_THICKNESS, LINE_TYPE)
        cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), color, 2)

        # Display status information at the top of the screen for each detection
        cv2.putText(frame, f"{name if name else ''}, {status}, Location: {bbox}",
                    (20, text_offset), FONT, FONT_SCALE, FONT_COLOR,
                    FONT_THICKNESS, LINE_TYPE)

def get_num_detections():
    root = tk.Tk()
    root.withdraw()
    num_detections = askinteger("Number of Detections", "Enter the number of detections you want: ")
    return num_detections

def get_detection_name(idx):
    root = tk.Tk()
    root.withdraw()
    name = askstring("Detection Name", f"Enter name for detection {idx + 1}: ")
    return name
