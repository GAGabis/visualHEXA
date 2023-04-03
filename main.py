import cv2
import numpy as np

cap = cv2.VideoCapture(0)

# image of the crosshair
mira = np.zeros((400, 400, 3), dtype=np.uint8)

cv2.line(mira, (0, 200), (400, 200), (0, 255, 255), 2)

# the static circle
mira_original = mira.copy()
cv2.circle(mira_original, (200, 200), 200, (0, 255, 255), 2)

angle = 0
while True:

    ret, frame = cap.read()

    if not ret:
        print("Não foi possível ler o frame")
        break

    frame_resized = cv2.resize(frame, (400, 400))

    # we use this to define the rotation matrix with the current angle
    center = (200, 200)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)

    # rotate the crosshair
    mira_rotated = cv2.warpAffine(mira, M, (mira.shape[1], mira.shape[0]))

    # copy the static circle from the original image to the rotated image
    mira_rotated_with_circle = mira_rotated.copy()
    mira_rotated_with_circle[mira_original > 0] = mira_original[mira_original > 0]

    # this is basically edge detection
    gray = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    edges = cv2.Canny(frame_resized, 100, 200)  # detect edges

    # integrating edge detection into crosshair
    mira_edges = mira_rotated_with_circle.copy()
    mira_edges[edges != 0] = (0, 255, 0)

    # add current angle to the image
    cv2.putText(mira_edges, f"Angle: {angle}", (315, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)

    # as the name of the variable says, they are the images together, both the webcam and the on-board computer
    combined_image = cv2.hconcat([mira_edges, frame_resized])

    cv2.imshow("Webcam + Mira", combined_image)
    angle += 1
    if angle > 180:
        angle = 0
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()