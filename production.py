import cv2
import numpy as np
import pyscreenshot as ImageGrab
import http.client, urllib.request, urllib.parse, urllib.error, base64
import time
import pafy
import vlc
from threading import Thread



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
        print("up")
        i+=1
        i=i%len(ori_list)
        url=ori_list[i]

        print("url={}".format(url))
        
        print("local emotrion {}".format(local_emotion))
        print(ori_list)
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
                print("retuerning")
                player.stop()
                return

            elif (fin_count==4):
                player.pause()

            elif (fin_count==1):
                fin_count=-1
                player.play()

            # next
            elif (fin_count==3):
                player.stop()
                fin_count=-1
                break

            elif (fin_count==2):
                player.stop()

                if i==0:
                    i=len(ori_list)

                elif i==1:
                    i=len(ori_list)-1

                i=i-2  
                fin_count=-1
                break
            continue
        print("retuerning no")
        
        player.stop()


def thread_function():
    while True:
        local_emotion=current_emotion
        ori_list = emotion_to_playlist[local_emotion]
        thread_helper(ori_list,local_emotion)
################################## music functions end #################################



######################################### Get_top_emotion #################################
# returns the top emotion
def Get_top_emotion(frame):
    retval, encoded_image = cv2.imencode('.jpeg', frame)
    # encoded_image = np.array(encoded_image)
    stringData = encoded_image.tostring()

    try:
        conn = http.client.HTTPSConnection('westus2.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/detect?%s" % params, stringData, headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
        conn.close()
        
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
######################################### Get_top_emotion end#################################





######################################## main_loop ###########################################
def main_loop():
    cap = cv2.VideoCapture(0)
    sz = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    fps = cap.get(cv2.CAP_PROP_FPS)
    print(fps)
    #fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    #fourcc = cv2.VideoWriter_fourcc('m', 'p', 'e', 'g')
    fourcc = cv2.VideoWriter_fourcc(*'mpeg')

    ## open and set props
    vout = cv2.VideoWriter()
    vout.open('output.mp4',fourcc,fps,sz,True)

    start_time=time.time()-3
    while(True):
        current_time=time.time()

        _, frame = cap.read()

        # after 3 seconds
        print(current_time-start_time)
        if current_time-start_time>3:
            start_time=current_time
            Get_top_emotion(frame)


        vout.write(frame)
        
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            out = cv2.imwrite('capture.jpg', frame)
            break
    vout.release()

    cap.release()
    cv2.destroyAllWindows()
######################################## main_loop end ###########################################



if __name__ == "__main__":
    thread = Thread(target = thread_function)
    thread.start()
    main_loop()
    thread.join()