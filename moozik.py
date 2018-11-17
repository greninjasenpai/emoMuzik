import pafy
import vlc
from threading import Thread

current_emotion="sadness"



contempt_play_list=[]
disgust_play_list=[]
fear_play_list=[]
happiness_play_list=[]
neutral_play_list=[]

sadness_play_list=["https://www.youtube.com/watch?v=N-nn4IdkFek","https://www.youtube.com/watch?v=12SImwAMEUk","https://www.youtube.com/watch?v=IMW0QGEdxmg","https://www.youtube.com/watch?v=9qIIgwmq7-4","https://www.youtube.com/watch?v=K6Ad1_Eq4Q8","https://www.youtube.com/watch?v=UoZP3L03Rfo","https://www.youtube.com/watch?v=5BM6bGkmNY8"]

surprise_play_list=["https://www.youtube.com/watch?v=GFegrI8AFUc","https://www.youtube.com/watch?v=JQSlA3pkViw","https://www.youtube.com/watch?v=36Gl8JMA7K0","https://www.youtube.com/watch?v=Kbi8CIGQ35w","https://www.youtube.com/watch?v=I8tespYBHGU","https://www.youtube.com/watch?v=sBjN0cgko6Q","https://www.youtube.com/watch?v=_5rFL8dtjuY","https://www.youtube.com/watch?v=S6JoSF_xyo0"]
anger_play_list=[]

emotion_to_playlist={
        "anger":anger_play_list,
        "contempt":contempt_play_list,
        "disgust":disgust_play_list,
        "fear":fear_play_list,
        "happiness":happiness_play_list,
        "neutral":neutral_play_list,
        "sadness":sadness_play_list,
        "surprise":surprise_play_list
}


def thread_function():
    local_emotion=current_emotion
    ori_list = emotion_to_playlist[local_emotion]
    for url in ori_list: 
        # if the current emotion changes, upadte the playlist
        if local_emotion != current_emotion:
            local_emotion=current_emotion
            ori_list = emotion_to_playlist[local_emotion]
            continue
        
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
                local_emotion=current_emotion
                ori_list = emotion_to_playlist[local_emotion]
                break
            continue
        player.stop()

if __name__ == "__main__":
    thread = Thread(target = thread_function)
    thread.start()
    while True:
        var = input("Please enter something: ")
        current_emotion=var


