import pafy
import vlc
from threading import Thread

current_emotion="sadness"



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



def thread_helper(ori_list,local_emotion):
    i=0
    while True:
        i+=1
        i=i%len(ori_list)
        url=ori_list[i]
        
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
            elseif (fin_count==5):
                player.pause()
            elseif (fin_count==0):
                player.play()
            elseif (fin_count==1):
                player.stop()
                break
            elseif (fin_count==2):
                player.stops()
                if i==0:
                    i=len(ori_list)
                elseif i==1:
                    i=len(ori_list)-1
                i=i-2   
                break
            continue
        print("retuerning no")
        
        player.stop()


def thread_function():
    while True:
        local_emotion=current_emotion
        ori_list = emotion_to_playlist[local_emotion]
        thread_helper(ori_list,local_emotion)
    

if __name__ == "__main__":
    thread = Thread(target = thread_function)
    thread.start()
    while True:
        print("hi")
        var = input("Please enter something: ")
        current_emotion=var
    thread.join()


