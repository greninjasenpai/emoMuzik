import pafy
import vlc

ori_list = ["https://www.youtube.com/watch?v=5k6kg---YKg&index=2&list=PLTSIqhWP1gKWbtSaAFCz5erPddH--7D6L","https://www.youtube.com/watch?v=j-Fhx2IEztw"]
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
    while player.get_position()<0.98:
        print(player.get_position())
        
        continue
    player.stop()