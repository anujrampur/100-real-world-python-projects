# Project 19: Classic 2D Snake
# 100 Real-World Python Projects - Anuj Kumar Saxena
import tkinter as tk
import random

WIDTH = 400
HEIGHT = 400
GRID_SIZE = 20
SPEED = 120
snake = [(100, 100), (80, 100), (60, 100)]
direction = "Right"
food = None
score = 0
game_running = True


def spawn_food():
    global food
    while True:
        x = random.randint(0, (WIDTH // GRID_SIZE) - 1) * GRID_SIZE
        y = random.randint(0, (HEIGHT // GRID_SIZE) - 1) * GRID_SIZE
        if (x, y) not in snake:
            food = (x, y)
            break


def change_direction(new_dir):
    global direction
    opposites = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
    if new_dir != opposites.get(direction):
        direction = new_dir


def game_loop():
    global snake, food, score, game_running
    if not game_running:
        return
    head_x, head_y = snake[0]
    if direction == "Up":
        head_y -= GRID_SIZE
    elif direction == "Down":
        head_y += GRID_SIZE
    elif direction == "Left":
        head_x -= GRID_SIZE
    elif direction == "Right":
        head_x += GRID_SIZE
    new_head = (head_x, head_y)
    # Collision with walls or self
    if (
        head_x < 0
        or head_x >= WIDTH
        or head_y < 0
        or head_y >= HEIGHT
        or new_head in snake
    ):
        canvas.create_text(
            WIDTH // 2,
            HEIGHT // 2,
            text="GAME OVER",
            fill="red",
            font=("Arial", 22, "bold"),
        )
        game_running = False
        return
    snake.insert(0, new_head)
    if new_head == food:
        score += 10
        score_label.config(text=f"Score: {score}")
        spawn_food()
    else:
        snake.pop()
    # Draw elements
    canvas.delete("all")
    canvas.create_oval(
        food[0],
        food[1],
        food[0] + GRID_SIZE,
        food[1] + GRID_SIZE,
        fill="red",
        outline="",
    )
    for i, (x, y) in enumerate(snake):
        color = "#15803d" if i == 0 else "#22c55e"
        canvas.create_rectangle(
            x, y, x + GRID_SIZE, y + GRID_SIZE, fill=color, outline=""
        )
    root.after(SPEED, game_loop)


root = tk.Tk()
root.title("Classic 2D Snake")
root.resizable(False, False)
score_label = tk.Label(root, text="Score: 0", font=("Arial", 12, "bold"))
score_label.pack(pady=5)
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#0f172a")
canvas.pack()
root.bind("<Up>", lambda e: change_direction("Up"))
root.bind("<Down>", lambda e: change_direction("Down"))
root.bind("<Left>", lambda e: change_direction("Left"))
root.bind("<Right>", lambda e: change_direction("Right"))
spawn_food()
game_loop()
root.mainloop()
