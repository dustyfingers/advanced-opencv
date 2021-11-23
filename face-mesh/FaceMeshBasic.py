import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

# initial past time
p_time = 0

# mp drawing utilities
mp_draw = mp.solutions.drawing_utils
draw_spec = mp_draw.DrawingSpec(thickness=1, circle_radius=2)

# mp face utils
mp_facemesh = mp.solutions.face_mesh
faceMesh = mp_facemesh.FaceMesh(max_num_faces=2)

while True:
    success, img = cap.read()

    # convert to rgb
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # use mediapipe to find face landmarks
    results = faceMesh.process(imgRGB)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            mp_draw.draw_landmarks(img, face_landmarks, mp_facemesh.FACE_CONNECTIONS, draw_spec, draw_spec)

    # c_time is current time, p_time is past time
    c_time = time.time()

    # calculate frames per second
    fps = 1 / (c_time - p_time)
    p_time = c_time
    cv2.putText(img, f'FPS: {str(int(fps))}', (40, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("Webcam", img)
    cv2.waitKey(1)