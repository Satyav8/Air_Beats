# 🎧 **AirBeats – AI Gesture Controlled Music Player**

Control Spotify **without touching anything** — just with your **hand gestures**.
Powered by **MediaPipe, OpenCV, and Spotify Web API**.

---

## ✨ **Overview**

**AirBeats** transforms your webcam into a futuristic gesture-control interface for Spotify.
Play, pause, skip tracks, adjust volume, and navigate your playlist — all using intuitive hand gestures.

It’s touchless.
It’s smooth.
It’s magical.
And it works in real-time with stunning UI overlays.

---

## 🚀 **Features**

### 🎮 **Gesture Controls**

| Gesture       | Action         |
| ------------- | -------------- |
| ✋ PALM        | Play / Pause   |
| ✊ FIST        | Pause          |
| 👉 POINT      | Next Track     |
| ✌ TWO FINGERS | Volume Up      |
| ↔ SWIPE LEFT  | Previous Track |
| ↔ SWIPE RIGHT | Next Track     |

### 🔥 **Live HUD Overlay**

Displays:

* Current gesture
* Swipe direction
* Track name
* Artist
* Volume
* AirBeats branding bar

### 🧠 **Stabilized AI Gesture Detection**

* Noise reduction
* Multi-frame gesture smoothing
* Swipe motion tracking
* Cooldown-based control to prevent accidental triggers

### 🎶 **Spotify Integration**

* Uses OAuth 2.0
* Full playback permissions
* Real-time device & volume sync

---

## 📁 **Project Structure**

```
AirBeats/
│
├── airbeats.py               # Main application (gesture → Spotify)
├── gesture_detector.py       # Gesture classification + swipe detection + smoothing
├── spotify_controls.py       # Play/pause/next/prev/volume control actions
├── requirements.txt          # Python dependencies
├── .gitignore                # Cleaner repository
├── .env                      # Spotify API credentials (ignored)
└── venv/                     # Virtual environment (ignored)
```

---

## ⚙️ **Installation**

### 1️⃣ Clone the repository

```bash
git clone https://github.com/Satyav8/Air_Beats.git
cd Air_Beats
```

### 2️⃣ Create and activate a virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 **Spotify Setup**

1. Go to: [https://developer.spotify.com/dashboard](https://developer.spotify.com/dashboard)
2. Create an app
3. Add this as your Redirect URI:

```
https://example.com/callback
```

4. Add these permissions:

```
user-modify-playback-state
user-read-playback-state
user-read-currently-playing
```

5. Put your credentials in `.env`:

```
SPOTIPY_CLIENT_ID=your_client_id
SPOTIPY_CLIENT_SECRET=your_client_secret
```

---

## ▶️ **Running AirBeats**

Activate venv and run:

```bash
python airbeats.py
```

**Important:**
Before using gestures, **start any Spotify song manually** on your phone or PC.
Spotify API requires an active device.

---

## 🤖 **How It Works**

AirBeats combines:

### 🟡 MediaPipe Hands

To track finger joints (21 landmarks).

### 🟡 Gesture Detection Logic

Rules to detect palm, fist, point, two-fingers, and swipes.

### 🟡 Stabilization Engine

* Multi-frame history
* Cooldown
* Swipe thresholds
* Action reset logic

### 🟡 Spotify Web API

Maps gestures → playback actions.

### 🟡 Live UI Overlay

Built with OpenCV’s drawing utilities.

---

## 📸 **Preview**

> Add screenshots or GIFs here after your next run.
> I can generate live preview templates if you want.

---

## 🛠️ **Tech Stack**

* Python
* MediaPipe
* OpenCV
* Spotipy
* OAuth 2.0
* NumPy

---

## 🧩 **Future Enhancements**

* Add gesture icons in HUD
* Ripple animation on gesture trigger
* Advanced volume visualization
* Voice confirmation (e.g., “Next Track”)
* Mobile companion app
* Custom training with TensorFlow Lite

If you want any of these features, I can generate them.

---

## ⭐ **Why AirBeats is Awesome**

* Touchless control feels futuristic
* Great showcase of computer vision + AI + music integration
* Perfect project for portfolio, resume, and demos
* Runs in real-time on CPU
* Highly extendable

---

## ❤️ **Contributions**

PRs welcome.
Open issues if you want features added.

---

## 📜 **License**

MIT License.

