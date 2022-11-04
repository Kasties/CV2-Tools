import cv2
import numpy as np
import os

run = False

def make_mask(img_path,name,c_pos):
    mask_path = ""
    img_path = ""
    txt_path = ""
    points = []
    def draw(event, x, y,_,__):
        global run
        ix=x
        iy=y
        if event == cv2.EVENT_LBUTTONDOWN:
            run = True
            cv2.line(img,(ix,iy),(x,y),(255,255,255),5)
            cv2.line(mask,(ix*int(new_size[0]),iy*int(new_size[1])),(x*int(new_size[0]),y*int(new_size[1])),(255,255,255),5)

        if event == cv2.EVENT_LBUTTONUP:
            run = False
        if event == cv2.EVENT_RBUTTONDBLCLK:
            run = False

        if event == cv2.EVENT_MOUSEMOVE:
            if run == True:
                cv2.line(img,(ix,iy),(x,y),(255,255,255),5)
                print(new_size[0])
                cv2.line(mask,(ix*int(new_size[0]),iy*int(new_size[1])),(x*int(new_size[0]),y*int(new_size[1])),(255,255,255),5)
    def get_rekt_cords(event,x,y,_,__):
        if event == cv2.EVENT_LBUTTONUP:
            run = False
        if event == cv2.EVENT_LBUTTONDOWN:
            run = True
            if run == True:
                print("clicked")
                points.append((x,y))
    def draw_ret(cords):
        for i in range(len(cords)-1):
            cv2.line(img, cords[i], cords[i+1],
                                (255, 255, 255), 155)
            cv2.line(mask,cords[i],cords[i+1],(255,255,255),5)
        cv2.line(img, cords[0], cords[-1],
                            (255, 255, 255), 155)
        cv2.line(mask,cords[0],cords[-1],(255,255,255),5)

    
    cv2.namedWindow('window')


    img = cv2.imread(img_path)
    img2 = img.copy()
    mask = np.zeros(img.shape, dtype='float64')
    w = img.shape[1]
    h = img.shape[0]
    top_left =  img[0:int(h*0.1), 0:int(w*0.1)]
    bot_right = img[int(h*0.8):h, int(w*0.75):w]
    top_right = img[0:int(h*0.95), int(w*0.75):w]
    bot_left = img[int(h*0.8):h, 0:int(0.15*w)]
    corners = [top_left,top_right,bot_right,bot_left]
    adjuster = [img[0:0, 0:0].shape[:-1],
    img[0:int(w*0.75), h:h].shape[:-1],
    img[0:int(w*0.75), int(h*0.2):h].shape[:-1],
    img[0:0, int(h*0.2):h].shape[:-1]]

    if choice == "a":
        cv2.setMouseCallback('window', get_rekt_cords)
        for c in corners:
            cv2.imshow('window', c)
            cv2.waitKey(0)
        for i in range(len(points)):
            points[i] = tuple(map(sum, zip(points[i], adjuster[i])))
        draw_ret(points)

    else:

        cv2.setMouseCallback('window', draw)
    global new_size
    new_size = (h/900,w/900)

    img = cv2.resize(img,(900,900))

    while True:
        cv2.imshow('window', img)
        k = cv2.waitKey(1)

        if k == ord('n'):
            c_pos += 1
            with open(txt_path, "w") as f:
                f.write(str(c_pos))
            break
        if k == ord('r'):
            with open(txt_path, "w") as f:
                f.write(str(0))
            break
        if k == ord('s'):
            c_pos += 1
            with open(txt_path, "w") as f:
                f.write(str(c_pos))
            cv2.imwrite(str(mask_path) + "/" +"mask"+ name[:-3]+ "png",mask)
            cv2.imwrite(str(img_path)  + "/" +name[:-3]+ "png",img2)
            break
        if k == 27:
            print(c_pos)
            cv2.destroyAllWindows()
            cv2.imwrite(str(mask_path)  + "/" +"mask"+ name[:-3] +"png",mask)
            cv2.imwrite(str(img_path)  + "/" +name[:-3] + "png",img2)
            with open("blackl/place.txt", "w") as f:
                f.write(str(c_pos))

            quit()
rootdir = ""
choice = input()

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        with open(str(txt_path), "r") as f:
            c_pos = int(f.readlines()[0])
        make_mask((rootdir +"/"+files[c_pos]),file,c_pos)
