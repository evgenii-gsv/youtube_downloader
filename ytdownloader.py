from pytube import YouTube
import ffmpeg
import os
import sys
import requests
from pydub import AudioSegment


def video_url_validating():
    while True:
        url = input('Paste video URL here: ')
        if url.lower().strip() == 'exit' or url.lower().strip() == 'quit' or url.lower().strip() == 'stop':
            sys.exit()
        try:
            YouTube(url).check_availability()
            break
        except:
            print('Error in URL or the video is unavailable')
    return url


def get_output_folder():
    with open('output_dir.txt', 'r') as open_file:
        output_dir = open_file.read()
    return output_dir


def get_best_audio_and_video(video):
    streams = [video.streams.filter(adaptive=True)[0], video.streams.filter(
        adaptive=True)[-1]]
    return streams


def set_new_output_folder(dir):
    with open('output_dir.txt', 'w') as open_file:
        if dir == '':
            open_file.write(os.getcwd() + '\\')
        elif not dir.endswith('\\'):
            open_file.write(dir + '\\')
        else:
            open_file.write(dir)


def download_yt_video(video):
    yt_streams = get_best_audio_and_video(video)
    yt_streams[0].download(output_path=output_dir, filename='temp_video')
    yt_streams[1].download(output_path=output_dir, filename='temp_audio')
    ffmpeg.concat(ffmpeg.input(f'{output_dir}temp_video'), ffmpeg.input(f'{output_dir}temp_audio'), v=1, a=1).output(
        f'{output_dir}{yt.title}.mp4').run()
    os.remove(f'{output_dir}temp_video')
    os.remove(f'{output_dir}temp_audio')
    print('Video downloaded')


def download_separately(video):
    yt_streams = get_best_audio_and_video(video)
    yt_streams[0].download(output_path=output_dir, filename_prefix='video - ')
    yt_streams[1].download(output_path=output_dir, filename_prefix='audio - ')


def download_video_only(video):
    yt_streams = get_best_audio_and_video(video)
    yt_streams[0].download(output_path=output_dir, filename_prefix='video - ')


def download_audio_only(video):
    yt_streams = get_best_audio_and_video(video)
    yt_streams[1].download(output_path=output_dir, filename='temp_audio.webm')
    AudioSegment.from_file(f'{output_dir}temp_audio.webm').export(f'{output_dir}{yt.title}.mp3', format='mp3')
    os.remove(f'{output_dir}temp_audio.webm')
    print(f'{yt.title}.mp3 is downloaded')


def download_thumbnail(video):
    high_res_url = video.thumbnail_url.replace('sddefault.jpg', 'maxresdefault.jpg')
    high_res_url = high_res_url.replace('hqdefault.jpg', 'maxresdefault.jpg')
    r = requests.get(high_res_url, allow_redirects=True)
    with open(f'{output_dir}thumbnail.jpg', 'wb') as handle:
        handle.write(r.content)
    print('Thumbnail downloaded')


def download_complete(stream, file_path):
    print(f'{stream} is downloaded')


commands = '''"download" - downloads the youtube video and audio combining them together
"download separately" - downloads the youtube video and audio separately
"download video" - downloads video without audio
"download audio" - downloads audio without video
"thumbnail" - downloads the thumbnail of the video
"output" - shows your current output folder
"change output" - changes your current output folder
"url" - lets you switch to another YouTube video
"exit" - exits the program
'''

if __name__ == '__main__':
    print('Welcome to Eugene\'s YouTube Downloader. Type \'exit\' to close the program.\n')
    if not os.path.isfile('output_dir.txt'):
        print('Let\'s set up your download\'s folder. Paste the path of your choice.')
        print('Paste nothing, if you wish to use the folder that the program is running from.')
        print('You can change it later.')
        set_new_output_folder(input('New directory: '))

    output_dir = get_output_folder()
    url = video_url_validating()
    yt = YouTube(url, on_complete_callback=download_complete)
    print(f'Video title is: {yt.title}')
    print('What do you want to do? Type \'help\' for the list of commands')

    while True:
        action = input('>>>> ').lower().strip()
        if action == 'download':
            download_yt_video(yt)
        elif action == 'download separately':
            download_separately(yt)
        elif action == 'download video':
            download_video_only(yt)
        elif action == 'download audio':
            download_audio_only(yt)
        elif action == 'thumbnail':
            download_thumbnail(yt)
        elif action == 'output':
            print(f'Your output directory is: {output_dir}')
        elif action == 'change output':
            set_new_output_folder(input('New directory:'))
            output_dir = get_output_folder()
        elif action == 'url':
            url = video_url_validating()
            yt = YouTube(url, on_complete_callback=download_complete)
            print(f'Video title is: {yt.title}')
            print('What do you want to do? Type \'help\' for the list of commands')
        elif action == 'exit' or action == 'quit' or action == 'stop':
            sys.exit()
        elif action == 'help' or action == '?':
            print(commands)
        else:
            print('Command not clear. See the list of commands typing \'help\'')
