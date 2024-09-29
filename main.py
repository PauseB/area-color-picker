import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import colorsys
import clipboard

class ImageAnalyzer:
    def __init__(self, master):
        self.master = master
        self.master.title("이미지 색상 분석기")
        self.rect = None
        self.start_x = self.start_y = None

        self.canvas = tk.Canvas(master)
        self.canvas.pack()

        self.load_button = tk.Button(master, text="이미지 로드", command=self.load_image)
        self.load_button.pack()

        self.image = None
        self.tk_image = None

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            original_image = Image.open(file_path)
            
            max_size = (800, 800)
            original_image.thumbnail(max_size, Image.LANCZOS) 
            
            self.image = original_image
            self.tk_image = ImageTk.PhotoImage(self.image)

            self.canvas.config(width=self.image.width, height=self.image.height)

            self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)

            self.canvas.bind("<ButtonPress-1>", self.on_button_press)
            self.canvas.bind("<B1-Motion>", self.on_move_press)
            self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red")

    def on_move_press(self, event):
        cur_x, cur_y = (event.x, event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        x1, y1, x2, y2 = self.canvas.coords(self.rect)
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        region = self.image.crop((x1, y1, x2, y2))

        pixels = np.array(region)
        avg_color = pixels.mean(axis=(0, 1))  # (R, G, B)

        r, g, b = avg_color / 255  # [0, 1]
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        h = round(h * 360)  # H: [0, 360]
        s = round(s * 100)  # S: [0, 100]
        l = round(l * 100)  # L: [0, 100]


        print(f"선택된 영역의 평균 HSL: ({h}, {s}%, {l}%)")
        clipboard.copy(f"{h}, {s}%, {l}%")


root = tk.Tk()
app = ImageAnalyzer(root)
root.mainloop()
