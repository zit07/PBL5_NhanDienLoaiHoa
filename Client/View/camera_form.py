import sys
sys.path.append("/Users/haison/Downloads/PBL5/Client")
import requests

import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from general_method import center_window
from Controller.global_resources import x, y
from Controller.predict_flower import predict_flower
from general_method import CREATICONBUTTON
from Controller.global_resources import camera_url

class Camera_Form:
    def __init__(self, root, main_app):
        self.root = root
        self.root.title("Nhận diện bằng Camera")
        self.main_app = main_app
        center_window(self.root, x, y)
        
        frame_top = ttk.Frame(self.root, style='Custom.TFrame')
        frame_top.pack(side=tk.TOP, fill=tk.X, padx=0)
        # Tạo nút bên trên bên phải
        self.camera_icon = CREATICONBUTTON(frame_top, "image.png", 15, lambda: self.show_selectIMG_form())
        
        # Tạo cửa sổ hiển thị hình ảnh từ camera
        self.camera_label = tk.Label(root)
        self.camera_label.pack()
        
        self.camera_url = camera_url
        self.bytes = b''
        
        frame_bottom = ttk.Frame(self.root, style='Custom.TFrame')
        frame_bottom.pack(side=tk.BOTTOM, fill=tk.X, padx=5)
        
        # Label hiển thị kết quả dự đoán
        self.lbl_dudoan = tk.Label(frame_bottom, text="", font=("Helvetica", 10))
        self.lbl_dudoan.pack(pady=(2,0))
        self.lbl_result = tk.Label(frame_bottom, text="", font=("Helvetica", 10))
        self.lbl_result.pack(pady=(2,2))
        self.lbl_accuracy = tk.Label(frame_bottom, text="", font=("Helvetica", 10))
        self.lbl_accuracy.pack(pady=(0,4))

    def open_ip_camera(self):
        # Mở luồng video từ IP Camera
        self.stream = requests.get(self.camera_url, stream=True)
        return self.stream.status_code == 200

    def read_ip_camera_frame(self):
        for chunk in self.stream.iter_content(chunk_size=1024):
            self.bytes += chunk
            a = self.bytes.find(b'\xff\xd8')
            b = self.bytes.find(b'\xff\xd9')
            if a != -1 and b != -1:
                jpg = self.bytes[a:b+2]
                self.bytes = self.bytes[b+2:]
                frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                return True, frame
        return False, None
    
    def update_frame(self):
        # Đọc khung hình từ camera
        # ret, frame = self.camera.read()
        ret, frame = self.read_ip_camera_frame()
        
        if ret:
            # Lấy kích thước của khung hình
            height, width = frame.shape[:2]

            # Tính toán vị trí và kích thước của khung ảnh vuông ở giữa
            square_size = min(height, width)
            x = (width - square_size) // 2
            y = (height - square_size) // 2
            
            # Cắt khung ảnh vuông ở giữa
            square_frame = frame[y:y+square_size, x:x+square_size]

            # Resize khung ảnh thành kích thước mới là 180x180
            resized_img = cv2.resize(square_frame, (300, 300))

            # Chuyển đổi khung ảnh thành định dạng RGB và tạo đối tượng Image
            img = Image.fromarray(cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB))

            # Hiển thị khung hình trên giao diện
            img_tk = ImageTk.PhotoImage(img)
            self.camera_label.configure(image=img_tk)
            self.camera_label.image = img_tk
            
            # Gọi hàm predict_flower với đối tượng Image
            result, accuracy = predict_flower(img)

            # Hiển thị kết quả dự đoán
            if accuracy != "":
                self.lbl_dudoan.config(text=f"Dự đoán:")
                self.lbl_result.config(text=f"{result}")
                self.lbl_accuracy.config(text=f"Tỉ lệ dự đoán: {round(float(accuracy*100), 1)}%")

            # Lặp lại việc cập nhật khung hình
            self.camera_label.after(1, self.update_frame)

    def show_selectIMG_form(self):
        self.main_app.Show_form_selectIMG()  # Gọi phương thức show_form_b từ MainApp
        self.root.destroy()  # Ẩn FormA
        
        
# def main():
#     # Tạo một cửa sổ gốc của Tkinter
#     root = tk.Tk()
    
#     # Điều chỉnh kích thước cửa sổ nếu cần
#     root.geometry("800x600")  # Ví dụ, cửa sổ có kích thước 800x600
    
#     # Khởi tạo đối tượng của Camera_Form
#     app = Camera_Form(root, main_app=None)  # Giả sử không có main_app phức tạp

#     # Khởi động luồng IP camera
#     if app.open_ip_camera():
#         print("Camera is streaming.")
#         # Bắt đầu cập nhật khung hình từ camera
#         app.update_frame()
#     else:
#         print("Failed to connect to the camera.")

#     # Chạy vòng lặp chính của Tkinter
#     root.mainloop()

# # Gọi hàm main
# if __name__ == "__main__":
#     main()
