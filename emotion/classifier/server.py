from . import app
from flask import render_template, Response
from .model import generate_frames, set_video_streaming



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    set_video_streaming(True)
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stop_video')
def stop_video():
    set_video_streaming(False)
    return ('', 204)

