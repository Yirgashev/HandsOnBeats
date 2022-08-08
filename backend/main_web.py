from fastapi import FastAPI,Request
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import time
import csv
import copy
import itertools
import cv2 as cv
import numpy as np
import mediapipe as mp
import base64
from fastapi import Body
import os

import sys

# pwd = os.getcwd()
# 当前路径的父路径
# f_pwd = os.path.abspath(os.path.join(os.getcwd(), ".."))
HERE = os.path.dirname(__file__)
# f_pwd = os.path.abspath(os.path.join(os.getcwd()),"")
HAND_GESTURE_RECOGNITION = HERE + '/hand_gesture_recognition'

print (HAND_GESTURE_RECOGNITION)
sys.path.append(HAND_GESTURE_RECOGNITION)
sys.path.append(HERE)

from model import KeyPointClassifier
import ranking_list
# class Model:
#     image = cv.Mat
#     f = None
#     mp_hands = None
#     hands = None
#     keypoint_classifier = None
#
#     def pre_process_landmark(self,landmark_list):
#         temp_landmark_list = copy.deepcopy(landmark_list)
#
#         # Convert to relative coordinates
#         base_x, base_y = 0, 0
#         for index, landmark_point in enumerate(temp_landmark_list):
#             if index == 0:
#                 base_x, base_y = landmark_point[0], landmark_point[1]
#
#             temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
#             temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y
#
#         # Convert to a one-dimensional list
#         temp_landmark_list = list(
#             itertools.chain.from_iterable(temp_landmark_list))
#
#         # Normalization
#         max_value = max(list(map(abs, temp_landmark_list)))
#
#         def normalize_(n):
#             return n / max_value
#
#         temp_landmark_list = list(map(normalize_, temp_landmark_list))
#
#         return temp_landmark_list
#
#     def calc_landmark_list(self,image, landmarks):
#         image_width, image_height = image.shape[1], image.shape[0]
#
#         landmark_point = []
#
#         # Keypoint
#         for _, landmark in enumerate(landmarks.landmark):
#             landmark_x = min(int(landmark.x * image_width), image_width - 1)
#             landmark_y = min(int(landmark.y * image_height), image_height - 1)
#             # landmark_z = landmark.z
#
#             landmark_point.append([landmark_x, landmark_y])
#
#         return landmark_point
#
#     def __init__(self):
#         self.f = open(
#             'C:\\Users\\Lim\\Desktop\\taigu\\backend\\hand_gesture_recognition\\model\\keypoint_classifier\\keypoint_classifier_label.csv',
#             encoding='utf-8-sig')
#         self.mp_hands = mp.solutions.hands
#         self.hands = self.mp_hands.Hands()
#         self.keypoint_classifier = KeyPointClassifier()
#
#
#
#     def predict(self):
#         keypoint_classifier_labels = csv.reader(self.f)
#         keypoint_classifier_labels = [row[0] for row in keypoint_classifier_labels]
#
#         image = cv.flip(self.image, 1)  # Mirror display
#         debug_image = copy.deepcopy(image)
#         image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
#         results = self.hands.process(image)
#         if results.multi_hand_landmarks is not None:
#             for hand_landmarks, handedness in zip(results.multi_hand_landmarks,
#                                                   results.multi_handedness):
#                 # Landmark calculation
#                 landmark_list = self.calc_landmark_list(debug_image, hand_landmarks)
#
#                 # Conversion to relative coordinates / normalized coordinates
#                 pre_processed_landmark_list = self.pre_process_landmark(
#                     landmark_list)
#
#                 hand_sign_id = self.keypoint_classifier(pre_processed_landmark_list)
#                 gesture = keypoint_classifier_labels[hand_sign_id]
#                 print("识别结果：" + gesture)
#         if results.multi_hand_landmarks is None:
#             print("无手势")


def pre_process_landmark(landmark_list):
    temp_landmark_list = copy.deepcopy(landmark_list)

    # Convert to relative coordinates
    base_x, base_y = 0, 0
    for index, landmark_point in enumerate(temp_landmark_list):
        if index == 0:
            base_x, base_y = landmark_point[0], landmark_point[1]

        temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
        temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y

    # Convert to a one-dimensional list
    temp_landmark_list = list(
        itertools.chain.from_iterable(temp_landmark_list))

    # Normalization
    max_value = max(list(map(abs, temp_landmark_list)))

    def normalize_(n):
        return n / max_value

    temp_landmark_list = list(map(normalize_, temp_landmark_list))

    return temp_landmark_list

def calc_landmark_list(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]

    landmark_point = []

    # Keypoint
    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)
        # landmark_z = landmark.z

        landmark_point.append([landmark_x, landmark_y])

    return landmark_point


mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
keypoint_classifier = KeyPointClassifier()
MODEL_FILE_PATH = os.path.join(HAND_GESTURE_RECOGNITION,"model")
f = open(
    MODEL_FILE_PATH + '/keypoint_classifier/keypoint_classifier_label.csv',
    encoding='utf-8-sig')
keypoint_classifier_labels = csv.reader(f)
keypoint_classifier_labels = [row[0] for row in keypoint_classifier_labels]

#预测手势
def predict(image):
    image = cv.flip(image, 1)  # Mirror display
    debug_image = copy.deepcopy(image)
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    results = hands.process(image)
    if results.multi_hand_landmarks is not None:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks,
                                                  results.multi_handedness):
            # Landmark calculation
            landmark_list = calc_landmark_list(debug_image, hand_landmarks)

            # Conversion to relative coordinates / normalized coordinates
            pre_processed_landmark_list = pre_process_landmark(
                landmark_list)

            hand_sign_id = keypoint_classifier(pre_processed_landmark_list)
            gesture = keypoint_classifier_labels[hand_sign_id]
            print("识别结果：" + gesture)
            return gesture
    if results.multi_hand_landmarks is None:
        print("无手势")
        return 'null'



app = FastAPI()

#跨域
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:5173",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:5173"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

frontend_dir=os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '/frontend'
print(frontend_dir)

template=Jinja2Templates(frontend_dir)

@app.get("/")
async def user(req:Request):
    return template.TemplateResponse("test.html",context={"request":req})

#手势识别
@app.post("/base64file")
async def uploadfile(image=Body(None), suffix=Body(None)):
    imgdata = base64.b64decode(image)
    nparr = np.fromstring(imgdata, np.uint8)
    images = cv.imdecode(nparr, cv.IMREAD_COLOR)
    start = time.perf_counter()
    # model.image = image
    # model.predict()
    res = predict(images)
    end  = time.perf_counter()
    runTime = end - start
    runTime_ms = runTime * 1000
    print("运行时间：", runTime_ms, "毫秒")
    return {'gesture_recognition_result': res}

#保存成绩
@app.post("/saveScore")
async def saveScore(id=Body(None),score=Body(None)):
    ndate = time.strftime('%Y-%m-%d %H:%M:%S')
    ranking_list.insert_data('mydb',id,score,ndate)
    # if(ranking_list.insert_data('mydb',id,score,ndate)):
    #     return {'status':'1'}
    # else:
    #     return {'status':'0'}

#查询前十名成绩
@app.post("/getRankingList")
async def getRankingList():
    return  ranking_list.listByScore('mydb')

if __name__ == '__main__':
    uvicorn.run(app,)

