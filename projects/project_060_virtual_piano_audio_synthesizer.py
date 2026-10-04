import io
import math
import os
import platform
import shutil
import struct
import subprocess
import tempfile
import threading
import tkinter as tk
import wave

# Musical notes frequencies (Middle C Octave)
NOTES = {
    "C": 261.63,
    "D": 293.66,
    "E": 329.63,
    "F": 349.23,
    "G": 392.00,
    "A": 440.00,
    "B": 493.88,
}
SYSTEM = platform.system()
WAV_FILES = {}  # note -> temporary .wav file (macOS / Linux players)


def generate_tone_wav(freq, duration=0.5, sample_rate=22050):
    """Build a WAV file in memory: a sine wave that fades out."""
    num_samples = int(duration * sample_rate)
    frames = bytearray()
    for i in range(num_samples):
        t = i / sample_rate
        sample = math.sin(2.0 * math.pi * freq * t)  # sine wave
        envelope = 1.0 - (i / num_samples)  # decay: loud -> silent
        frames += struct.pack("<h", int(sample * envelope * 30000))
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wav:
        wav.setnchannels(1)  # mono
        wav.setsampwidth(2)  # 16-bit
        wav.setframerate(sample_rate)
        wav.writeframes(bytes(frames))
    return buf.getvalue()


def play_sound(note, audio_bytes):
    """Play WAV data. Returns True if a sound player was available."""
    if SYSTEM == "Windows":
        import winsound

        # SND_MEMORY cannot be combined with SND_ASYNC (Python raises an
        # error), so the sound is played in a background thread instead.
        threading.Thread(
            target=winsound.PlaySound,
            args=(audio_bytes, winsound.SND_MEMORY),
            daemon=True,
        ).start()
        return True
    player = (
        shutil.which("afplay")  # macOS
        or shutil.which("paplay")  # Linux (PulseAudio)
        or shutil.which("aplay")  # Linux (ALSA)
    )
    if player is None:
        return False
    path = WAV_FILES.get(note)
    if path is None:
        path = os.path.join(tempfile.gettempdir(), f"piano_{note}.wav")
        with open(path, "wb") as f:
            f.write(audio_bytes)
        WAV_FILES[note] = path
    subprocess.Popen(
        [player, path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    return True


class VirtualPiano(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Virtual Piano Synthesizer")
        self.geometry("540x280")
        self.resizable(False, False)
        self.configure(bg="#0f172a")
        # Generate every note once, so a key press responds instantly
        self.sounds = {n: generate_tone_wav(f) for n, f in NOTES.items()}
        tk.Label(
            self,
            text="VIRTUAL PIANO SYNTHESIZER",
            font=("Arial", 16, "bold"),
            fg="#38bdf8",
            bg="#0f172a",
        ).pack(pady=15)
        self.status = tk.Label(
            self,
            text="Press piano keys below or use keyboard (A, S, D, F, G, H, J)",
            font=("Arial", 9),
            fg="#94a3b8",
            bg="#0f172a",
        )
        self.status.pack(pady=2)
        keys_frame = tk.Frame(self, bg="#0f172a")
        keys_frame.pack(pady=20)
        self.key_buttons = {}
        bindings = ["a", "s", "d", "f", "g", "h", "j"]
        for i, (note, freq) in enumerate(NOTES.items()):
            k_char = bindings[i]
            btn = tk.Button(
                keys_frame,
                text=f"{note}\n({k_char.upper()})",
                font=("Arial", 11, "bold"),
                width=6,
                height=6,
                bg="#ffffff",
                fg="#0f172a",
                relief="raised",
                command=lambda n=note, f=freq: self.play_note(n, f),
            )
            btn.pack(side="left", padx=3)
            self.key_buttons[k_char] = (btn, note, freq)
            self.bind(k_char, lambda e, n=note, f=freq: self.play_note(n, f))

    def play_note(self, note, freq):
        try:
            played = play_sound(note, self.sounds[note])
        except Exception:
            played = False
        if played:
            self.status.config(text=f"Playing Note: {note} ({freq:.1f} Hz)")
        else:
            self.bell()
            self.status.config(
                text=f"No audio player found - bell only (note {note})"
            )


if __name__ == "__main__":
    app = VirtualPiano()
    app.mainloop()
