import cv2
import mediapipe as mp

# Finger mapping: TIP and DIP joints
TIP = [4, 8, 12, 16, 20]
DIP = [3, 7, 11, 15, 19]

# History buffer for stable gestures
gesture_history = []
MAX_HISTORY = 5

def finger_extended(hand_landmarks, tip, dip):
    """
    Returns True if finger is extended (tip higher than DIP joint)
    """
    return hand_landmarks.landmark[tip].y < hand_landmarks.landmark[dip].y


def get_gesture(hand_landmarks):
    """
    Returns PALM, FIST, POINT, TWO_FINGERS, UNKNOWN
    """
    fingers_up = []

    for t, d in zip(TIP, DIP):
        fingers_up.append(finger_extended(hand_landmarks, t, d))

    total_up = sum(fingers_up)

    if total_up == 5:
        return "PALM"
    elif total_up == 0:
        return "FIST"
    elif fingers_up[1] and not fingers_up[2] and not fingers_up[3] and not fingers_up[4]:
        return "POINT"
    elif fingers_up[1] and fingers_up[2]:
        return "TWO_FINGERS"
    else:
        return "UNKNOWN"


def stable_gesture(new_gesture):
    """
    Smooths gesture by requiring consistency across frames.
    """
    global gesture_history
    gesture_history.append(new_gesture)

    if len(gesture_history) > MAX_HISTORY:
        gesture_history.pop(0)

    if gesture_history.count(new_gesture) >= MAX_HISTORY - 1:
        return new_gesture
    return None


# Swipe detection
prev_x = None

def detect_swipe(hand_landmarks, frame_width, threshold=40):
    """
    Detect SWIPE_LEFT or SWIPE_RIGHT based on wrist movement.
    """
    global prev_x
    x = hand_landmarks.landmark[0].x * frame_width

    if prev_x is None:
        prev_x = x
        return None

    movement = x - prev_x
    prev_x = x

    if movement > threshold:
        return "SWIPE_RIGHT"
    elif movement < -threshold:
        return "SWIPE_LEFT"

    return None


