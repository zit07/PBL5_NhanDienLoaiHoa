import requests
from Controller.global_resources import url_server
import io

def predict_flower(image):
    try:
        # Chuyển đổi hình ảnh thành dữ liệu nhị phân
        with io.BytesIO() as output:
            image.save(output, format='JPEG')
            image_data = output.getvalue()

        files = {'image': image_data}  # Dữ liệu hình ảnh là dạng bytes
        response = requests.post(url_server, files=files)  # Gửi POST request với hình ảnh

        if response.status_code == 200:
            result = response.json()  # Nhận kết quả từ server
            if float(result['accuracy']) >= 0.7:
                return result['flower'], result['accuracy']
            else:
                return "Không nhận diện được", ""
        else:
            print(response.status_code)
            return "Lỗi trong quá trình dự đoán", ""
    except Exception as e:
        print("Lỗi trong quá trình dự đoán:", e)
        return "Lỗi trong quá trình dự đoán"
