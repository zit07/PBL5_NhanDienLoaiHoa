from flask import Flask, request, jsonify
import torch
from PIL import Image
import numpy as np
from torch import nn
from torch.autograd import Variable
from collections import OrderedDict
import json
import torch.nn as nn
from model import stt2024
from io import BytesIO

def load_checkpoint(filepath):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    checkpoint = torch.load(filepath, map_location=device)
    model = stt2024()
    classifier = nn.Sequential(OrderedDict([
                          ('fc1', nn.Linear(25088, 500)),
                          ('relu', nn.ReLU()),
                          ('dropout1', nn.Dropout(p= 0.02)),
                          ('fc2', nn.Linear(500, 102)),
                          ('output', nn.LogSoftmax(dim=1))
                          ]))

    model.classifier = classifier
    model.load_state_dict(checkpoint['state_dict'])

    return model, checkpoint['class_to_idx']

def process_image(image):
    size = 256, 256
    image.thumbnail(size, Image.LANCZOS)
    image = image.crop((128 - 112, 128 - 112, 128 + 112, 128 + 112))
    npImage = np.array(image)
    npImage = npImage/255.

    imgA = npImage[:,:,0]
    imgB = npImage[:,:,1]
    imgC = npImage[:,:,2]

    imgA = (imgA - 0.485)/(0.229)
    imgB = (imgB - 0.456)/(0.224)
    imgC = (imgC - 0.406)/(0.225)

    npImage[:,:,0] = imgA
    npImage[:,:,1] = imgB
    npImage[:,:,2] = imgC

    npImage = np.transpose(npImage, (2,0,1))

    return npImage


def predict_flower(image_path, model, topk=5):
    image = torch.FloatTensor([process_image(image_path)])
    model.eval()
    output = model.forward(Variable(image))
    pobabilities = torch.exp(output).data.numpy()[0]

    top_idx = np.argsort(pobabilities)[-topk:][::-1]
    top_class = [idx_to_class[x] for x in top_idx]
    top_probability = pobabilities[top_idx]

    return top_probability, top_class

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():    
    if 'image' not in request.files:
        return jsonify({'error': 'Không có hình ảnh được cung cấp'}), 400

    image_pil = Image.open(BytesIO(request.files['image'].read()))
    
    # image_file = request.files['image']
    # image = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)
    
    p, c = predict_flower(image_pil, loaded_model)
    print(p, c)
    accuracy = float(p[0])
    return jsonify({'flower': cat_to_name[c[0]], 'accuracy': accuracy}), 200


loaded_model, class_to_idx = load_checkpoint('./checkpoint6_31Hoa.pth')
idx_to_class = { v : k for k,v in class_to_idx.items()}
with open('./cat_to_name.json', 'r') as f:
    cat_to_name = json.load(f)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

