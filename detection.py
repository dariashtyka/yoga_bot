import numpy as np
import cv2 #load image
import mediapipe as mp
import matplotlib.pyplot as plt

#Load image from file
image=cv2.imread("posture.jpeg")

#Convert .jped-> rgb (for mediapipe)
image_rgb=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

#Show the image
plt.imshow(image_rgb)
plt.axis('off')
plt.title("Original Image")
# plt.show()

#Set up mediapipe pose
mp_pose=mp.solutions.pose
pose=mp_pose.Pose(static_image_mode=True) # For still images

#Run pose detection
results=pose.process(image_rgb)

#Check if the pose is found
if results.pose_landmarks:
    print("Pose landmarks found!")
else:
    print("No pose detected.")

#Set up drawing
mp_drawing=mp.solutions.drawing_utils

#Make a copy to draw on
image_copy=image_rgb.copy()

#Draw the pose on the copy
if results.pose_landmarks:
    mp_drawing.draw_landmarks(
        image=image_copy,
        landmark_list=results.pose_landmarks,
        connections=mp_pose.POSE_CONNECTIONS
    )

# Show the final result
plt.imshow(image_copy)
plt.axis('off')
plt.title("Pose Detected")
# plt.show()

def calculate_angle(pA, pB, pC):
    a = np.array([pA.x, pA.y])
    b = np.array([pB.x, pB.y])
    c = np.array([pC.x, pC.y])

    bc=c-b
    ba=a-b
    cosABC=np.dot(bc, ba)/(np.linalg.norm(bc)*np.linalg.norm(ba))
    angle_rad=np.arccos(np.clip(cosABC, -1.0, 1.0))
    angle_deg= np.degrees(angle_rad)
    return angle_deg

wrist=results.pose_landmarks.landmark[15]
elbow=results.pose_landmarks.landmark[13]
shoulder=results.pose_landmarks.landmark[11]
print(f"Angle:{calculate_angle(wrist, elbow, shoulder)}")




