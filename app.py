from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS from flask_cors
import subprocess
import base64
from PIL import Image
from io import BytesIO

app = Flask(__name__)
request_count = 0
CORS(app)  # Enable CORS for all routes

@app.route('/', methods=['POST'])
def detect():
    try:

        global request_count
        request_count += 1

        # Get the image file from the request
        image_file = request.files['image']

        # Decode base64 image data
        image = Image.open(BytesIO(image_file.read()))

        # Save the image to a temporary file
        image_path = "temp_image.jpg"
        image.save(image_path)

        # Replace this with your YOLO command
        yolo_command = "yolo task=detect mode=predict model=model.pt data=data.yaml source=temp_image.jpg"
        subprocess.run(yolo_command, shell=True)

        # Open the processed image
        result_image_path = f"runs/detect/predict{request_count}/temp_image.jpg"  # Update with the actual path of the processed image

        # Convert the processed image to base64
        with open(result_image_path, "rb") as result_image_file:
            encoded_image = base64.b64encode(result_image_file.read()).decode("utf-8")

        # Prepare the JSON response
        response_data = {
            'result_image': encoded_image,
            'mime_type': 'image/jpeg'  # Update with the appropriate MIME type
        }

        return jsonify(response_data)

    except Exception as e:
        return str(e), 400

if __name__ == '__main__':
    app.run()