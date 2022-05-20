import cv2
import numpy as np
import time

def rgb_to_hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    cmax = max(r, g, b) 
    cmin = min(r, g, b) 
    diff = cmax-cmin       
    if cmax == cmin:
        h = 0
    elif cmax == r:
        h = (60*((g-b)/diff)+360)%360
    elif cmax == g:
        h = (60*((b-r)/diff)+120)%360
    elif cmax == b:
        h = (60*((r-g)/diff)+240)%360
    if cmax == 0:
        s = 0
    else:
        s = (diff/cmax)*100
    v = cmax*100
    return int(h/2), int(s), int(v)

def mouseRGB(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        colorsB = image[y,x,0]
        colorsG = image[y,x,1]
        colorsR = image[y,x,2]
        hsv = rgb_to_hsv(colorsR, colorsG, colorsB)

        low_red[0] = hsv[0]-10
        high_red[0] = hsv[0]+10
        low_red[1] = 100
        high_red[1] = 255
        low_red[2] = 100
        high_red[2] = 255
        
def nothing(x):
    pass

cam = cv2.VideoCapture(0)
global hsv 
prev_frame_time = 0 
new_frame_time = 0
low_red = np.array([160, 100, 100])
high_red = np.array([179, 255, 255])
width = cam.get(cv2.CAP_PROP_FRAME_WIDTH )
height = cam.get(cv2.CAP_PROP_FRAME_HEIGHT )
width = int(width)
height = int(height)
intwidth = int(width/3)
intheight = int(height/2)
dikey1 = intwidth
dikey2 = 2*intwidth
yatay1 = intheight

cv2.namedWindow('mouseRGB')
cv2.createTrackbar("Doygunluk", "mouseRGB",100,255, nothing)
cv2.createTrackbar("Parlaklik", "mouseRGB",100,255, nothing)
cv2.createTrackbar('Black/White', "mouseRGB",2,2,nothing)
cv2.createTrackbar("Dikey1", "mouseRGB",intwidth,width,nothing)
cv2.createTrackbar("Dikey2", "mouseRGB",2*intwidth,width,nothing)
cv2.createTrackbar("Yatay1", "mouseRGB",intheight,height,nothing)

while(True):
    ret, image = cam.read()

    deger = cv2.getTrackbarPos("Black/White","mouseRGB")
    if(deger == 0):
        low_red = np.array([0, 0, 0])#black
        high_red = np.array([179, 255, 100])
        low_red[1] = cv2.getTrackbarPos("Doygunluk","mouseRGB")
        low_red[2] = cv2.getTrackbarPos("Parlaklik","mouseRGB")
    elif(deger == 1):
        low_red = np.array([0,0,168])#white
        high_red = np.array([160,111,255])
        low_red[1] = cv2.getTrackbarPos("Doygunluk","mouseRGB")
        low_red[2] = cv2.getTrackbarPos("Parlaklik","mouseRGB")
    elif(deger == 2):
        cv2.setMouseCallback('mouseRGB',mouseRGB)
        low_red[1] = cv2.getTrackbarPos("Doygunluk","mouseRGB")
        low_red[2] = cv2.getTrackbarPos("Parlaklik","mouseRGB")
    
    hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    maskeleme=cv2.inRange(hsv,low_red,high_red)

    blur = cv2.GaussianBlur(maskeleme,(5,5),cv2.BORDER_DEFAULT)
    opening5 = cv2.morphologyEx(blur.astype(np.float32),cv2.MORPH_OPEN,np.ones((5,5),dtype=np.uint8))
    opening7 = cv2.morphologyEx(opening5.astype(np.float32),cv2.MORPH_OPEN,np.ones((7,7),dtype=np.uint8))
    bw = cv2.threshold(opening7, 128, 255, cv2.THRESH_BINARY)[1]

    new_frame_time = time.time()
    fps = 1/(new_frame_time-prev_frame_time)
    prev_frame_time = new_frame_time
    fps = int(fps)
    cv2.putText(image, str(fps), (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)

    dikey1 = cv2.getTrackbarPos("Dikey1", "mouseRGB")
    dikey2 = cv2.getTrackbarPos("Dikey2", "mouseRGB")
    yatay1 = cv2.getTrackbarPos("Yatay1", "mouseRGB")

    
    p11 = bw[0:yatay1,0:dikey1]
    p12 = bw[0:yatay1,dikey1:dikey2]
    p13 = bw[0:yatay1,dikey2:width]
    p21 = bw[yatay1:height,0:dikey1]
    p22 = bw[yatay1:height,dikey1:dikey2]
    p23 = bw[yatay1:height,dikey2:width]

    cv2.line(bw, (0, yatay1), (width, yatay1), (204, 255, 255), 5)
    cv2.line(bw, (dikey1, 0), (dikey1, height), (204, 255, 255), 5)
    cv2.line(bw, (dikey2, 0), (dikey2, height), (204, 255, 255), 5)

    bolge = [0,0,0,0,0,0]
    if((p11 == 255).any() == True):
        bolge[0] = 1
    if((p12 == 255).any() == True):
        bolge[1] = 1
    if((p13 == 255).any() == True):
        bolge[2] = 1
    if((p21 == 255).any() == True):
        bolge[3] = 1
    if((p22 == 255).any() == True):
        bolge[4] = 1
    if((p23 == 255).any() == True):
        bolge[5] = 1

    print(bolge)

    cv2.imshow("bw",bw)
    cv2.imshow('mouseRGB', image)

    if cv2.waitKey(1) == 27:
        break

cam.release()
cv2.destroyAllWindows()


