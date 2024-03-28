import cv2
import vmcp
import numpy as np

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2

from vmcp.osc import OSC
from vmcp.osc.typing import Message
from vmcp.osc.backend.osc4py3 import as_eventloop as backend

from time import time as get_time
 
cap = cv2.VideoCapture(0)

def draw_landmarks_on_image(rgb_image, detection_result):
    pose_landmarks_list = detection_result.pose_landmarks
    annotated_image = np.copy(rgb_image)

    for idx in range(len(pose_landmarks_list)):
        pose_landmarks = pose_landmarks_list[idx]

        pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        pose_landmarks_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(x = landmark.x, y = landmark.y, z = landmark.z) for landmark in pose_landmarks
        ])
        solutions.drawing_utils.draw_landmarks(
            annotated_image,
            pose_landmarks_proto,
            solutions.pose.POSE_CONNECTIONS,
            solutions.drawing_styles.get_default_pose_landmarks_style()
        )
    
    return annotated_image

options = vision.PoseLandmarkerOptions(
    base_options = python.BaseOptions(model_asset_path = 'pose_landmarker_heavy.task'),
    output_segmentation_masks = True
)
detector = vision.PoseLandmarker.create_from_options(options)

before = 0
osc = OSC(backend)

with osc.open():
    osc.create_sender("192.168.56.1", 39539, "sender1")
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue
    
        color = np.zeros(image.shape, np.uint8)
        color = mp.Image(image_format = mp.ImageFormat.SRGB, data = color)

        image = mp.Image(image_format = mp.ImageFormat.SRGB, data = image)

        detection_result = detector.detect(image)
        if detection_result.pose_landmarks != []:
            before = detection_result
        else:
            if before != 0:
                detection_result = before

        # print(detection_result.pose_landmarks)
    
        annotated_image = draw_landmarks_on_image(color.numpy_view(), detection_result)
        cv2.imshow('test', annotated_image)
        if cv2.waitKey(1) & 0xFF == 27:
            break
 
cap.release()