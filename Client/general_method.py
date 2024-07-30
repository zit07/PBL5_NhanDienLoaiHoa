import sys
sys.path.append("/Users/haison/Downloads/PBL5/Client")

import tkinter as tk
from tkinter import PhotoImage
from Controller.global_resources import directoryIMG_icon
# import re

def CREATICONBUTTON(frame, image_name, size, command):
    icon = PhotoImage(file=directoryIMG_icon + image_name).subsample(size, size)
    icon_label = tk.Label(frame, image=icon)
    icon_label.bind("<Button-1>", lambda event, cmd=command: cmd())
    icon_label.pack(side=tk.RIGHT, padx=0)
    return icon

def center_window(root, width, height):
    # Lấy kích thước màn hình
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Tính toán vị trí của cửa sổ
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        # Đặt vị trí cửa sổ
        root.geometry(f"{width}x{height}+{x}+{y}")