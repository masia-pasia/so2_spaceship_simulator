import tkinter as tk
import random
import threading
import time


class MapGenerator:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=50 * cols, height=50 * rows)
        self.canvas.pack()
        self.cells = [[None for _ in range(cols)] for _ in range(rows)]
        self.actor1_pos = [0, random.randint(0, cols - 1)]
        self.actor2_pos = [random.randint(0, rows - 1), random.randint(0, cols - 1)]
        self.actor3_pos = [0, random.randint(0, cols - 1)]

        self.root.bind("<Up>", self.move_actor2_up)
        self.root.bind("<Down>", self.move_actor2_down)
        self.root.bind("<Left>", self.move_actor2_left)
        self.root.bind("<Right>", self.move_actor2_right)
        self.root.focus_set()

        self.draw_map()
        self.start_threads()
        self.root.mainloop()

    def draw_map(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j] = self.canvas.create_rectangle(
                    50 * j, 50 * i, 50 * (j + 1), 50 * (i + 1), fill="white", outline="black"
                )
        self.cells[self.actor1_pos[0]][self.actor1_pos[1]] = self.canvas.create_text(
            50 * self.actor1_pos[1] + 25, 50 * self.actor1_pos[0] + 25, text="A1", fill="red"
        )
        self.cells[self.actor2_pos[0]][self.actor2_pos[1]] = self.canvas.create_text(
            50 * self.actor2_pos[1] + 25, 50 * self.actor2_pos[0] + 25, text="A2", fill="blue"
        )
        self.cells[self.actor3_pos[0]][self.actor3_pos[1]] = self.canvas.create_text(
            50 * self.actor3_pos[1] + 25, 50 * self.actor3_pos[0] + 25, text="A3", fill="green"
        )

    def start_threads(self):
        thread1 = threading.Thread(target=self.move_actor1)
        thread1.start()
        time.sleep(2)
        thread2 = threading.Thread(target=self.move_actor3)
        thread2.start()

    def move_actor1(self):
        while self.actor1_pos[0] < self.rows - 1:
            time.sleep(1)
            self.canvas.delete(self.cells[self.actor1_pos[0]][self.actor1_pos[1]])
            self.actor1_pos[0] += 1
            self.cells[self.actor1_pos[0]][self.actor1_pos[1]] = self.canvas.create_text(
                50 * self.actor1_pos[1] + 25, 50 * self.actor1_pos[0] + 25, text="A1", fill="red"
            )

    def move_actor2_up(self, event):
        if self.actor2_pos[0] > 0:
            self.canvas.delete(self.cells[self.actor2_pos[0]][self.actor2_pos[1]])
            self.actor2_pos[0] -= 1
            self.cells[self.actor2_pos[0]][self.actor2_pos[1]] = self.canvas.create_text(
                50 * self.actor2_pos[1] + 25, 50 * self.actor2_pos[0] + 25, text="A2", fill="blue"
            )

    def move_actor2_down(self, event):
        if self.actor2_pos[0] < self.rows - 1:
            self.canvas.delete(self.cells[self.actor2_pos[0]][self.actor2_pos[1]])
            self.actor2_pos[0] += 1
            self.cells[self.actor2_pos[0]][self.actor2_pos[1]] = self.canvas.create_text(
                50 * self.actor2_pos[1] + 25, 50 * self.actor2_pos[0] + 25, text="A2", fill="blue"
            )


    def move_actor2_left(self, event):
        if self.actor2_pos[1] > 0:
            self.canvas.delete(self.cells[self.actor2_pos[0]][self.actor2_pos[1]])
            self.actor2_pos[1] -= 1
            self.cells[self.actor2_pos[0]][self.actor2_pos[1]] = self.canvas.create_text(
                50 * self.actor2_pos[1] + 25, 50 * self.actor2_pos[0] + 25, text="A2", fill="blue"
            )


    def move_actor2_right(self, event):
        if self.actor2_pos[1] < self.cols - 1:
            self.canvas.delete(self.cells[self.actor2_pos[0]][self.actor2_pos[1]])
            self.actor2_pos[1] += 1
            self.cells[self.actor2_pos[0]][self.actor2_pos[1]] = self.canvas.create_text(
                50 * self.actor2_pos[1] + 25, 50 * self.actor2_pos[0] + 25, text="A2", fill="blue"
            )


    def move_actor3(self):
        while self.actor3_pos[0] < self.rows - 1:
            time.sleep(1)
            self.canvas.delete(self.cells[self.actor3_pos[0]][self.actor3_pos[1]])
            self.actor3_pos[0] += 1
            self.cells[self.actor3_pos[0]][self.actor3_pos[1]] = self.canvas.create_text(
                50 * self.actor3_pos[1] + 25, 50 * self.actor3_pos[0] + 25, text="A3", fill="green"
            )

MapGenerator(10,10)
