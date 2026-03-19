"""Collect hand landmark data for sign language classification.

Usage:
    python collect_data.py

Controls:
    - Type a label (e.g., "A", "B", "Hello") and press Enter.
    - Press SPACE to save the current landmark vector for that label.
    - Press BACKSPACE to clear the current label.
    - Press Q to quit.

Output:
    data.csv - CSV file with: label, x1,y1,z1, ..., x21,y21,z21
"""

import csv
import pathlib
import sys

try:
    import cv2
    import mediapipe as mp
    from mediapipe.tasks import python as mp_tasks
    from mediapipe.tasks.python import vision as mp_vision
except ModuleNotFoundError as e:
    print(f"ERROR: Missing dependency: {e.name}")
    print("Install required packages with: python -m pip install -r requirements.txt")
    sys.exit(1)


DATA_PATH = pathlib.Path(__file__).resolve().parent / "data.csv"


def get_landmark_vector(landmarks):
    # Flatten the 21 landmarks (x, y, z) into a single list.
    return [coord for lm in landmarks for coord in (lm.x, lm.y, lm.z)]


def main():
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.75,
        min_tracking_confidence=0.75,
    )

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("ERROR: Unable to open webcam")
        return 1

    label = ""
    print("Type a label, then press ENTER. Press Q to quit.")

    # Ensure header exists.
    if not DATA_PATH.exists():
        with DATA_PATH.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            header = ["label"] + [f"f{i}" for i in range(21 * 3)]
            writer.writerow(header)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
                )

        display_label = label or "(no label)"
        cv2.putText(
            frame,
            f"Label: {display_label}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2,
        )

        cv2.putText(
            frame,
            "SPACE = add sample, BACKSPACE = clear label, Q = quit",
            (10, frame.shape[0] - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1,
        )

        cv2.imshow("Collect Sign Data", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break
        if key == 8:  # BACKSPACE
            label = ""
        if key == ord(" "):
            if not label:
                print("No label set. Type a label and press ENTER.")
            elif not result.multi_hand_landmarks:
                print("No hand detected. Make sure your hand is visible.")
            else:
                landmarks = result.multi_hand_landmarks[0].landmark
                row = [label] + get_landmark_vector(landmarks)
                with DATA_PATH.open("a", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(row)
                print(f"Appended sample for label={label} (total now: {DATA_PATH.stat().st_size} bytes)")

        if key == 13:  # ENTER
            label = input("Label: ").strip()

    cap.release()
    cv2.destroyAllWindows()
    return 0


if __name__ == "__main__":
    sys.exit(main())
