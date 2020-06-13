import cv2
import json
import requests
import RPi.GPIO as GPIO
import dht11
import time

from watson_developer_cloud import VisualRecognitionV3
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.cleanup()
SensorInstance = dht11.DHT11(pin = 12)
GPIO.setup(7, GPIO.OUT)
p = GPIO.PWM(7, 50)
p.start(7.5)
T=0
H=0
visual_recognition = VisualRecognitionV3(
    '2018-03-19',
    iam_apikey='JTxiAlbDnxppMgOicLZuIOy-rbfbZQgipIQ5AisWmlsE')

# Loading the cascades
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
# Defining a function that will do the detections
def detect(gray, frame):
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        print (faces.shape)
        print ("Number of faces detected: " + str(faces.shape[0]))
        cv2.putText(frame, "Number of faces detected: " + str(faces.shape[0]), (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        FaceFileName = "face.jpg"
        cv2.imwrite(FaceFileName, roi_color)
        with open('./face.jpg', 'rb') as images_file:
            classes = visual_recognition.classify(
            images_file,
            threshold='0.6',
            classifier_ids='new_model_2017432400').get_result()
        #print (classes)
        try:
            data=classes["images"][0]['classifiers'][0]['classes'][0]['class']
            print(classes["images"][0]['classifiers'][0]['classes'][0]['class'])
            if(data=="Simran.zip"):
                p.ChangeDutyCycle(12.5)
                print("door open")
            else:
                print("door locked")
                p.ChangeDutyCycle(2.5)
            
                
                
        except:
            print("")
        #print(json.dumps(classes, indent=2))
        cv2.putText(frame, data, (x, y),
        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 3)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
    return frame

video_capture = cv2.VideoCapture(0)
# Doing some Face Recognition with the webcam
while True:
        p.ChangeDutyCycle(2.5)
        SensorData = SensorInstance.read()
        if SensorData.is_valid():
                T = SensorData.temperature
                H = SensorData.humidity
                response=requests.get("https://ozzy.eu-gb.mybluemix.net/data?temperature="+str(SensorData.temperature)+"&humidity="+str(SensorData.humidity))
                print(response)
        else:
                print ("SensorData Invalid")
        
        _,frame = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        canvas = detect(gray, frame)
        cv2.imshow('Video', canvas)
        if cv2.waitKey(1) & 0xFF == ord('q'):
                break
video_capture.release()
cv2.destroyAllWindows()
