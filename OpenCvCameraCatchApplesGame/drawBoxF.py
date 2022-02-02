import cv2 as cv

def drawBox(img, bbox):
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    cv.rectangle(img, (x, y), ((x+w), (y+h)), (255, 0, 255), 3, 1)
    cv.putText(img, "Tracing", (75, 75), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

