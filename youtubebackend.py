from pytubefix import YouTube
from moviepy.video.io.ffmpeg_tools import ffmpeg_merge_video_audio
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_audio
import os


def on_progress(chunk, file_handler, progress):
    output = abs(round((progress / stream_filesize) * 100) - 100)
    print(str(output) + "% done...")
    
def video_download(input_link, resolution="1080p"):
    yt = YouTube(
        input_link,
        use_oauth=True,
        allow_oauth_cache=True,
        on_progress_callback=on_progress
        )


    video_stream = yt.streams.filter(type='video', file_extension='mp4', resolution=resolution).first()
    video_stream_filesize = video_stream.filesize
    video_uh_title = video_stream.title

    global video_title
    video_title = video_uh_title
    

    audio_stream = yt.streams.filter(type='audio').first()
    audio_stream_filesize = audio_stream.filesize

    print("Downloading video file...")
    print("0% done...")
    global stream_filesize 
    stream_filesize = video_stream_filesize
    video_stream.download(output_path=path + "\\tmp", filename="tempvideo.mp4")

    stream_filesize = audio_stream_filesize
    print("Downloading audio file...")
    audio_stream.download(output_path=path + "\\tmp", filename="tempaudio.mp4")

    print("Download complete!!!")
    
def audio_download(input_link):
    yt = YouTube(
        input_link,
        use_oauth=True,
        allow_oauth_cache=True,
        on_progress_callback=on_progress
        )

    audio_stream = yt.streams.filter(type='audio').first()
    audio_stream_filesize = audio_stream.filesize
    video_uh_title = audio_stream.title
    
    global video_title
    video_title = video_uh_title

    print("Downloading video file...")
    print("0% done...")
    
    global stream_filesize 
    stream_filesize = audio_stream_filesize
    print("Downloading audio file...")
    audio_stream.download(output_path=path + "\\tmp", filename="tempaudio.mp4")

    print("Download complete!!!")
    
def merge_av():
    print("Merging audio and video...")
    ffmpeg_merge_video_audio(path + "\\tmp\\" + "tempvideo.mp4",
                            path + "\\tmp\\" + "tempaudio.mp4",
                            path + "\\output\\" + video_title + ".mp4",
                            vcodec='copy',
                            acodec='copy',
                            ffmpeg_output=False,
                            logger=None)
    print("Merging complete!")
    
def convert_mp4_mp3():
    print("Converting MP4 to MP3...")
    
    ffmpeg_extract_audio(path + "\\tmp\\" + "tempaudio.mp4",
                         path + "\\output\\" + video_title + ".mp3")
    
    print("Converting complete!")
    

def cleanup(tempvideo="tempvideo.mp4", tempaudio="tempaudio.mp4"):
    print("Cleaning up...")
    
    if os.path.exists(path + "\\tmp\\" + tempvideo):
        os.remove(path + "\\tmp\\" + tempvideo)
    
    if os.path.exists(path + "\\tmp\\" + tempaudio):
        os.remove(path + "\\tmp\\" + tempaudio)
        
    print("Clean up complete!")
    
def checkdir():
    if not os.path.exists(path + "\\tmp"):
        os.mkdir(path + "\\tmp")
        
    if not os.path.exists(path + "\\output"):
        os.mkdir(path + "\\output")
    
    
path = os.getcwd()
flag = True

checkdir()

while flag:
    
    input_link = input("Paste the URL of the video you want: ")
    input_file_type = input("Would you like video (MP4) or just audio (MP3)?: (a/v)")
    
    if input_file_type.lower() == 'a':
        audio_download(input_link)
        convert_mp4_mp3()
        cleanup()
        print("Done! :D")
  
    elif input_file_type.lower() == 'v':
        resolution = input("Enter desired resolution:")
        video_download(input_link, resolution)
        merge_av()
        cleanup()
        print("Done! :D")
        
    else:
        print("Invalid choice, try again.")
    
    choice = 'u'
    
    while choice not in "yn":    
        choice = input("Would you like to continue?: (y/n)")
    
        if choice.lower() == 'y':
            break
        
        elif choice.lower() == 'n':
            flag = False

os.startfile("C:\\Users\\ethan\\Desktop\\YoutubeDownloadTool")