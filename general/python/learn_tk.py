import tkinter as tk
import os
import random


WIDTH = 600
HEIGHT = 600

ROOT = tk.Tk()
ROOT.title("Learn Tkinter")

# screen_center_x = int(ROOT.winfo_screenwidth() * 0.1)
# screen_center_y = int(ROOT.winfo_screenheight() * 0.1)


"""Class representing a ball on the screen, with a position and (per-frame) velocity """


class ball:
    def __init__(self, radius=10, position=None, velocity=None):
        if position == None:
            # set self.position to be the middle of the screen
            self.position = (WIDTH / 2, HEIGHT / 2)
        if velocity == None:
            # set (reasonable) random velocity
            self.velocity = (
                random.randint(1, WIDTH // 10),
                random.randint(1, HEIGHT // 10),
            )
            pass
        else:
            self.velocity = velocity
            self.position = position
            self.radius = radius

    def update(self):
        # update position based on velocity
        x_out_of_bounds = (self.position[0] + self.velocity[0] > WIDTH) or (
            self.position[0] + self.velocity[0] < 0
        )
        y_out_of_bounds = (self.position[1] + self.velocity[1] > HEIGHT) or (
            self.position[1] + self.velocity[1] < 0
        )
        if x_out_of_bounds:
            self.position[0] = 2 * WIDTH - self.position[0] - self.velocity[0]
            self.velocity = (-self.velocity[0], self.velocity[1])
        if y_out_of_bounds:
            self.position[1] = 2 * HEIGHT - self.position[1] - self.velocity[1]
            self.velocity = (self.velocity[0], -self.velocity[1])
        else:
            self.position = (
                self.position[0] + self.velocity[0],
                self.position[1] + self.velocity[1],
            )

    def draw(self):
        # draw the ball on the canvas
        central_canvas.create_oval(
            self.position[0] - self.radius,
            self.position[1] - self.radius,
            self.position[0] + self.radius,
            self.position[1] + self.radius,
            fill="white",
        )
        pass


ROOT.geometry(f"{WIDTH}x{HEIGHT}")
ROOT.resizable(False, False)

# entry_message = tk.Label(
#     WINDOW,
#     text=f"Hello {os.getlogin().capitalize()}!\nWelcome to my Tkinter tutorial!",
#     font=("fira code", 30),
# )
# entry_message.pack(side="left", fill="x", pady=20)


central_canvas = tk.Canvas(ROOT, width=WIDTH * 0.5, height=HEIGHT * 0.5, bg="purple")
central_canvas.grid(row=1, column=2, padx=10, pady=10)


ROOT.bind("<Escape>", lambda e: print("wagwan bruv, why you tryna leave?"))

my_ball = ball()

my_ball.after(100, my_ball.update)
my_ball.after(0, my_ball.draw)
my_ball.after(100, my_ball.update)
my_ball.after(0, my_ball.draw)
my_ball.after(100, my_ball.update)
my_ball.after(0, my_ball.draw)
my_ball.after(100, my_ball.update)
my_ball.after(0, my_ball.draw)
my_ball.after(100, my_ball.update)
my_ball.after(0, my_ball.draw)
my_ball.after(100, my_ball.update)
my_ball.after(0, my_ball.draw)
my_ball.after(100, my_ball.update)
my_ball.after(0, my_ball.draw)


ROOT.mainloop()
