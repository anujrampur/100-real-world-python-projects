# Project 88: Convolutional Image Filter & Edge Detector
# 100 Real-World Python Projects - Anuj Kumar Saxena
import tkinter as tk

# 5x5 Synthetic pixel image matrix (0 = dark, 255 = light)
SAMPLE_IMAGE = [
    [10, 10, 255, 255, 255],
    [10, 10, 255, 255, 255],
    [10, 10, 255, 255, 255],
    [10, 10, 255, 255, 255],
    [10, 10, 255, 255, 255],
]
# 3x3 Vertical Sobel Kernel
SOBEL_VERTICAL = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]


def convolve_2d(matrix, kernel):
    h = len(matrix)
    w = len(matrix[0])
    output = [[0] * (w - 2) for _ in range(h - 2)]
    for r in range(1, h - 1):
        for c in range(1, w - 1):
            val = 0
            for kr in range(-1, 2):
                for kc in range(-1, 2):
                    val += matrix[r + kr][c + kc] * kernel[kr + 1][kc + 1]
            output[r - 1][c - 1] = max(0, min(255, abs(val)))
    return output


root = tk.Tk()
root.title("2D Matrix Convolution Engine")
root.geometry("480x320")
tk.Label(
    root,
    text="2D DISCRETE CONVOLUTION FILTER",
    font=("Arial", 14, "bold"),
    fg="#1e3a8a",
).pack(pady=12)
conv_res = convolve_2d(SAMPLE_IMAGE, SOBEL_VERTICAL)
report = "Input Matrix (Step Edge):\n"
for row in SAMPLE_IMAGE:
    report += f"{row}\n"
report += "\nConvolved Feature Output (Vertical Edge Detected):\n"
for row in conv_res:
    report += f"{row}\n"
txt = tk.Text(root, height=10, width=54, font=("Consolas", 9), bg="#f8fafc")
txt.pack(padx=20, pady=10)
txt.insert(tk.END, report)
txt.config(state="disabled")
root.mainloop()
