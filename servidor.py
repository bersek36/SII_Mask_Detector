from flask import Flask, render_template, Response
from camera import Camera
import modelo
import cv2
app = Flask(__name__)

def gen_frames(camera):
    while True:

        success, frame = camera.get_frame()
        if success:
            faces, fr = modelo.to_tensor(frame)
            yest, boxes = modelo.detect_and_predict_mask(faces, fr)
            frame = modelo.labeled(fr, yest, boxes)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/video_feed')
def video_feed():


    return Response(gen_frames(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Detector')
def Detector():
    return render_template('Detector_mascara.html')

@app.route('/Nosotros')
def Nosotros():
    return render_template('Sobre_nosotros.html')

if __name__ == '__main__':
    app.run(host="localhost" ,debug=True)