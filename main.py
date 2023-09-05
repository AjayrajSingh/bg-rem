from flask import Flask, request, jsonify
from rembg import remove
from PIL import Image
from io import BytesIO
import requests

app = Flask(__name__)

@app.route("/remove-bg", methods=["POST"])
def remove_bg():
    data = request.get_json()
    imageUrl = data['image']
    response = requests.get(imageUrl)
    if response.status_code == 200:
        input_image_data = BytesIO(response.content)
        input_image = Image.open(input_image_data)
        output_image = remove(input_image, alpha_matting=True)
        output_image_path = 'output.png'
        output_image.save(output_image_path)
        return jsonify({'output-location' :output_image_path}), 201
    else:
        return jsonify({'response' :'failed'}), 500

if __name__ == "__main__":
    app.run(debug=True)