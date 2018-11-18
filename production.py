import cv2
import numpy as np
import pyscreenshot as ImageGrab
import http.client, urllib.request, urllib.parse, urllib.error, base64
import time
import pafy
import vlc
from threading import Thread
import json
import copy
import math



nex_flag=0
prev_flag=0
bgModel = None
test_var=0
#from appscript import app

# Environment:
# OS    : Mac OS EL Capitan
# python: 3.5
# opencv: 2.4.13

# parameters
# export PYTHONPATH="${PYTHONPATH}:/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages"

cap_region_x_begin=0.5  # start point/total width
cap_region_y_end=0.5  # start point/total width
threshold = 60  #  BINARY threshold
blurValue = 41  # GaussianBlur parameter
bgSubThreshold = 50
learningRate = 0

# variables
isBgCaptured = 0   # bool, whether the background captured
triggerSwitch = False  # if true, keyborad simulator works

def printThreshold(thr):
    print("! Changed threshold to "+str(thr))


def removeBG(frame):
    fgmask = bgModel.apply(frame,learningRate=learningRate)
    # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    # res = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

    kernel = np.ones((3, 3), np.uint8)
    fgmask = cv2.erode(fgmask, kernel, iterations=1)
    res = cv2.bitwise_and(frame, frame, mask=fgmask)
    return res


def calculateFingers(res,drawing):  # -> finished bool, cnt: finger count
    #  convexity defect
    hull = cv2.convexHull(res, returnPoints=False)
    if len(hull) > 3:
        defects = cv2.convexityDefects(res, hull)
        if type(defects) != type(None):  # avoid crashing.   (BUG not found)

            cnt = 0
            for i in range(defects.shape[0]):  # calculate the angle
                s, e, f, d = defects[i][0]
                start = tuple(res[s][0])
                end = tuple(res[e][0])
                far = tuple(res[f][0])
                a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))  # cosine theorem
                if angle <= math.pi / 2:  # angle less than 90 degree, treat as fingers
                    cnt += 1
                    cv2.circle(drawing, far, 8, [211, 84, 0], -1)
            return True, cnt
    return False, -1


global_frame=None


########################################global variables for the music player#############################
current_emotion="neutral"

fin_count=-1

contempt_play_list=[]
disgust_play_list=[]
fear_play_list=["https://www.youtube.com/watch?v=UI2WuKFX7u0","https://www.youtube.com/watch?v=f8fUFmjqXZo","https://www.youtube.com/watch?v=0ewQiU3q5jM","https://www.youtube.com/watch?v=kVpPlWlHMrA","https://www.youtube.com/watch?v=wVodyoHhNto","https://www.youtube.com/watch?v=WcuRkaqxEAU"]
happiness_play_list=["https://www.youtube.com/watch?v=WTht2pC-9AA","https://www.youtube.com/watch?v=wnJ6To0qkBU","https://www.youtube.com/watch?v=q0GrB07rBSk","https://www.youtube.com/watch?v=kEqPDKPoY3g","https://www.youtube.com/watch?v=NtPVFyqjUoo"]
neutral_play_list=["https://www.youtube.com/watch?v=hR5lIKHLuPA","https://www.youtube.com/watch?v=nPjvp5u0UN8","https://www.youtube.com/watch?v=CcYq0aeTBr4","https://www.youtube.com/watch?v=Ptt_WQk4Yt8","https://www.youtube.com/watch?v=87wAZbQWsko"]

sadness_play_list=["https://www.youtube.com/watch?v=12SImwAMEUk","https://www.youtube.com/watch?v=IMW0QGEdxmg","https://www.youtube.com/watch?v=9qIIgwmq7-4","https://www.youtube.com/watch?v=K6Ad1_Eq4Q8","https://www.youtube.com/watch?v=UoZP3L03Rfo","https://www.youtube.com/watch?v=5BM6bGkmNY8"]

surprise_play_list=["https://www.youtube.com/watch?v=GFegrI8AFUc","https://www.youtube.com/watch?v=JQSlA3pkViw","https://www.youtube.com/watch?v=36Gl8JMA7K0","https://www.youtube.com/watch?v=Kbi8CIGQ35w","https://www.youtube.com/watch?v=I8tespYBHGU","https://www.youtube.com/watch?v=sBjN0cgko6Q","https://www.youtube.com/watch?v=_5rFL8dtjuY","https://www.youtube.com/watch?v=S6JoSF_xyo0"]
anger_play_list=[]

emotion_to_playlist={
        "anger":neutral_play_list,
        "contempt":neutral_play_list,
        "disgust":neutral_play_list,
        "fear":fear_play_list,
        "happiness":happiness_play_list,
        "neutral":neutral_play_list,
        "sadness":sadness_play_list,
        "surprise":surprise_play_list
}

########################################global variables for the music player end########################################


########################################## global variables for the assure framework ###################################
headers = {
    # Request headers
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': '4c8334d694de4146a748230788ad2f49',
}

params = urllib.parse.urlencode({
    # Request parameters
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,emotion',
})

########################################## global variables for the assure framework end ###################################

################################## music functions #################################
def thread_helper(ori_list,local_emotion):
    global fin_count
    i=0
    while True:
        i+=1
        i=i%len(ori_list)
        url=ori_list[i]

        # print("url={}".format(url))
        
        # print("local emotrion {}".format(local_emotion))
        # print(ori_list)
        # if the current emotion changes, upadte the playlist
        if local_emotion != current_emotion:
            player.stop()
            return
        
        # setup the video
        video = pafy.new(url)
        best = video.getbest()
        playurl = best.url
        Instance = vlc.Instance()
        player = Instance.media_player_new()
        Media = Instance.media_new(playurl)
        Media.get_mrl()
        player.set_media(Media)
        player.play()

        while player.get_position()<0.98:
            if local_emotion != current_emotion:
                print(local_emotion)
                print("retuerning")
                player.stop()
                return
            #pause
            elif (fin_count>=3):
                player.pause()

            #play
            elif (fin_count<3):
                fin_count=-1
                player.play()

            # # next
            # elif (fin_count==3):
            #     player.stop()
            #     fin_count=-1
            #     break

            # #previous
            # elif (fin_count==2):
            #     player.stop()

            #     if i==0:
            #         i=len(ori_list)

            #     elif i==1:
            #         i=len(ori_list)-1

            #     i=i-2  
            #     fin_count=-1
            #     break

            continue
        print("retuerning no")
        
        player.stop()


def thread_function():
    global current_emotion
    print("hbdjhvb")
    print(current_emotion)
    while True:
        local_emotion=current_emotion
        ori_list = emotion_to_playlist[local_emotion]
        print(ori_list,local_emotion)
        thread_helper(ori_list,local_emotion)
################################## music functions end #################################



######################################### Get_top_emotion #################################
# returns the max emortion in the json response, rejects neutral if it is less than 80%
def Get_top_emotion_helper(data):
    global current_emotion
    try:
        dict1=data[0]["faceAttributes"]["emotion"]
        max=0
        max_emotion=""
        for item in dict1:
            confideance=dict1[item]
            if confideance>max:
                if item=="neutral":
                    if confideance>0.8:
                        max_emotion=item
                        max=confideance
                else:
                    max_emotion=item
                    max=confideance
        return(max_emotion)
    except:
        return current_emotion
    
# does and assure api call and returns the top emotion
def Get_top_emotion(frame):
    global current_emotion
    retval, encoded_image = cv2.imencode('.jpeg', frame)
    # encoded_image = np.array(encoded_image)
    stringData = encoded_image.tostring()

    try:
        conn = http.client.HTTPSConnection('westus2.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/detect?%s" % params, stringData, headers)
        response = conn.getresponse()
        data = response.read()
        data_json=json.loads(data)
        print(data_json)
        current_emotion=Get_top_emotion_helper(data_json)
        print("current emotion changes!!!!!! to {}".format(current_emotion))
        conn.close()
        
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
######################################### Get_top_emotion end#################################





######################################## main_loop ###########################################
def main_loop():
    global global_frame
    assure_capture = cv2.VideoCapture(0)
    assure_capture.set(10,200)
    sz = (int(assure_capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(assure_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    fps = assure_capture.get(cv2.CAP_PROP_FPS)
    print(fps)
    #fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    #fourcc = cv2.VideoWriter_fourcc('m', 'p', 'e', 'g')
    fourcc = cv2.VideoWriter_fourcc(*'mpeg')

    # ## open and set props
    # vout = cv2.VideoWriter()
    # vout.open('output.mp4',fourcc,fps,sz,True)

    start_time=time.time()-3
    _, global_frame = assure_capture.read()
    while(True):
        current_time=time.time()
        _, global_frame = assure_capture.read()



        # emotion detections
        # only run after after 3 seconds
        # print(current_time-start_time)
        if current_time-start_time>3:
            start_time=current_time
            Get_top_emotion(global_frame)
            # cv2.imshow('global_frame', global_frame)
            # vout.write(global_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            out = cv2.imwrite('capture.jpg', global_frame)
            break
    # vout.release()

    assure_capture.release()
    cv2.destroyAllWindows()
######################################## main_loop end ###########################################


def getsture_reco():

    time.sleep(2)
    trial_var = 0
    global bgModel
    global fin_count
    bgModel = cv2.createBackgroundSubtractorMOG2(0, bgSubThreshold)
    isBgCaptured = 1
    print( '!!!Background Captured!!!')
    while True:
        global global_frame
        frame = global_frame
        threshold = 30
        frame = cv2.bilateralFilter(frame, 5, 50, 100)  # smoothing filter
        frame = cv2.flip(frame, 1)  # flip the frame horizontally
        cv2.rectangle(frame, (int(cap_region_x_begin * frame.shape[1]), 0),
                    (frame.shape[1], int(cap_region_y_end * frame.shape[0])), (255, 0, 0), 2)
        # cv2.imshow('original', frame)

        #  Main operation
        if isBgCaptured == 1:  # this part wont run until background captured
            img = removeBG(frame)
            img = img[0:int(cap_region_y_end * frame.shape[0]),
                        int(cap_region_x_begin * frame.shape[1]):frame.shape[1]]  # clip the ROI
            # cv2.imshow('mask', img)

            # convert the image into binary image
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (blurValue, blurValue), 0)
            # cv2.imshow('blur', blur)
            ret, thresh = cv2.threshold(blur, threshold, 255, cv2.THRESH_BINARY)
            # cv2.imshow('ori', thresh)

            # get the coutours
            thresh1 = copy.deepcopy(thresh)
            _,contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            length = len(contours)
            maxArea = -1
            if length > 0:
                for i in range(length):  # find the biggest contour (according to area)
                    temp = contours[i]
                    area = cv2.contourArea(temp)
                    if area > maxArea:
                        maxArea = area
                        ci = i

                res = contours[ci]
                hull = cv2.convexHull(res)
                drawing = np.zeros(img.shape, np.uint8)
                # cv2.drawContours(drawing, [res], 0, (0, 255, 0), 2)
                # cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 3)

                isFinishCal,cnt = calculateFingers(res,drawing)
                trial_var = cnt
                # print (trial_var)

                # if triggerSwitch is True:
                #     if isFinishCal is True and cnt <= 2:
                #         print (cnt)
                        #app('System Events').keystroke(' ')  # simulate pressing blank space
                        
            print (trial_var)
            fin_count=trial_var
            # cv2.imshow('output', drawing)

 


if __name__ == "__main__":

    
# cv2.namedWindow('trackbar')
# cv2.createTrackbar('trh1', 'trackbar', threshold, 100, printThreshold)
 
  
   

    thread_gestture=Thread(target= getsture_reco)
    thread = Thread(target = thread_function)
    thread.start()
    thread_gestture.start()
    main_loop()
    thread.join()