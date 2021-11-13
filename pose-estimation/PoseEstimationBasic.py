import cv2
import mediapipe as mp
import time

# create pose object
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# mp drawing utilities
mp_draw = mp.solutions.drawing_utils

# capture video
cap = cv2.VideoCapture('assets/5.mp4')

# previous time
p_time = 0

while True:
    success, img = cap.read()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # process frame for human poses
    results = pose.process(img_rgb)

    # draw landmarks
    if results.pose_landmarks:
        mp_draw.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)


    # current time, calculate frames per second
    c_time = time.time()
    fps = 1 / (c_time - p_time)
    p_time = c_time

    # put fps on screen
    cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)