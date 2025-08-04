import numpy as np
import cv2 #load image
import mediapipe as mp
import matplotlib.pyplot as plt

def process_image(file):
    #Load image from file
    image=cv2.imread(file)

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
    pose_processed=pose.process(image_rgb)

    #Check if the pose is found
    if pose_processed.pose_landmarks:
        print("Pose landmarks found!")
    else:
        print("No pose detected.")
    
    return pose_processed

    #Set up drawing
    # mp_drawing=mp.solutions.drawing_utils

    #Make a copy to draw on
    # image_copy=image_rgb.copy()

    #Draw the pose on the copy
    # if pose_processed.pose_landmarks:
    #     mp_drawing.draw_landmarks(
    #         image=image_copy,
    #         landmark_list=pose_processed.pose_landmarks,
    #         connections=mp_pose.POSE_CONNECTIONS
    #     )

    # Show the final result
    # plt.imshow(image_copy)
    # plt.axis('off')
    # plt.title("Pose Detected")
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

def is_about(angle, target, tolerance=15):
    return abs(angle-target)<tolerance

def downward_dog(landmark):
    #right arm
    wristR=landmark[16]
    elbowR=landmark[14]
    shoulderR=landmark[12]
    #left arm
    wristL=landmark[15]
    elbowL=landmark[13]
    shoulderL=landmark[11]

    #arms straight
    armR=calculate_angle(wristR, elbowR, shoulderR)
    # print(f"Right arm{armR}")
    armL=calculate_angle(wristL, elbowL, shoulderL)
    # print(f"Left arm{armL}")
    arms_straight=(is_about(armR,180) and is_about(armL,180))
    #wrist-hip-toe angle
    hipR=landmark[24]
    heelR=landmark[30]
    # hipR_wristR_v=np.array([wristR.x-hipR.x, wristR.y-hipR.y]) #vector hip->wrist, hip is higher
    hip_angle=calculate_angle(wristR, hipR, heelR)
    hip_bent=hip_angle<=90 and hip_angle>=45

    return hip_bent and arms_straight # and hipR_wristR_v.all()<0

def tree(landmark):
    #left leg
    hipL=landmark[23]
    kneeL=landmark[25]
    heelL=landmark[29]
    #right leg
    hipR=landmark[24]
    kneeR=landmark[26]
    heelR=landmark[30]

    #calculating angles and difference
    legL_angle=calculate_angle(hipL, kneeL, heelL)
    # print(f"Left leg{legL_angle}")
    legR_angle=calculate_angle(hipR, kneeR, heelR)
    # print(f"Right leg{legR_angle}")
    heelLR_diff=heelR.y-heelL.y
    heelRL_diff=heelL.y-heelR.y
    # print(f"Diff LR{heelLR_diff}")
    # print(f"Diff RL{heelRL_diff}")
    #calculating tree right leg bended
    tree_right=(is_about(legL_angle,180) and legR_angle<90 and heelLR_diff<0)
    #calculating tree left leg bended
    tree_left=(is_about(legR_angle,180) and legL_angle<90 and heelRL_diff<0)

    #result
    return tree_right ^ tree_left #xor

def warrior2(landmark):
    #arms
    wristL=landmark[15]
    shoulderL=landmark[11]
    wristR=landmark[16]
    #left leg
    hipL=landmark[23]
    kneeL=landmark[25]
    heelL=landmark[29]
    #right leg
    hipR=landmark[24]
    kneeR=landmark[26]
    heelR=landmark[30]

    #calculating arms open straight
    arms_angle=calculate_angle(wristL, shoulderL, wristR)
    # print(f"Arms angle{arms_angle}")
    #calculating angles and difference
    legL_angle=calculate_angle(hipL, kneeL, heelL)
    # print(f"Left leg{legL_angle}")
    legR_angle=calculate_angle(hipR, kneeR, heelR)
    # print(f"Right leg{legR_angle}")
    #calculating right leg bended
    legR_bended=(is_about(legL_angle,180) and is_about(legR_angle,90, 30))
    #calculating left leg bended
    legL_bended=(is_about(legR_angle,180) and is_about(legL_angle,90, 30))

    #result
    return is_about(arms_angle,180) and (legR_bended ^ legL_bended)

def detect_pose(pose_processed):
    landmark=pose_processed.pose_landmarks.landmark
    if (downward_dog(landmark)):
        print("Downward Dog") 
        return "Downward Dog"
    elif(tree(landmark)):
        print("Tree")
        return "Tree"
    elif(warrior2(landmark)):
        print("Warrior II")
        return "Warrior II"
    else:
        print("Pose not detected")
        return "Pose not detected"


#Tests
# wrist=pose_processed.pose_landmarks.landmark[15]
# elbow=pose_processed.pose_landmarks.landmark[13]
# shoulder=pose_processed.pose_landmarks.landmark[11]
# print(f"Angle:{calculate_angle(wrist, elbow, shoulder)}")

# detect_pose(process_image("poses/downwarddog.jpeg"))
# detect_pose(process_image("poses/tree.jpg"))
# detect_pose(process_image("poses/warrior2.jpg"))




