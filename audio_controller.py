import subprocess

volume_levels = [100, 150, 200]
current_index = 0
is_paused = False

def toggle_volume_mode():
    global current_index
    current_index = (current_index + 1) % len(volume_levels)
    print(f"🔊 Volume set to: {volume_levels[current_index]}%")

def pause_or_resume_speech():
    # Simple logic placeholder; implement with espeak/ng if using threads
    print("⏯️ Pause/Play is a placeholder - can integrate with espeak-ng if threaded")
