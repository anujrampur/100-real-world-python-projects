# Project 60: Virtual Piano & Audio Synthesizer
# 100 Real-World Python Projects - Anuj Kumar Saxena
import tkinter as tk
import math
import struct
import wave
import io
import os
import subprocess
import platform

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


def generate_tone_wav(freq, duration=0.3, sample_rate=22050):
    num_samples = int(duration * sample_rate)
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wav:
        wav.setnchannels(1)  # Mono
        wav.setsampwidth(2)  # 16-bit
        wav.setframerate(sample_rate)
        for i in range(num_samples):
            # Sine wave formula
            t = float(i) / sample_rate
            sample = math.sin(2.0 * math.pi * freq * t)
            # Apply decay envelope
            envelope = max(0.0, 1.0 - (i / num_samples))
            packed = struct.pack("<h", int(sample * envelope * 32767))
            wav.writeframes(packed)
    return buf.getvalue()


class VirtualPiano(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Virtual Piano Synthesizer")
        self.geometry("540x280")
        self.resizable(False, False)
        self.configure(bg="#0f172a")
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
        self.status.config(text=f"Playing Note: {note} ({freq:.1f} Hz)")
        audio_bytes = generate_tone_wav(freq)
        # Audio playback using native OS sound systems
        if platform.system().lower() == "windows":
            try:
                import winsound

                winsound.PlaySound(
                    audio_bytes, winsound.SND_MEMORY | winsound.SND_ASYNC
                )
            except Exception:
                pass
        else:
            # Fallback bell on POSIX systems if audio devices are unconfigured
            self.bell()


if __name__ == "__main__":
    app = VirtualPiano()
    app.mainloop()
