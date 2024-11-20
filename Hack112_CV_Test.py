import mediapipe as mp
import cv2 as cv
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from collections import deque


globalCoords = deque()

def hand_tracker(app):
    cv.startWindowThread()
    capture = cv.VideoCapture(0)
    mp_hands = mp.solutions.hands 
    mp_drawing = mp.solutions.drawing_utils
    # For testing
    # mp_drawing_styles = mp.solutions.drawing_styles
    hands = mp_hands.Hands(
        static_image_mode = False,
        max_num_hands = 1,
        min_detection_confidence = 0.7
                          )

    while capture.isOpened() and not app.stopTracker:
        ret, annotatedFrame = capture.read()
        if not ret:
            break
        processingFrame = annotatedFrame.copy()
        processingFrame = cv.flip(cv.cvtColor(annotatedFrame, cv.COLOR_BGR2RGB), 1) # OpenCV initially provides a BGR frame
                                                                           # '1' means flip about y-axis; corrects handedness for mediapipe
        annotatedFrame = cv.flip(annotatedFrame, 1)
        results = hands.process(processingFrame) # the magic of mediapipe : )   
        
        if results.multi_hand_landmarks:
            for landmark in results.multi_hand_landmarks:
                indexTip = landmark.landmark[8]
                globalCoords.append((indexTip.x, indexTip.y))
                if len(globalCoords)>5:
                    globalCoords.popleft()
                circle_spec = mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=5)
                mp_drawing.draw_landmarks(annotatedFrame, landmark, mp_hands.HAND_CONNECTIONS, circle_spec, circle_spec)


        # For testing
        # cv.imshow("Fruit Ninja : )", annotatedFrame)

        if cv.waitKey(1) == 27:  # 27 is  ASCII code for 'Esc' 
            break

    capture.release()
    cv.destroyAllWindows()
    hands.close()


def getGlobalCoords():
    return globalCoords

def setGlobalCoords(deque):
    globalCoords = deque
