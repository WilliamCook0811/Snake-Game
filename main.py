import tkinter as tk
import random

# --- Constants ---
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE
FPS = 100  # Milliseconds per frame

# --- Colors ---
WHITE = "#FFFFFF"
GREEN = "#00FF00"
RED = "#FF0000"
BLACK = "#000000"

# --- Initialize ---
root = tk.Tk()
root.title("Snake Game")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=BLACK)
canvas.pack()

# --- Snake and Apple ---
snake = [(5, 5)]
direction = (1, 0)
apple = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
score = 0

def draw_block(color, pos):
    x1, y1 = pos[0] * CELL_SIZE, pos[1] * CELL_SIZE
    x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
    canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

def move_snake():
    global apple, score, running
    head_x, head_y = snake[0]
    dx, dy = direction
    new_head = (head_x + dx, head_y + dy)

    # Check collisions
    if (new_head in snake or
        not 0 <= new_head[0] < GRID_WIDTH or
        not 0 <= new_head[1] < GRID_HEIGHT):
        running = False
        return

    snake.insert(0, new_head)
    if new_head == apple:
        score += 1
        while apple in snake:
            apple = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    else:
        snake.pop()

def draw():
    canvas.delete("all")
    draw_block(RED, apple)
    for segment in snake:
        draw_block(GREEN, segment)
    canvas.create_text(50, 10, text=f"Score: {score}", fill=WHITE, anchor="nw", font=("Arial", 14))

def game_loop():
    if running:
        move_snake()
        draw()
        root.after(FPS, game_loop)
    else:
        canvas.create_text(WIDTH // 2, HEIGHT // 2, text="Game Over!", fill=WHITE, font=("Arial", 24))

def on_key_press(event):
    global direction
    new_dir = {
        "Up": (0, -1),
        "Down": (0, 1),
        "Left": (-1, 0),
        "Right": (1, 0),
        "w": (0, -1),
        "s": (0, 1),
        "a": (-1, 0),
        "d": (1, 0),
    }.get(event.keysym, direction)

    # Prevent the snake from reversing
    if (new_dir[0] != -direction[0] or new_dir[1] != -direction[1]):
        direction = new_dir

# --- Bindings ---
root.bind("<KeyPress>", on_key_press)

# --- Start Game ---
running = True
draw()
game_loop()
root.mainloop()
