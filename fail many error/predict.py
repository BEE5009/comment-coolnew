"""Live sign language prediction using a trained model.

Usage:
    python predict.py

This script loads `model.pkl` and uses the webcam to classify the current hand pose.
"""

import pathlib
import sys

try:
    import cv2
    import joblib
    import mediapipe as mp
except ModuleNotFoundError as e:
    print(f"ERROR: Missing dependency: {e.name}")
    print("Install required packages with: python -m pip install -r requirements.txt")
    sys.exit(1)


MODEL_PATH = pathlib.Path(__file__).resolve().parent / "model.pkl"


def get_landmark_vector(landmarks):
    return [coord for lm in landmarks for coord in (lm.x, lm.y, lm.z)]


def main():
    if not MODEL_PATH.exists():
        print(f"Missing model file: {MODEL_PATH}. Run train_model.py first.")
        return 1

    model = joblib.load(MODEL_PATH)

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

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        label = "(no hand)"
        if result.multi_hand_landmarks:
            landmarks = result.multi_hand_landmarks[0].landmark
            vec = get_landmark_vector(landmarks)
            pred = model.predict([vec])[0]
            label = str(pred)
            mp.solutions.drawing_utils.draw_landmarks(
                frame, result.multi_hand_landmarks[0], mp_hands.HAND_CONNECTIONS
            )

        cv2.putText(
            frame,
            f"Prediction: {label}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 255, 0),
            2,
        )

        cv2.putText(
            frame,
            "Press Q to quit",
            (10, frame.shape[0] - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1,
        )

        cv2.imshow("Sign Prediction", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    return 0


if __name__ == "__main__":
    sys.exit(main())
