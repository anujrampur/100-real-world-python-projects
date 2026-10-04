# Project 83: K-Means Unsupervised Clustering Engine
# 100 Real-World Python Projects - Anuj Kumar Saxena
import random
import math
import tkinter as tk


class KMeans:
    def __init__(self, k=3, max_iter=20):
        self.k = k
        self.max_iter = max_iter
        self.centroids = []
        self.clusters = {}

    def fit(self, points):
        # Initialize random centroids from observed data
        self.centroids = random.sample(points, self.k)
        for _ in range(self.max_iter):
            self.clusters = {i: [] for i in range(self.k)}
            # Assign points to nearest centroid
            for p in points:
                dists = [math.dist(p, c) for c in self.centroids]
                closest = dists.index(min(dists))
                self.clusters[closest].append(p)
            # Recompute centroids as mean of cluster members
            new_centroids = []
            for i in range(self.k):
                members = self.clusters[i]
                if members:
                    mean_x = sum(pt[0] for pt in members) / len(members)
                    mean_y = sum(pt[1] for pt in members) / len(members)
                    new_centroids.append((mean_x, mean_y))
                else:
                    new_centroids.append(self.centroids[i])
            if new_centroids == self.centroids:
                break  # Converged
            self.centroids = new_centroids


class KMeansApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("K-Means Clustering Visualizer")
        self.geometry("540x440")
        self.points = (
            [
                (random.randint(40, 180), random.randint(40, 180))
                for _ in range(15)
            ]
            + [
                (random.randint(280, 460), random.randint(40, 180))
                for _ in range(15)
            ]
            + [
                (random.randint(150, 350), random.randint(220, 340))
                for _ in range(15)
            ]
        )
        self.colors = ["#ef4444", "#3b82f6", "#10b981"]
        ctrl_f = tk.Frame(self)
        ctrl_f.pack(pady=8)
        tk.Button(
            ctrl_f,
            text="Run K-Means (K=3)",
            command=self.cluster_and_draw,
            bg="#2563eb",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=10,
        ).pack()
        self.canvas = tk.Canvas(self, bg="#ffffff")
        self.canvas.pack(fill="both", expand=True, padx=20, pady=10)
        self.cluster_and_draw()

    def cluster_and_draw(self):
        self.canvas.delete("all")
        kmeans = KMeans(k=3)
        kmeans.fit(self.points)
        # Draw clustered data points
        for i, pts in kmeans.clusters.items():
            col = self.colors[i % len(self.colors)]
            for x, y in pts:
                self.canvas.create_oval(
                    x - 4, y - 4, x + 4, y + 4, fill=col, outline=""
                )
        # Draw centroids as stars/large diamonds
        for i, (cx, cy) in enumerate(kmeans.centroids):
            self.canvas.create_rectangle(
                cx - 7,
                cy - 7,
                cx + 7,
                cy + 7,
                fill="#f59e0b",
                outline="black",
                width=2,
            )
            self.canvas.create_text(
                cx, cy - 14, text=f"C{i+1}", font=("Arial", 9, "bold")
            )


if __name__ == "__main__":
    app = KMeansApp()
    app.mainloop()
