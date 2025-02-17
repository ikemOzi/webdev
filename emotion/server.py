from flask import Flask, render_template, Response
import cv2

app= Flask(__name__)



def generate_frames():
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Error: could not open camera")
        return

    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            faceCascade = cv2.CascadeClassifier(r"C:\Users\IKEMBUCHUKWU\PycharmProjects\automating\emotion\artifacts\haarcascades\haarcascade_frontalface_default.xml")
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.1, 4)
            for x, y, w, h in faces:
                roi_gray = gray[y:y + h, x:x + w]
                roi_color = frame[y:y + h, x:x + w]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                faces = faceCascade.detectMultiScale(roi_gray)
                if len(faces) == 0:
                    print("Face not detected")
                else:
                    for (ex, ey, ew, eh) in faces:
                        face_roi = roi_color[ey: ey + eh, ex:ex + ew]

            ret,buffer = cv2.imencode('.jpg', frame)
            frame= buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)

