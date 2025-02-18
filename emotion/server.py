from flask import Flask, render_template, Response
import cv2
import numpy as np
import tensorflow as tf
import keras

from keras.models import load_model

model = load_model(r"C:\Users\IKEMBUCHUKWU\PycharmProjects\automating\emotion\artifacts\disgust_surp_happy_sad 83.keras")


app= Flask(__name__)



font_scale = 1.5
font = cv2.FONT_HERSHEY_PLAIN
rectangle_bgr = (255, 255, 255)
img = np.zeros((500,500))
text = "some text in a box!"
(text_width, text_height) = cv2.getTextSize(text, font, fontScale= font_scale, thickness= 1)[0]
text_offset_x = 10
text_offset_y = img.shape[0] - 25

box_coords = ((text_offset_x, text_offset_y), (text_offset_x + text_width + 2, text_offset_y - text_height - 2))
cv2.rectangle(img, box_coords[0], box_coords[1], rectangle_bgr, cv2.FILLED)
cv2.putText(img, text, (text_offset_x, text_offset_y), font, fontScale = font_scale, color = (0,0,0), thickness = 1)

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

            final_image = cv2.resize(face_roi, (64, 64))
            final_image = np.expand_dims(final_image, axis=0)
            final_image = final_image / 255.0

            font = cv2.FONT_HERSHEY_SIMPLEX

            prediction = model.predict(final_image)

            font_scale = 1.5
            font = cv2.FONT_HERSHEY_PLAIN

            if (np.argmax(prediction) == 0):
                status = 'Disgust'

                x1, y1, w1, h1 = 0, 0, 175, 75
                cv2.rectangle(frame, (x1, x1), (x1 + w1, y1 + h1), (0, 0, 0), -1)
                cv2.putText(frame, status, (x1 + int(w1 / 10), y1 + int(h1 / 2)), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                            (0, 0, 255), 2)
                cv2.putText(frame, status, (100, 150), font, 3, (0, 0, 255), 2, cv2.LINE_4)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255))


            elif (np.argmax(prediction) == 1):
                status = 'Surprise'

                x1, y1, w1, h1 = 0, 0, 175, 75
                cv2.rectangle(frame, (x1, x1), (x1 + w1, y1 + h1), (0, 0, 0), -1)
                cv2.putText(frame, status, (x1 + int(w1 / 10), y1 + int(h1 / 2)), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                            (0, 0, 255), 2)
                cv2.putText(frame, status, (100, 150), font, 3, (0, 0, 255), 2, cv2.LINE_4)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255))


            elif (np.argmax(prediction) == 2):
                status = 'Happy'

                x1, y1, w1, h1 = 0, 0, 175, 75
                cv2.rectangle(frame, (x1, x1), (x1 + w1, y1 + h1), (0, 0, 0), -1)
                cv2.putText(frame, status, (x1 + int(w1 / 10), y1 + int(h1 / 2)), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                            (0, 0, 255), 2)
                cv2.putText(frame, status, (100, 150), font, 3, (0, 0, 255), 2, cv2.LINE_4)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255))


            elif (np.argmax(prediction) == 3):
                status = 'Sad'

                x1, y1, w1, h1 = 0, 0, 175, 75
                cv2.rectangle(frame, (x1, x1), (x1 + w1, y1 + h1), (0, 0, 0), -1)
                cv2.putText(frame, status, (x1 + int(w1 / 10), y1 + int(h1 / 2)), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                            (0, 0, 255), 2)
                cv2.putText(frame, status, (100, 150), font, 3, (0, 0, 255), 2, cv2.LINE_4)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255))

            cv2.imshow('Face Emotion Detection', frame)

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

