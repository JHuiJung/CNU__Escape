import cv2
from pathlib import Path
import numpy as rp

BODY_PARTS = { "Head": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
                "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
                "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "Chest": 14,
                "Background": 15 }

POSE_PAIRS = [ ["Head", "Neck"], ["Neck", "RShoulder"], ["RShoulder", "RElbow"],
                ["RElbow", "RWrist"], ["Neck", "LShoulder"], ["LShoulder", "LElbow"],
                ["LElbow", "LWrist"], ["Neck", "Chest"], ["Chest", "RHip"], ["RHip", "RKnee"],
                ["RKnee", "RAnkle"], ["Chest", "LHip"], ["LHip", "LKnee"], ["LKnee", "LAnkle"] ]                

    
# 각 파일 path
protoFile = "./pose_deploy_linevec_faster_4_stages.prototxt"
weightsFile= "./pose_iter_160000.caffemodel"

net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)

capture = cv2.VideoCapture(0) 

inputWidth=320
inputHeight=240
inputScale=1.0/255

while cv2.waitKey(1) <0:
    hasFrame, frame = capture.read()  
    if not hasFrame:
        cv2.waitKey()
        break
    
    frameWidth = frame.shape[1]
    frameHeight = frame.shape[0]
    
    inpBlob = cv2.dnn.blobFromImage(frame, inputScale, (inputWidth, inputHeight), (0, 0, 0), swapRB=False, crop=False)
    
    imgb=cv2.dnn.imagesFromBlob(inpBlob)
    
    net.setInput(inpBlob)

    output = net.forward()

    points = []
    for i in range(0,15):
        probMap = output[0, i, :, :]
    
        minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)

        x = (frameWidth * point[0]) / output.shape[3]
        y = (frameHeight * point[1]) / output.shape[2]

        if prob > 0.1 :    
            cv2.circle(frame, (int(x), int(y)), 3, (0, 255, 255), thickness=-1, lineType=cv2.FILLED) # circle(그릴곳, 원의 중심, 반지름, 색)
            cv2.putText(frame, "{}".format(i), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, lineType=cv2.LINE_AA)
            points.append((int(x), int(y)))
        else :
            points.append(None)
    
    for pair in POSE_PAIRS:
        partA = pair[0]             # Head
        partA = BODY_PARTS[partA]   # 0
        partB = pair[1]             # Neck
        partB = BODY_PARTS[partB]   # 1
        
        if points[partA] and points[partB]:
            cv2.line(frame, points[partA], points[partB], (0, 255, 0), 2)
    

    if (points[3] is not None) and (points[5] is not None)and(points[6] is not None) and(points[7] is not None):
        point_4 = points[4] #왼쪽 손목
        point_2 = points[2] #왼쪽 어깨
        point_7 = points[7] #오른쪽 손목
        point_5 = points[5] #오른쪽 어깨
        point_3 = points[3] #왼쪽 팔꿈치
        point_6 = points[6] #오른쪽 팔꿈치

        if(point_4[0] < point_7[0] and point_3[1]>point_5[1] and point_6[1] > point_7[1]):
         cv2.putText(frame, "DEFENCE",(0,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

    if (points[12] is not None) and (points[11] is not None)and(points[9] is not None) and(points[8] is not None): 
        point_11 = points[11] #오른쪽 엉덩이
        point_12 = points[12] #오른쪽 무릎
        point_8 = points[8] #왼쪽 엉덩이
        point_9 = points[9] #왼쪽 무릎
        if(point_12[1] < point_11[1] or point_9[1] < point_8[1]):
         cv2.putText(frame, "ATTACK",(0,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

    if (points[0] is not None) and (points[2] is not None) and (points[5] is not None):
        point_0 = points[0] #머리
        point_2 = points[2] #왼쪽 어깨        
        point_5 = points[5] #오른쪽 어깨

        if(point_0[1] > point_2[1] ) or (point_0[1] > point_5[1]):
         cv2.putText(frame, "BOW",(0,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
    cv2.imshow("Output-Keypoints",frame)
    
capture.release()
cv2.destroyAllWindows()