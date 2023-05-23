#!/usr/bin/env python3
import os
import sys
import cv2
import numpy as np

GREEN = (0,255,0)
RED = (0, 0, 255)
BLUE = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def find_pixel(contours):
    # Find the size of a small rectangle
    blockw=9999
    for c in contours:
        if len(c) > 4:
            continue
        x, y, w, h = cv2.boundingRect(c)
        w = max(w, h)
        # Find smallest rectangle
        blockw = min(blockw, w)
    blockw += 1
    return blockw

def is_black(mask, blockw, x, y):
    # Can't get this to work
    mysum = 0
    THRESH = blockw**2 * 0.55
    for i in range(0, blockw):
        for j in range(0, blockw):
            x_ = int(x+i)
            y_ = int(y+j)
            # print(x_, y_, mask[x_, y_], img[x_, y_])
            if np.all(mask[x_, y_] > 250):
                mysum += 1
    if mysum > THRESH:
        print("BLACK CORNER", mysum)
        return True
    return False

def add_corner_square(img, mask, blockw, x, y, color):
    if is_black(mask, blockw, x, y):
        pass
    cv2.rectangle(img,
                pt1=(x, y),
                pt2=(x+blockw, y+blockw),
                color=color,
                thickness=-1)


filename = "test.png"
filename = "ticket_orig.png"
img = cv2.imread(filename)
# img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgray_i = cv2.bitwise_not(imgray)

_, mask = cv2.threshold(imgray, 127, 255, cv2.THRESH_BINARY)
imask = cv2.bitwise_not(mask)

contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
icontours, hierarchy = cv2.findContours(imask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

contours = list(contours)
icontours = list(icontours)
contours.pop() # Bounding box is last
icontours.pop() # Bounding box is last

# contours = contours[70:75]
# indexes = [74] # 63
# contours =  list(map(contours.__getitem__, indexes))

w =  img.shape[0]
w = max(w, img.shape[1])
w3 = w/3.5
central = [w3, w3*2, w3, w3*2]

blockw = find_pixel(contours)

# cv2.drawContours(img, contours, -1, GREEN, 1)
for c in contours:
    x = c[0][0][0]
    y = c[0][0][1]
    if central[0] < x < central[1] and central[2] < y < central[3]:
        continue
    add_corner_square(img, mask, blockw, x, y, WHITE)

for c in icontours:
    x = c[0][0][0]
    y = c[0][0][1]
    if central[0] < x < central[1] and central[2] < y < central[3]:
        continue
    add_corner_square(img, mask, blockw, x, y, BLACK)


out = "foo.png"
if os.path.exists(out):
    os.remove(out)
cv2.imwrite(out, mask)

out = "foo2.png"
if os.path.exists(out):
    os.remove(out)
cv2.imwrite(out, img)
sys.exit()

w =  img.shape[0]
w = max(w, img.shape[1])
w3 = w/3.5
central = [w3, w3*2, w3, w3*2]

# Add a small rectangle at the start of each contour
for c in contours:
    x, y, w, h = cv2.boundingRect(c)
    if central[0] < x < central[1] and central[2] < y < central[3]:
        continue
    if is_black(img, blockw, x, y):
        continue
    cv2.rectangle(img,
                  pt1=(x, y),
                  pt2=(x+blockw, y+blockw),
                  color=(0, 255, 0),
                  thickness=-1)

# blank out the corners of the original contours
for c in icontours:
    x, y, w, h = cv2.boundingRect(c)
    if central[0] < x < central[1] and central[2] < y < central[3]:
        continue
    if is_black(img, blockw, x, y):
        continue
    cv2.rectangle(img,
                  pt1=(x, y),
                  pt2=(x+blockw, y+blockw),
                  color=(255, 0, 0),
                  thickness=-1)


cv2.imwrite("foo.png", img)

sys.exit()
detect = cv2.QRCodeDetector()
value, points, straight_qrcode = detect.detectAndDecode(img)
print(value)
print(points)
print(straight_qrcode)
