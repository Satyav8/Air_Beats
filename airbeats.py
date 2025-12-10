import cv2
import mediapipe as mp
import time
from gesture_detector import get_gesture, detect_swipe, stable_gesture
from spotify_controls import play_pause, next_track, previous_track, volume_up, volume_down
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

load_dotenv()

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# Spotify authentication
sp = Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri="https://example.com/callback"
,
    scope="user-modify-playback-state user-read-playback-state user-read-currently-playing"
))

cap = cv2.VideoCapture(0)

last_action = ""
cooldown_time = 1.0  # seconds
last_action_time = 0


# --------------------- TRACK INFORMATION ---------------------

def get_track_info(sp):
    current = sp.current_user_playing_track()
    if not current:
        return None

    name = current["item"]["name"]
    artist = current["item"]["artists"][0]["name"]

    playback = sp.current_playback()
    volume = playback["device"]["volume_percent"] if playback else 0

    return {
        "name": name,
        "artist": artist,
        "volume": volume
    }


# --------------------- HUD DRAWING ---------------------

def draw_hud(frame, gesture, swipe, track_info):
    h, w, _ = frame.shape

    # Top bar background
    cv2.rectangle(frame, (0, 0), (w, 120), (0, 0, 0), -1)
    cv2.rectangle(frame, (0, 0), (w, 120), (0, 255, 255), 2)

    # Branding
    cv2.putText(frame, "AIRBEATS", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3)

    # Gesture display
    cv2.putText(frame, f"Gesture: {gesture}", (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # Swipe display
    cv2.putText(frame, f"Swipe: {swipe}", (20, 110),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    # Track Info
    if track_info:
        cv2.putText(frame, f"Track: {track_info['name']}", (300, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        cv2.putText(frame, f"Artist: {track_info['artist']}", (300, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)

        cv2.putText(frame, f"Volume: {track_info['volume']}%", (300, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 255), 2)


# --------------------- MAIN LOOP ---------------------

with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7) as hands:
    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        h, w, c = frame.shape

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        raw_gesture = None
        gesture = None
        swipe = None

        if result.multi_hand_landmarks:
            for handLms in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

                raw_gesture = get_gesture(handLms)
                gesture = stable_gesture(raw_gesture)
                swipe = detect_swipe(handLms, w)

        # Cooldown control
        current_time = time.time()
        can_trigger = (current_time - last_action_time) >= cooldown_time

        # --------------------- ACTION MAPPING ---------------------

        if can_trigger:
            if gesture == "PALM" and last_action != "PALM":
                play_pause(sp)
                last_action = "PALM"
                last_action_time = current_time

            elif gesture == "FIST" and last_action != "FIST":
                sp.pause_playback()
                last_action = "FIST"
                last_action_time = current_time

            elif gesture == "POINT" and last_action != "POINT":
                next_track(sp)
                last_action = "POINT"
                last_action_time = current_time

            elif gesture == "TWO_FINGERS" and last_action != "TWO_FINGERS":
                volume_up(sp)
                last_action = "TWO_FINGERS"
                last_action_time = current_time

            # Swipe detection
            if swipe == "SWIPE_RIGHT" and last_action != "SWIPE_RIGHT":
                next_track(sp)
                last_action = "SWIPE_RIGHT"
                last_action_time = current_time

            if swipe == "SWIPE_LEFT" and last_action != "SWIPE_LEFT":
                previous_track(sp)
                last_action = "SWIPE_LEFT"
                last_action_time = current_time

        # Reset gesture lock when hand stops
        if gesture is None and swipe is None:
            last_action = ""

        # Draw the HUD
        track_info = get_track_info(sp)
        draw_hud(frame, gesture, swipe, track_info)

        cv2.imshow("AirBeats - Gesture Control", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()



