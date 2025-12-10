from spotipy import Spotify

def play_pause(sp):
    current = sp.current_playback()
    if current and current['is_playing']:
        sp.pause_playback()
        print("Paused")
    else:
        sp.start_playback()
        print("Playing")

def next_track(sp):
    sp.next_track()
    print("Next Track")

def previous_track(sp):
    sp.previous_track()
    print("Previous Track")

def volume_up(sp):
    current = sp.current_playback()
    if current:
        vol = min(current["device"]["volume_percent"] + 10, 100)
        sp.volume(vol)
        print("Volume Up:", vol)

def volume_down(sp):
    current = sp.current_playback()
    if current:
        vol = max(current["device"]["volume_percent"] - 10, 0)
        sp.volume(vol)
        print("Volume Down:", vol)
