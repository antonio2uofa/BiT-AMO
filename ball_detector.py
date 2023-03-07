import cv2
import numpy as np

# Define the lower and upper bounds of the orange color in HSV color space
orange_lower = np.array([0, 50, 50])
orange_upper = np.array([20, 255, 255])

# Initialize the camera source (replace the parameter with the correct camera index or video file name)
cap = cv2.VideoCapture(0)

while True:
    # Capture a frame from the camera source
    ret, frame = cap.read()

    # Convert the frame from BGR to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Threshold the image to extract the orange regions
    orange_mask = cv2.inRange(hsv, orange_lower, orange_upper)

    # Apply a series of morphological operations to remove noise and fill holes
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    orange_mask = cv2.morphologyEx(orange_mask, cv2.MORPH_OPEN, kernel)
    orange_mask = cv2.morphologyEx(orange_mask, cv2.MORPH_CLOSE, kernel)

    # Find the contours of the orange regions
    contours, hierarchy = cv2.findContours(orange_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Extract the x and y coordinates of the centers of the four largest orange contours
    centers = []
    for cnt in sorted(contours, key=cv2.contourArea, reverse=True)[:4]:
        M = cv2.moments(cnt)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        centers.append(center)

    # Draw circles at the centers of the four detected balls
    for center in centers:
        cv2.circle(frame, center, 10, (0, 255, 0), 2)

    # Display the image with the detected circles
    cv2.imshow('frame', frame)

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera source and close all windows
cap.release()
cv2.destroyAllWindows()
###############

import cv2
import numpy as np

# Load the pre-trained object detector (replace the parameter with the path to the model file)
net = cv2.dnn.readNetFromTensorflow('frozen_inference_graph.pb', 'graph.pbtxt')

# Define the lower and upper bounds of the orange color in HSV color space
orange_lower = np.array([0, 50, 50])
orange_upper = np.array([20, 255, 255])

# Initialize the camera source (replace the parameter with the correct camera index or video file name)
cap = cv2.VideoCapture(0)

while True:
    # Capture a frame from the camera source
    ret, frame = cap.read()

    # Convert the frame from BGR to RGB color space and resize it to the input size of the object detector
    input_size = (300, 300)
    resized_frame = cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), input_size)

    # Create a blob from the resized frame and pass it through the object detector
    blob = cv2.dnn.blobFromImage(resized_frame, size=input_size, swapRB=True, crop=False)
    net.setInput(blob)
    detections = net.forward()

    # Extract the x and y coordinates of the centers of the four detected balls
    centers = []
    for i in range(detections.shape[2]):
        class_id = int(detections[0, 0, i, 1])
        if class_id == 1:  # Check if the detected object is a ball
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:  # Check if the detection has high confidence
                box = detections[0, 0, i, 3:7] * np.array([input_size[0], input_size[1], input_size[0], input_size[1]])
                x1, y1, x2, y2 = box.astype('int')
                center = ((x1 + x2) // 2, (y1 + y2) // 2)
                centers.append(center)

    # Draw circles at the centers of the four detected balls
    for center in centers:
        cv2.circle(frame, center, 10, (0, 255, 0), 2)

    # Display the image with the detected circles
    cv2.imshow('frame', frame)

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera source and close all windows
cap.release()
cv2.destroyAllWindows()
