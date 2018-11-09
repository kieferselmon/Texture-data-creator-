import cv2
import argparse
import random
import os

#reference points and boolean telling us if we are currently cropping
pts      = []
sel_pt   = []
cropping = False


def mince(box, sign, f, texture):
    global shape
    height = int(box.shape[0]/shape[0])
    print height
    width  = int(box.shape[1]/shape[1])
    print width 
    for i in range(height):
        for j in range(width):
            cell = box[i*shape[0]:(i+1)*shape[0], j*shape[1]:(j+1)*shape[1]]
            if sign == 1:
                cv2.imwrite("./" + str(texture) + "/" + os.path.splitext(f)[0] + "_" + str(random.randint(0,10000)) + ".jpg", cell)
            elif sign == -1:
                cv2.imwrite("./not_" + str(texture) + "/" + os.path.splitext(f)[0] + "_" + str(random.randint(0,10000)) + ".jpg", cell)


def draw_box(event, x, y, flags, param):
    global pts, cropping, sel_pt
    
    #if left button goes down
    if event == cv2.EVENT_LBUTTONDOWN and cropping == False:
        pts      = [(x,y)]
        sel_pt   = pts
        cropping = True
    
    #draw while we are holding the mouse down
    elif event == cv2.EVENT_MOUSEMOVE and cropping == True:
        sel_pt = [(x,y)]

    #left button up
    elif event == cv2.EVENT_LBUTTONUP:
        pts.append((x,y))
        cropping = False
        
        cv2.rectangle(img, pts[0], pts[1], (0,255,0), 1)
        cv2.imshow("img", img)


#command line parsing
parser = argparse.ArgumentParser()
parser.add_argument('file')
parser.add_argument('texture')
parser.add_argument('width')
parser.add_argument('height')
args = parser.parse_args()

shape    = (int(args.height), int(args.width))
texture  = args.texture

#initialize img
img = cv2.imread(args.file)
clean_img = img.copy()
cv2.namedWindow('img')
cv2.setMouseCallback('img', draw_box)

while(1):
    
    #draw the image
    if not cropping:
        cv2.imshow('img', img)
    elif cropping:
        clone = img.copy()
        cv2.rectangle(clone, pts[0], sel_pt[0] ,(0,255,0), 2)
        cv2.imshow("img", clone)
    
    if cv2.waitKey(0) & 0xFF  == 49:
        cell = clean_img[pts[0][1] : pts[1][1], pts[0][0] : pts[1][0]]
        mince(cell, 1, args.file, texture)
    elif cv2.waitKey(0) & 0xFF  == 50:
        cell = clean_img[pts[0][1] : pts[1][1], pts[0][0] : pts[1][0]]
        mince(cell, -1, args.file, texture)
    elif cv2.waitKey(0) & 0xFF == 27:
        break

cv2.destroyAllwindows()
