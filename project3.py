import numpy as np
import cv2
import math
import imutils

img_before = cv2.imread("./TestCases/test_sample10.jpg")
img_gray = cv2.cvtColor(img_before, cv2.COLOR_BGR2GRAY)
img_edges = cv2.Canny(img_before, 100, 100, apertureSize=3)
lines = cv2.HoughLinesP(img_edges, 1, math.pi / 180.0, 100, minLineLength=100, maxLineGap=5)
angles = []

for x1, y1, x2, y2 in lines[0]:
    cv2.line(img_before, (x1, y1), (x2, y2), (255, 0, 0), 3)
    angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
    angles.append(angle)

median_angle = np.median(angles)
img_rotated = imutils.rotate(img_before, median_angle)
cv2.imwrite("rotated.jpg", img_rotated)

name = "test_sample"
ext = ".jpg"
strings = ["Gender: ", "Semester: ", "Program: ", "1.1 ", "1.2 ", "1.3 ", "1.4 ", "1.5 ", "2.1 ", "2.2 ", "2.3 "
    , "2.4 ", "2.5 ", "2.6 ", "3.1 ", "3.2 ", "3.3 ", "4.1 ", "4.2 ", "4.3 ", "5.1 ", "5.2 "]
gender = ["Male", "Female"]
semester = ["Fall", "Spring", "Summer"]
program = [["MCTA", "ENVR", "BLDG", "CESS", "ERGY", "COMM", "MANF"], ["LAAR", "MATL", "CISE", "HAUD"]]
choices = ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"]
gender_x_coordinates = [376, 416]
gender_y_coordinate = 87
semester_x_coordinates = [166, 246, 326]
semester_y_coordinate = 112
program_x_coordinates = [136, 176, 216, 256, 296, 336, 376]
program_y_coordinates = [136, 148]
choices_x_coordinates = [336, 366, 396, 426, 456]
choices_y_coordinates = [292, 304, 316, 328, 340, 376, 388, 400, 412, 424, 436, 471, 483, 495, 532, 544, 568, 603, 615]
margin = 5
index = 0
scale = 30
height = int(img_rotated.shape[0] * scale / 100)
width = int(img_rotated.shape[1] * scale / 100)
dimensions = (width, height)
img_rotated = cv2.resize(img_rotated, dimensions)
lower = np.array([0, 0, 0])
upper = np.array([15, 15, 15])
shapeMask = cv2.inRange(img_rotated, lower, upper)
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(shapeMask, connectivity=4)
file = open("output.txt", "w")
for i in range(0, num_labels):
    cx = int(centroids[i][0])
    cy = int(centroids[i][1])
    written = False
    if index == 0:
        if abs(cx - gender_x_coordinates[0]) < margin and abs(cy - gender_y_coordinate) < margin:
            file.write(strings[index] + gender[0] + "\n")
            index = index + 1
        elif abs(cx - gender_x_coordinates[1]) < margin and abs(cy - gender_y_coordinate) < margin:
            file.write(strings[index] + gender[1] + "\n")
            index = index + 1
    elif index == 1:
        if abs(cx - semester_x_coordinates[0]) < margin and abs(cy - semester_y_coordinate) < margin:
            file.write(strings[index] + semester[0] + "\n")
            index = index + 1
        elif abs(cx - semester_x_coordinates[1]) < margin and abs(cy - semester_y_coordinate) < margin:
            file.write(strings[index] + semester[1] + "\n")
            index = index + 1
        elif abs(cx - semester_x_coordinates[2]) < margin and abs(cy - semester_y_coordinate) < margin:
            file.write(strings[index] + semester[2] + "\n")
            index = index + 1
    elif index == 2:
        for j in range(len(program_x_coordinates)):
            if abs(cx - program_x_coordinates[j]) < margin:
                for k in range(len(program_y_coordinates)):
                    if abs(cy - program_y_coordinates[k]) < margin:
                        file.write(strings[index] + program[k][j] + "\n")
                        index = index + 1
                        break
                if index == 3:
                    break
    elif index >= 3:
        for l in range(len(choices_x_coordinates)):
            if abs(cx - choices_x_coordinates[l]) < margin:
                for m in range(len(choices_y_coordinates)):
                    if abs(cy - choices_y_coordinates[m]) < margin:
                        file.write(strings[index] + choices[l] + "\n")
                        index = index + 1
                        written = True
                        break
                if written:
                    break
file.close()

# cv2.imshow("Original", src)
# cv2.imshow("Circles", circles)
# cv2.waitKey(0)
# ret, thresh = cv2.threshold(img_rotated, 15, 255, cv2.THRESH_BINARY_INV)
# circles = cv2.HoughCircles(thresh, cv2.HOUGH_GRADIENT, 1, 2, param1=5, param2=2, minRadius=1, maxRadius=5)
# circles = np.round(circles[0, :]).astype("int")
# cv2.imshow("thresh", thresh)
# cv2.waitKey(0)

# kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
# shapeMask = cv2.dilate(shapeMask, kernel)
# for i in range(0, num_labels):
#     print(int(centroids[i][0]), int(centroids[i][1]), " ")
# for i in range(0, num_labels):
#     cx = int(centroids[i][0])
#     cy = int(centroids[i][1])
#     cv2.putText(shapeMask, str(i), (cx - 3, cy + 2), cv2.FONT_HERSHEY_SIMPLEX, 0.25, (0, 0, 255), 1)
#     print(cx, cy)
# cv2.imshow("mask", shapeMask)
# cv2.waitKey(0)
