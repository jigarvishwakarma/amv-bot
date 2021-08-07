#It works
from moviepy.editor import *
import random
import os 
import pafy
import datetime

# variables
SAVE_PATH = os.getcwd()
video_path = str(SAVE_PATH+'/amvbot.mp4')
audio_path = str(SAVE_PATH+'/amvbot.m4a')

# reseting
try:
    os.remove(video_path)
    os.remove(audio_path)
except:
    print("nothing to reset")

# input
def take_yt_link(value):
    link=""
    while(link==""):
        link=input("Enter YouTube link for "+value+" : ")
        if link=="":
            print("dude plz paste the link :D\n")
    return link

def pafyd(link,flag):
	v = pafy.new(link)
	audiostreams = v.audiostreams
	best = v.getbest()
	bestaudio = v.getbestaudio()
	if flag==1:
		bestaudio.download(filepath='amvbot.m4a')
	best.download(quiet=False, filepath='amvbot.mp4')
	return v.title

def coverting_time_to_sec(time_str):
    try:
        m,s = time_str.split(':')
    except ValueError:
        h,m,s = time_str.split(':')
        return int(h) * 3600 + int(m) * 60 + int(s)
    return int(m) * 60 + int(s)

link = take_yt_link("video")
edited_video_name ='output'+str(random.random()).replace(".","--")

video_title = pafyd(link,0)

try:
    try:
        clip0 = VideoFileClip(SAVE_PATH+"/amvbot.mp4")
    except:
        clip0 = VideoFileClip(SAVE_PATH+"/"+video_title+".webm")

except:
    downloaded_video_name = input("Enter downloaded video name: ")
    
    try:
        clip0 = VideoFileClip(SAVE_PATH+"/"+downloaded_video_name+".mp4")
    except:
        clip0 = VideoFileClip(SAVE_PATH+"/"+downloaded_video_name+".webm")

audio_title = pafyd(take_yt_link("audio"),1)

try:
    try:
       aud0 =AudioFileClip(SAVE_PATH+"/amvbot.mp3") 
    except:
        aud0 =AudioFileClip(SAVE_PATH+"/amvbot.m4a")
except:
    downloaded_audio_name = input("Enter downloaded audio name: ")
    try:
       aud0 =AudioFileClip(SAVE_PATH+"/"+downloaded_audio_name+".webm") 
    except:
        aud0 =AudioFileClip(SAVE_PATH+"/"+downloaded_audio_name+".mp3")
      
finalvideo=[]
toatal_len =0 
prev_total = 0
duration = 50

start_value = 1
void = 14
audio_start = 48

auto_void = 0
if int(clip0.duration) < 180:
    auto_void = int(clip0.duration/13)
    void = auto_void
    print("[!]video's duration is less than 3 min.. so void is changed to {}".format(void))
else:
    auto_void = void
is_customize = input("Enter y or yes to cutomize the video : ")

if is_customize in ("y","Y","YES","yes","Yes","YEs","yeah","si","ha"):
    print("[!]Please enter values in (min:sec) or (sec) format only")
    start_value = input("Enter start_time: ")
    if start_value=="":
        start_value =1
    if ":" in str(start_value):
        start_value = coverting_time_to_sec(start_value) 

    void = input("Enter void: ")
    if void=="":
        void = auto_void
    if ":" in str(void):
        void = coverting_time_to_sec(void)

    audio_start = input("Enter audio_start: ")
    if audio_start=="":
        audio_start = 48
    if ":" in str(audio_start):
        audio_start = coverting_time_to_sec(audio_start)
    print("(customized) start_value = {} \n(customized) void = {} \n(customized) audio_start = {}".format(start_value,void,audio_start))
else:
    print("(default) start_value = {} \n(default) void = {} \n(default) audio_start = {}".format(start_value,void,audio_start))
start_value= int(start_value)
void = int(void)
audio_start = int(audio_start)

end_value = start_value+void
print(start_value,end_value)
while(toatal_len<=duration):
	r =  random.randrange(3, 6, 1)
	prev_total = toatal_len
	toatal_len= toatal_len+r
	if end_value>=clip0.duration:
		end_value=clip0.duration
	start_time =  random.randrange(int(start_value), int(end_value), 1)
	clip1 = clip0.subclip(start_time,start_time+r)
	finalvideo.append(clip1)
	start_value+=void
	end_value+=void

start_time =  random.randrange(1, clip1.duration, 1)
clip1 = clip0.subclip(start_time,start_time+(duration-prev_total))
finalvideo.append(clip1)
random.shuffle(finalvideo)


final_audio = aud0.subclip(int(audio_start), int(audio_start)+int(duration))
final_audio.write_audiofile("c1_amv.mp3", fps=44100)

final_video_clip = concatenate_videoclips(finalvideo)
final_video = final_video_clip.set_audio(final_audio)
final_video.write_videofile(edited_video_name+".mp4", codec='libx264', audio_codec="aac")
