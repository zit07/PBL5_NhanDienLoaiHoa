import sys
sys.path.append("/Users/haison/Downloads/PBL5/Client")

import tkinter as tk
from tkinter import filedialog
import os
from PIL import Image, ImageTk
from general_method import CREATICONBUTTON
from tkinter import ttk
from general_method import center_window
from Controller.predict_flower import predict_flower
from Controller.global_resources import x, y

class Select_IMG_Form():
    def __init__(self, root, main_app):
        self.root = root
        self.root.title("Chọn ảnh để dự đoán hoa")
        self.main_app = main_app
        center_window(self.root, x, y)
        
        frame_top = ttk.Frame(self.root, style='Custom.TFrame')
        frame_top.pack(side=tk.TOP, fill=tk.X, padx=0)
        # Tạo nút bên trên bên phải
        self.camera_icon = CREATICONBUTTON(frame_top, "camera.png", 15, lambda: self.show_camera_form())
        
        # Tạo nút để chọn ảnh
        self.btn_select_image = tk.Button(frame_top, text="Chọn ảnh", command=self.select_image)
        self.btn_select_image.pack(padx=0)

        self.lbl_file_error = tk.Label(self.root, text="")
        self.lbl_file_error.pack(pady=(2,2))
        
        # Tạo một `Label` để hiển thị hình ảnh đã chọn
        self.img_label = tk.Label(self.root)
        self.img_label.pack()

        frame_bottom = ttk.Frame(self.root, style='Custom.TFrame')
        frame_bottom.pack(side=tk.BOTTOM, fill=tk.X, padx=5)
        # Label hiển thị kết quả dự đoán
        self.lbl_dudoan = tk.Label(frame_bottom, text="", font=("Helvetica", 10))
        self.lbl_dudoan.pack(pady=(2,0))
        self.lbl_result = tk.Label(frame_bottom, text="", font=("Helvetica", 10))
        self.lbl_result.pack(pady=(2,2))
        self.lbl_accuracy = tk.Label(frame_bottom, text="", font=("Helvetica", 10))
        self.lbl_accuracy.pack(pady=(0,4))

    def select_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            kieufile = os.path.splitext(file_path)[1]
            if kieufile in [".jpg", ".jpeg", ".png"]:
                # Hiển thị hình ảnh đã chọn
                self.show_image(file_path)

                # Gửi ảnh đến server và nhận kết quả
                img = Image.open(file_path)
                result, accuracy = predict_flower(img)

                # Hiển thị kết quả dự đoán
                if accuracy != "":
                    self.lbl_dudoan.config(text=f"Dự đoán:")
                    self.lbl_result.config(text=f"{result}")
                    self.lbl_accuracy.config(text=f"Tỉ lệ dự đoán: {round(float(accuracy*100), 1)}%")

            else:
                self.lbl_file_error.config(text="Hãy chọn file ảnh (jpg, png, jpeg)!", fg="red")

    def show_image(self, image_path):
        # Mở hình ảnh và chuyển đổi sang định dạng phù hợp
        img = Image.open(image_path)
        img = img.resize((300, 300), Image.LANCZOS)  # Thay đổi kích thước hình ảnh
        img = ImageTk.PhotoImage(img)

        # Cập nhật hình ảnh trong Label
        self.img_label.configure(image=img)
        self.img_label.image = img  # Giữ một tham chiếu đến hình ảnh để tránh bị hủy bởi garbage collector

    def show_camera_form(self):
        self.main_app.Show_Camera_Form()  # Gọi phương thức show_form_b từ MainApp
        self.root.destroy()  # Ẩn FormA
        
        