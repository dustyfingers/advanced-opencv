import cv2
import time
import numpy as np
import HandTrackingModule as ht
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# you can set resolution to be whatever you like....mind the native resolution of the input however
wCam, hCam = 1920, 1080

# the source for video capture could also be video from an assets folder (for example)
cap = cv2.VideoCapture(0)

# manually set capture size
cap.set(3, wCam)
cap.set(4, hCam)

# initial past time
p_time = 0

# init instance of custom hand tracking module
detector = ht.HandDetector(detectionCon=0.7)

# hook into system audio
audio_device = AudioUtilities.GetSpeakers()
interface = audio_device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# volume range is how loud or quiet the system can go ...obv
# ~ -65 to 0 on my system
vol_range = volume.GetVolumeRange()
min_volume = vol_range[0]
max_volume = vol_range[1]

while True:
    success, frame  = cap.read()

    # find hands in frame
    handsFrame = detector.findHands(frame)

    lm_list = detector.findPosition(handsFrame, draw=False)

    if len(lm_list) != 0:
        thumb_x, thumb_y = lm_list[4][1], lm_list[4][2]
        pointer_x, pointer_y  = lm_list[8][1], lm_list[8][2]
        center_x, center_y = (thumb_x + pointer_x) // 2, (thumb_y + pointer_y) // 2

        # draw circles on appropriate finger tips
        cv2.circle(frame, (thumb_x, thumb_y), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(frame, (pointer_x, pointer_y), 15, (255, 0, 255), cv2.FILLED)

        # draw line and center circle
        cv2.line(frame, (thumb_x, thumb_y), (pointer_x, pointer_y), (255, 0, 255), 3)
        cv2.circle(frame, (center_x, center_y), 15, (255, 0, 255), cv2.FILLED)

        # find length of line
        length = math.hypot(pointer_x - thumb_x, pointer_y - thumb_y)

        # hand range is around 50 to 300
        # vol range is -65 to 0
        # need to convert hand range to vol range using numpy
        vol = np.interp(length, [50, 300], [min_volume, max_volume])

        # change system volume based on line length
        volume.SetMasterVolumeLevel(vol, None)

        # make center circle green when pointer and thumb are pressed together irl
        # if length < 50:
        #     cv2.circle(frame, (center_x, center_y), 15, (0, 255, 0), cv2.FILLED)


    # c_time is current time, p_time is past time
    c_time = time.time()

    # calculate frames per second
    fps = 1 / (c_time - p_time)
    p_time = c_time
    cv2.putText(frame, f'FPS: {str(int(fps))}', (40, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("Image", handsFrame)
    cv2.waitKey(1)