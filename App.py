from flask import Flask, render_template, request, Response
import cv2
from datetime import datetime
import os
from PIL import Image
import numpy as np

from static.api import call

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'your_secret_key'
image_folder = os.path.join(app.static_folder, 'temp')
camera = cv2.VideoCapture(0)

# Route to the home page
@app.route('/')
def home():
    image_files = os.listdir(image_folder)
    
    # Check if there is an image file
    if image_files:
        image_path = os.path.join('temp', image_files[0]).replace('\\', '/')
    else:
        image_path = None

    # Render the home template and pass the image path to it
    return render_template('index.html', image_path=image_path)

# Route to handle the file upload
@app.route('/upload_picture', methods=['GET','POST'])
def upload_picture():
    if request.method == 'POST':
    # Check if a file was uploaded in the request
        if 'file' not in request.files:
            return 'No file uploaded'

        file = request.files['file']

        # Check if a file was selected
        if file.filename == '':
            return 'No file selected'
        
        image = Image.open(file)
        resized_image = image.resize((2160, 2160))

        current_date = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"uploaded_image_{current_date}"

        # Create the save folder if it doesn't exist
        save_folder = os.path.join(app.static_folder, 'temp')
        os.makedirs(save_folder, exist_ok=True)

        # Save the uploaded file to the save folder
        save_path = os.path.join(save_folder, f'{file_name}.jpg')
        resized_image.save(save_path)

        return '''
        <script>
            alert('File uploaded successfully!');
            window.location.href = '/';
        </script>
        '''
    return '''
    <script>
        alert('Failed to upload file!');
        window.location.href = '/';
    </script>
    '''

@app.route('/take_picture', methods=['GET','POST'])
def take_picture():
    if request.method == 'POST':
        # Read the frame from the camera
        success, frame = camera.read()
        if success:
            # Flip the frame horizontally
            frame = cv2.flip(frame, 1)

            image = Image.fromarray(frame)
            resized_image = image.resize((2160, 2160))

            resized_array = np.array(resized_image)

            current_date = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"take_picture_{current_date}"

            # Save the frame to the "save" folder
            save_folder = os.path.join(app.static_folder, 'temp')
            os.makedirs(save_folder, exist_ok=True)
            save_path = os.path.join(save_folder, f'{file_name}.jpg')
            cv2.imwrite(save_path, resized_array)

            return '''
            <script>
                alert('File uploaded successfully!');
                window.location.href = '/';
            </script>
            '''
        
    return '''
    <script>
        alert('Failed to capture picture');
        window.location.href = '/';
    </script>
    '''

@app.route('/video_feed')
def video_feed():
    def generate_frames():
        while True:
            # Baca frame dari kamera
            success, frame = camera.read()
            if not success:
                break
            else:
                # Ubah format frame menjadi format yang dapat ditampilkan di HTML (JPG)
                frame = cv2.flip(frame, 1)
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()

            # Mengirimkan frame kepada HTML untuk ditampilkan
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    # Mengembalikan respons video streaming dengan menggunakan generator frames
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/identifikasi', methods=['POST'])
def identifikasi():
    result = call(r'static\temp\*')

    if result == 1:
        res = "Ripe"
    else:
        res = "Unripe"
    
    image_folder = os.path.join(app.static_folder, 'temp')
    image_files = os.listdir(image_folder)
    
    # Check if there is an image file
    if image_files:
        image_path = os.path.join('temp', image_files[0]).replace('\\', '/')
    else:
        image_path = None

    # Render the home template and pass the image path to it
    return render_template('identifikasi.html', image_path=image_path, result = res)

@app.route('/hapus', methods=['GET'])
def hapus():
    files = os.listdir(image_folder)
    for file in files:
        file_path = os.path.join(image_folder, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
            return '''
                    <script>
                        alert('File deleted!');
                        window.location.href = '/';
                    </script>
                    '''
        
    return '''
            <script>
                alert('No file found!');
                window.location.href = '/';
            </script>
            '''
    
if __name__ == '__main__':
    app.run(debug=True)
