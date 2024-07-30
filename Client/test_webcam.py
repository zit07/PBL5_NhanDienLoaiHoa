import requests
import cv2
import numpy as np

url = 'http://192.168.93.88:8080/video'

# Sử dụng requests để nhận dữ liệu video
response = requests.get(url, stream=True)

# Kiểm tra trạng thái kết nối
if response.status_code == 200:
    # Xử lý từng chunk dữ liệu nhận được
    bytes = b''
    for chunk in response.iter_content(chunk_size=1024):
        bytes += chunk
        # Kiểm tra đầu của một khung hình JPEG
        a = bytes.find(b'\xff\xd8')
        b = bytes.find(b'\xff\xd9')
        # Nếu tìm thấy cả đầu và đuôi của khung hình JPEG
        if a != -1 and b != -1:
            jpg = bytes[a:b+2]  # Cắt JPEG từ byte stream
            bytes = bytes[b+2:]  # Loại bỏ phần đã xử lý
            frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            if frame is not None:
                cv2.imshow('Frame', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
    cv2.destroyAllWindows()
else:
    print("Không thể kết nối tới camera")
