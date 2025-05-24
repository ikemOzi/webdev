from . import app
from flask import render_template, Response
from .model import generate_frames, set_video_streaming



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

