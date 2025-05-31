from . import app
from flask import render_template, Response
from .model import generate_frames, set_video_streaming, camera_video, change_streaming, release_camera, capture_stream, stop_requested, emotion_classifier
import cv2 as cv
from flask import jsonify
import base64



@app.route('/')
@app.route('/Live_Classifier')
def liveClassifier():
    return render_template('liveClassifier.html')

@app.route('/video')
def video():
    set_video_streaming(True)
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stop_video')
def stop_video():
    set_video_streaming(False)
    return ('', 204)

@app.route('/home_page')
def home_page():
    return render_template('home_page.html')

@app.route('/takePhoto')
def takePhoto_page():
    return render_template('TakePhoto.html')

@app.route('/photo')
def photo():
    change_streaming(True)
    return Response(camera_video(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/takeSelfie')
def selfie():
    change_streaming(False)
    isTrue, frame = capture_stream()
    if not isTrue:
        return jsonify({'error': 'Failed to capture image'}), 500
    
    ret, buffer = cv.imencode('.jpg', frame)
    if not ret:
        return jsonify({'error': 'Failed to encode image'}), 500

    
    release_camera()

    prediction = emotion_classifier(frame)

     # Encode image to Base64
    img_base64 = base64.b64encode(buffer).decode('utf-8')
    img_data_url = f"data:image/jpeg;base64,{img_base64}"

    return jsonify({
        'image': img_data_url,
        'prediction': prediction

    })
    # return Response(buffer.tobytes(), mimetype='image/jpeg')
    

@app.route('/clearPhoto')
def clearPhoto():
    release_camera()
    stop_requested(True)
    return('', 204)
    



