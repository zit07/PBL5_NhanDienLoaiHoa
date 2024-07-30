import sys
sys.path.append("/Users/haison/Downloads/PBL5/Client")

import tkinter as tk
from select_img_form import Select_IMG_Form
from camera_form import Camera_Form
from general_method import center_window
from Controller.global_resources import x, y

class MainForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Nhận biết tên loài hoa")
        center_window(root, x, y)
        
        self.current_form = None  # Form hiện tại
        
        # Khởi tạo Form Select Image là form hiện tại
        self.Show_Camera_Form()
        
    def Show_form_selectIMG(self):
        self.current_form = Select_IMG_Form(tk.Toplevel(), self)
        self.current_form.root.protocol("WM_DELETE_WINDOW", self.destroy_main_window)  # Xử lý sự kiện khi đóng cửa sổ
        self.root.withdraw()  # Ẩn cửa sổ của MainApp
        
    def Show_Camera_Form(self):
        self.current_form = Camera_Form(tk.Toplevel(), self)
        self.current_form.root.protocol("WM_DELETE_WINDOW", self.destroy_main_window)  # Xử lý sự kiện khi đóng cửa sổ
        self.root.withdraw()  # Ẩn cửa sổ của MainApp
        # self.current_form.update_frame()
        if self.current_form.open_ip_camera():
            print("Camera is streaming.")
            self.current_form.update_frame()
        else:
            print("Failed to connect to the camera.")
    
    def destroy_main_window(self):
        self.current_form = None 
        self.root.destroy()  # Hiển thị cửa sổ của MainApp
        
if __name__ == "__main__":
    root = tk.Tk()
    mainform = MainForm(root)
    root.mainloop()
