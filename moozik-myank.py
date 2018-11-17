import pafy
import vlc

sad_moozik=["https://www.youtube.com/watch?v=N-nn4IdkFek","https://www.youtube.com/watch?v=12SImwAMEUk","https://www.youtube.com/watch?v=IMW0QGEdxmg","https://www.youtube.com/watch?v=9qIIgwmq7-4","https://www.youtube.com/watch?v=K6Ad1_Eq4Q8","https://www.youtube.com/watch?v=UoZP3L03Rfo","https://www.youtube.com/watch?v=5BM6bGkmNY8"]
adv_moozik=["https://www.youtube.com/watch?v=GFegrI8AFUc","https://www.youtube.com/watch?v=JQSlA3pkViw","https://www.youtube.com/watch?v=36Gl8JMA7K0","https://www.youtube.com/watch?v=Kbi8CIGQ35w","https://www.youtube.com/watch?v=I8tespYBHGU","https://www.youtube.com/watch?v=sBjN0cgko6Q","https://www.youtube.com/watch?v=_5rFL8dtjuY","https://www.youtube.com/watch?v=S6JoSF_xyo0"]


ori_list = adv_moozik
for url in ori_list:
    video = pafy.new(url)
    best = video.getbest()
    playurl = best.url
    Instance = vlc.Instance()
    player = Instance.media_player_new()
    Media = Instance.media_new(playurl)
    Media.get_mrl()
    player.set_media(Media)
    player.play()
    while player.get_position()<0.1:
        print(player.get_position())
        
        continue
    player.stop()