# USAGE
# python multi_object_tracking.py --video videos/soccer_01.mp4 --tracker csrt

# import the necessary packages
from imutils.video import VideoStream
import imutils
import time
import cv2
import numpy as np
import math
import os
import csv

dateandtime = []
for file in os.listdir("C:/Users/CoeFamily/Documents/python_awsradar_gui-master/kbox_new"):
    date = file[0:8]
    print("The current date is: " + str(date))
    print("Please press s to select cell(s) to track")
    print("Once you are done, press q to go to next date")
    # initialize a dictionary that maps strings to their corresponding
    # OpenCV object tracker implementations
    OPENCV_OBJECT_TRACKERS = {
        "csrt": cv2.TrackerCSRT_create,
        "kcf": cv2.TrackerKCF_create,
        "boosting": cv2.TrackerBoosting_create,
        "mil": cv2.TrackerMIL_create,
        "tld": cv2.TrackerTLD_create,
        "medianflow": cv2.TrackerMedianFlow_create,
        "mosse": cv2.TrackerMOSSE_create
    }

    # initialize OpenCV's special multi-object tracker
    trackers = cv2.MultiTracker_create()


    vs = cv2.VideoCapture("C:/Users/CoeFamily/Documents/python_awsradar_gui-master/kbox_new/"+file)
    global numpts
    numpts = 0
    # loop over frames from the video stream
    try:
        while(vs.isOpened()):
            # grab the current frame, then handle if we are using a
            # VideoStream or VideoCapture object
            frame = vs.read()
            frame = frame[1]

            # check to see if we have reached the end of the stream
            if frame is None:
                vs = cv2.VideoCapture("C:/Users/CoeFamily/Documents/python_awsradar_gui-master/kbox_new/"+file)
                frame = vs.read()
                frame = frame[1]
                trackers = cv2.MultiTracker_create()

            # resize the frame (so we can process it faster)
            frame = imutils.resize(frame,width=1000)

            # grab the updated bounding box coordinates (if any) for each
            # object that is being tracked
            (success, boxes) = trackers.update(frame)

            # loop over the bounding boxes and draw then on the frame
            tempi = 0
            for box in boxes:
                (x, y, w, h) = [int(v) for v in box]
                
                
                
                if(len(box_save[tempi])>1):
                    if(x == box_save[tempi][-1][0] and y == box_save[tempi][-1][1]):
                        trackers = cv2.MultiTracker_create()
                        break
                    else:
                        box_save[tempi].append(np.array([x,y]))
                        tempi = tempi + 1
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                else:
                    box_save[tempi].append(np.array([x, y]))
                    tempi = tempi + 1
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # show the output frame
            cv2.imshow("Frame", frame)
            time.sleep(0.5)
            key = cv2.waitKey(1) & 0xFF

            # if the 's' key is selected, we are going to "select" a bounding
            # box to track
            if key == ord("s"):
                # select the bounding box of the object we want to track (make
                # sure you press ENTER or SPACE after selecting the ROI)
                box = cv2.selectROI("Frame", frame, fromCenter=False,
                    showCrosshair=True)

                # create a new object tracker for the bounding box and add it
                # to our multi-object tracker
                tracker = OPENCV_OBJECT_TRACKERS["csrt"]()
                trackers.add(tracker, frame, box)
                next = input("select another point? y/n")
                numpts = numpts + 1
                def select_another(ycheck=None):
                    global numpts
                    if(ycheck == 'y'):
                        # select the bounding box of the object we want to track (make
                        # sure you press ENTER or SPACE after selecting the ROI)
                        box = cv2.selectROI("Frame", frame, fromCenter=False,
                                            showCrosshair=True)

                        # create a new object tracker for the bounding box and add it
                        # to our multi-object tracker
                        tracker = OPENCV_OBJECT_TRACKERS["csrt"]()
                        trackers.add(tracker, frame, box)
                        next = input("select another point? y/n")
                        numpts = numpts + 1
                        select_another(next)
                select_another(next)
                box_save = [[0] * 1 for i in range(numpts)]

            # if the `q` key was pressed, break from the loop
            elif key == ord("q"):
                break


        vs.release()
        # close all windows
        cv2.destroyAllWindows()

        #Now calculate the degrees
        dir = []
        for col in range(len(box_save)):
            temp = box_save[col]
            temp.pop(0)
            tempx = []
            tempy = []
            for im in range(len(temp)):
                tempx.append(temp[im][0])
                tempy.append(temp[im][1])
            if(tempx[0] > tempx[-1]):
                pass
            else:
                tempx ,tempy = zip(*sorted(zip(tempx, tempy)))
            x1 = tempx[0]
            x2 = tempx[-1]
            y1 = tempy[0]
            y2 = tempy[-1]
            #Reverse y2-y1 to y1-y2 since y is positive downwards
            if((x2-x1)!=0):
                angle = math.degrees(math.atan((y2-y1)/(x2-x1)))
                if((y2-y1) < 0 and (x2-x1)>0):
                    dir.append(angle+90)
                elif((y2-y1)>0 and (x2-x1)>0):
                    dir.append(angle+90)
                elif((y2-y1)>0 and (x2-x1)<0):
                    dir.append(angle+270)
                else:
                    dir.append(270+angle)
            else:
                pass
        if(np.mean(dir)+180>360):
            dateandtime.append([date,np.mean(dir),np.mean(dir)-180])
        else:
            dateandtime.append([date, np.mean(dir), np.mean(dir) + 180])
        print(np.mean(dir))
        
    except:
        pass

#Direction to will be the second column and direction from is the first column
with open('date_direction_kbox.csv', "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(dateandtime)