import keras
import cv2
import numpy as np
import base64

model = keras.models.load_model(r"C:\Users\IKEMBUCHUKWU\PycharmProjects\automating\emotion\classifier\artifacts\disgust_surp_happy_sad 83.keras")

video_streaming = False

def set_video_streaming(value):
    global video_streaming
    video_streaming = value

def generate_frames():
    global video_streaming
    font_scale = 1.5
    font = cv2.FONT_HERSHEY_PLAIN
    rectangle_bgr = (255, 255, 255)
    img = np.zeros((500, 500))
    text = "some text in a box!"
    (text_width, text_height) = cv2.getTextSize(text, font, fontScale=font_scale, thickness=1)[0]
    text_offset_x = 10
    text_offset_y = img.shape[0] - 25

    box_coords = ((text_offset_x, text_offset_y), (text_offset_x + text_width + 2, text_offset_y - text_height - 2))
    cv2.rectangle(img, box_coords[0], box_coords[1], rectangle_bgr, cv2.FILLED)
    cv2.putText(img, text, (text_offset_x, text_offset_y), font, fontScale=font_scale, color=(0, 0, 0), thickness=1)

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Error: could not open camera")
        return

    while video_streaming:
        success, frame = camera.read()
        if not success:
            break
        else:
            faceCascade = cv2.CascadeClassifier(r"C:\Users\IKEMBUCHUKWU\PycharmProjects\automating\emotion\classifier\artifacts\haarcascades\haarcascade_frontalface_default.xml")
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.1, 4)
            for x, y, w, h in faces:
                roi_gray = gray[y:y + h, x:x + w]
                roi_color = frame[y:y + h, x:x + w]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                faces = faceCascade.detectMultiScale(roi_gray)

                face_roi = None

                if len(faces) == 0:
                    print("Face not detected")
                else:
                    face_roi = None
                    for (ex, ey, ew, eh) in faces:
                        face_roi = roi_color[ey: ey + eh, ex:ex + ew]

            if face_roi is not None:
                final_image = cv2.resize(face_roi, (64, 64))
                final_image = np.expand_dims(final_image, axis=0)
                final_image = final_image / 255.0
            else:
                continue

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
    


##### CAMERA

camera_streaming = False

capture = None

def change_streaming(value):
    global camera_streaming
    camera_streaming = value


def intit_camera():
    global capture
    if capture is None or not capture.isOpened():
        capture = cv2.VideoCapture(0)

def capture_stream():
    intit_camera()
    return capture.read()
    # isTrue, frame = capture.read()
    # return isTrue, frame

def release_camera():
    global capture
    if capture is not None:
        capture.release()
        capture = None



def camera_video():

    while True:
        isTrue, frame = capture_stream()
        if not isTrue:
            print('Failed to read frame')
            break
        

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        # convert to jpeg
        ret,buffer = cv2.imencode('.jpg', frame)
        frame= buffer.tobytes()

        if camera_streaming:
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            
            # change to Base64 encode
            img_base64 = base64.b64encode(buffer).decode('utf-8')
            data_url = f"data:image/jpeg;base64,{img_base64}"
            image = data_url.encode('utf-8')
            yield image
            break
                
            