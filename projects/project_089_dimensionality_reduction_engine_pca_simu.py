# Project 89: Dimensionality Reduction Engine (PCA Simulation)
# 100 Real-World Python Projects - Anuj Kumar Saxena
import tkinter as tk

# 2D Correlated data points (Feature 1, Feature 2)
DATA_POINTS = [(1.0, 1.2), (2.0, 1.9), (3.0, 3.2), (4.0, 3.8), (5.0, 5.1)]


def center_data(points):
    mean_x = sum(p[0] for p in points) / len(points)
    mean_y = sum(p[1] for p in points) / len(points)
    return [(p[0] - mean_x, p[1] - mean_y) for p in points], (mean_x, mean_y)


def project_1d(centered_points):
    # Principal direction vector approx (1.0, 1.0) normalized
    mag = (1.0**2 + 1.0**2) ** 0.5
    u = (1.0 / mag, 1.0 / mag)
    # Scalar projection: dot product
    return [p[0] * u[0] + p[1] * u[1] for p in centered_points]


centered, means = center_data(DATA_POINTS)
projections = project_1d(centered)
root = tk.Tk()
root.title("Dimensionality Reducer")
root.geometry("480x300")
tk.Label(
    root,
    text="PRINCIPAL COMPONENT REDUCTION (2D -> 1D)",
    font=("Arial", 13, "bold"),
    fg="#1e3a8a",
).pack(pady=12)
txt = tk.Text(root, height=8, width=54, font=("Consolas", 9), bg="#f8fafc")
txt.pack(padx=20, pady=10)
txt.insert(tk.END, f"Feature Means: X={means[0]:.2f}, Y={means[1]:.2f}\n\n")
txt.insert(tk.END, "Original 2D Points -> 1D Compressed Scalar:\n")
for i, p in enumerate(DATA_POINTS):
    txt.insert(tk.END, f"Point {p} -> {projections[i]:.3f}\n")
txt.config(state="disabled")
root.mainloop()
