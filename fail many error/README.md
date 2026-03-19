# Sign Language Detection (Python 3.13.9)

A simple sign language detection pipeline using **MediaPipe Hands** for landmark extraction and **scikit-learn** for classification.

This repository follows the workflow demonstrated in the video: *"Sign language detection with Python and Scikit Learn | Landmark detection | Computer vision tutorial"*.

## 🧩 What’s Included

- `collect_data.py` — Capture hand landmarks from your webcam and label them.
- `train_model.py` — Train a scikit-learn model on collected landmark data.
- `predict.py` — Run live sign detection from your webcam.

## ✅ Setup (Python 3.13.9)

1. Create a virtual environment (recommended):

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## 🏃‍♀️ Workflow

1. **Collect training data:**
   - Run `python collect_data.py`
   - Press `SPACE` to capture a sample (it will record the current hand landmarks with the label you enter).
   - Press `q` to quit.

2. **Train:**
   - Run `python train_model.py`
   - This will produce `model.pkl`.

3. **Predict live:**
   - Run `python predict.py`
   - It will show live predictions on your webcam feed.

## ⚠️ Notes

- You need a clear hand in view of the webcam to get good landmarks.
- `mediapipe` expects a reasonably well-lit scene.
- You can extend this pipeline with more classes, data augmentation, or a different ML model.
