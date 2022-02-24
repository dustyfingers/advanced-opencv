import cv2
import mediapipe as mp
import time
    

class FaceMeshDetector():
    
    def __init__(self, static_mode=False, max_faces=1, min_detect_conf=0.6, min_track_conf=0.45):
        self.static_mode = static_mode
        self.max_faces = max_faces
        self.min_detect_conf = min_detect_conf
        self.min_track_conf = min_track_conf
        
        # mp drawing utilities
        self.mp_draw = mp.solutions.drawing_utils
        self.draw_spec = self.mp_draw.DrawingSpec(thickness=1, circle_radius=2)

        # mp face utils
        self.mp_facemesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_facemesh.FaceMesh(static_image_mode=self.static_mode, max_num_faces=self.max_faces, min_detection_confidence=self.min_detect_conf, min_tracking_confidence=self.min_track_conf)
        
    
    def find_face_mesh(self, img, draw=True):
        # convert to rgb
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # use mediapipe to find face landmarks
        self.results = self.face_mesh.process(imgRGB)
        
        faces = []

        if self.results.multi_face_landmarks:
            
            for face_landmarks in self.results.multi_face_landmarks:
                
                # draw mesh
                if (draw):
                    self.mp_draw.draw_landmarks(img, face_landmarks, self.mp_facemesh.FACEMESH_CONTOURS, self.draw_spec, self.draw_spec)
                
                face = []
                
                # find face position in image
                for id, lm in enumerate(face_landmarks.landmark):
                    
                    # image height, width
                    ih, iw, ic = img.shape
                    
                    # x and y of center of detected face
                    x, y = int(lm.x*iw), int(lm.y*ih)
                    
                            
                    cv2.putText(img, str(id), (x, y), cv2.FONT_HERSHEY_PLAIN, 0.5, (255, 0, 0), 1)

                    face.append([x,y])
                    
                faces.append(face)
                
        return img, faces


def main():
    
    # hook into video input
    cap = cv2.VideoCapture(0)

    # initial past time
    p_time = 0
    
    # init detector
    detector = FaceMeshDetector()
    
    while True:
        
        # capture input each frame
        success, img = cap.read()
        
        # process image and return modified image and faces array
        img, faces = detector.find_face_mesh(img)
        
        if len(faces) != 0:
            pass
            # print(len(faces))
        
        # c_time is current time, p_time is past time
        c_time = time.time()

        # calculate frames per second
        fps = 1 / (c_time - p_time)
        p_time = c_time
        cv2.putText(img, f'FPS: {str(int(fps))}', (40, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        cv2.imshow("Webcam", img)
        cv2.waitKey(1)


if __name__ == '__main__':
    main()