import cv2
import numpy as np
import sys
from utils import draw_menu, get_num_detections, get_detection_name
from constants import FPS_POSITION, VIDEO_PATH


def main():
    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        print("Could not open video")
        sys.exit()

    ret, frame = cap.read()
    if not ret:
        print("Cannot read video file")
        sys.exit()

    num_selections = get_num_detections()

    detections = []

    for i in range(num_selections):
        bbox = cv2.selectROI(f"Select ROI {i + 1}", frame)
        color = tuple(map(int, (255 * np.random.rand(3))))
        # Initialize name as empty string
        detections.append(("Tracking", bbox, color, ""))

        name = get_detection_name(i)
        detections[i] = (detections[i][0], detections[i][1],
                         detections[i][2], name)  # Update name

        cv2.destroyWindow(f"Select ROI {i + 1}")

    trackers = [cv2.TrackerCSRT_create() for _ in detections]

    for idx, detection in enumerate(detections):
        status, bbox, color, name = detection
        ret = trackers[idx].init(frame, bbox)

    while True:
        ret, frame = cap.read()

        start_time = cv2.getTickCount()

        if not ret:
            break

        for idx, tracker in enumerate(trackers):
            status, bbox, color, name = detections[idx]
            ret, bbox = tracker.update(frame)

            if ret:
                p1 = (int(bbox[0]), int(bbox[1]))
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                cv2.rectangle(frame, p1, p2, color, 2)
                status = "Tracking"
            else:
                status = "Tracking failure detected"

            detections[idx] = (status, bbox, color, name)
            draw_menu(frame, detections)

        end_time = cv2.getTickCount()
        fps = cv2.getTickFrequency() / (end_time - start_time)
        start_time = end_time

        cv2.putText(frame, f"FPS: {fps:.2f}", FPS_POSITION,
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

        cv2.imshow("Tracking CSRT", frame)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
