import os
import datetime
import random
import subprocess

datetime = datetime.datetime.now().strftime('''%d-%m-%Y_%H-%M-%S''')

base_dir = os.path.dirname(__file__)
os_sep = os.sep

input_dir = f'''{base_dir}{os.sep}input{os.sep}'''
output_dir = f'''{base_dir}{os.sep}output{os.sep}'''
bg_dir = f'''{base_dir}{os.sep}static{os.sep}backgrounds{os.sep}'''
logo_dir = f'''{base_dir}{os.sep}static{os.sep}logos{os.sep}'''
font_dir = f'''{base_dir}{os.sep}static{os.sep}fonts{os.sep}'''
music_dir = f'''{base_dir}{os.sep}static{os.sep}musics{os.sep}'''
outro_dir =f'''{base_dir}{os.sep}static{os.sep}outros{os.sep}'''


files = [files for files in os.listdir(input_dir)]
musics = [musics for musics in os.listdir(music_dir)]

def Joinvideo():
    for f in files:
        path = f'''{input_dir}{f}{os.sep}'''

        with open(f'{path}titles.txt', 'r') as _f:
            _titles = _f.readlines()

        n = 0

        for filenames, title in zip(os.listdir(path),_titles):
            n += 1
            if filenames.endswith(".jpg") or filenames.endswith(".png"):
                file_name, file_extension = os.path.splitext(filenames)

                # Resize
                os.system(f'''ffmpeg -i {path}{file_name}{file_extension} -vf scale=-1:1080 {path}resize-{n}.png''')
                # Add background
                os.system(f'''ffmpeg -i {bg_dir}bg.png -i {path}resize-{n}.png -filter_complex "overlay=(W-w)/2:(H-h)/2" {path}bg-{n}.png''')
                # os.remove(f'''{path}resize-{n}.png''')
                # Add logo
                os.system(f'''ffmpeg -i {path}bg-{n}.png -i {logo_dir}logo.png -filter_complex "overlay=0:0" {path}logo-{n}.png''')
                # os.remove(f'''{path}bg-{n}.png''')
                # Covert into video
                os.system(f'''ffmpeg -framerate 1/6 -i {path}logo-{n}.png -c:v libx264 -r 30 -pix_fmt yuv420p \
                            {path}clip-{n}.mp4''')
                # os.remove(f'''{path}logo-{n}.png''')
                # Add subtitles
                if len(title) in range(0,50):
                    length = len(title)-1
                    os.system(f'''ffmpeg -i {path}clip-{n}.mp4 -vf "[in]drawtext=fontfile=impact.ttf:text={title[0:length]}: \
                                fontcolor=white:fontsize=45:box=1:boxcolor=black@0.5:boxborderw=10:x=(w-text_w)/2:y=(h-text_h)-45" \
                                -codec:a copy {path}clip-with-subtitles{n}.mp4''')
                elif len(title) in range(50,100):
                    length = len(title)-1
                    os.system(f'''ffmpeg -i {path}clip-{n}.mp4 -vf "[in]drawtext=fontfile=impact.ttf:text={title[0:length]}: \
                                fontcolor=white:fontsize=40:box=1:boxcolor=black@0.5:boxborderw=10:x=(w-text_w)/2:y=(h-text_h)-45" \
                                -codec:a copy {path}clip-with-subtitles{n}.mp4''')
                elif len(title) > 100:
                    length = len(title)-1
                    length_ = len(title)-99
                    os.system(f'''ffmpeg -i {path}clip-{n}.mp4 -vf "[in]drawtext=fontfile=impact.ttf:text='{title[0:length_]}-': \
                                fontcolor=white:fontsize=35:box=1:boxcolor=black@0.5:boxborderw=10:x=(w-text_w)/2:y=(h-text_h)-70, \
                                drawtext=fontfile=impact.ttf:text='{title[length_:length]}': \
                                fontcolor=white:fontsize=35:box=1:boxcolor=black@0.5:boxborderw=10:x=(w-text_w)/2:y=(h-text_h)-20[out]" \
                                -codec:a copy {path}clip-with-subtitles{n}.mp4''')
                os.remove(f'''{path}clip-{n}.mp4''')

        # Convert into ts videos
        os.system(f'''for %i in ({path}*.mp4) do ffmpeg -i "%i" -c copy -bsf:v h264_mp4toannexb -f mpegts {path}%~ni.ts''') 

        # Join all ts videos and convert into mp4
        path_ts_ = []
        for filenames_ts in os.listdir(path):
            if filenames_ts.endswith(".ts"):
                path_ts = f'''file '{path}{filenames_ts}'\n'''
                path_ts_.append(path_ts)
        path_ts_.sort()

        for p in path_ts_:
            with open(f'{path}videos.txt', 'a') as _f_:
                _f_.write(p)

        os.system(f'''ffmpeg -f concat -safe 0 -i {path}videos.txt \
                    -c copy -bsf:a aac_adtstoasc {path}output.mp4''')

def Joinsong():
    v_ = []
    path_video_ = []
    for f in files:
        path_video = f'''{input_dir}{f}{os.sep}'''

        filename_video = f'''{path_video}output.mp4'''
        result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                    "format=duration", "-of",
                                    "default=noprint_wrappers=1:nokey=1", filename_video],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
        video_length = float(result.stdout)
        v_.append(video_length)
        path_video_.append(path_video)

    music_list = {}
    for music_ in musics:
        path_music = f'''{music_dir}{music_}'''
        # filename_music, _ =  os.path.splitext(path_music)
        result_ = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                    "format=duration", "-of",
                                    "default=noprint_wrappers=1:nokey=1", path_music],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
        music_length = float(result_.stdout)
        music_list[music_] = music_length

    n = 0
    music_names, music_lengths = random.choice(list(music_list.items()))
    print(f'''Time {n}. {music_names}: {music_lengths}''')
    try:
        with open(f'{path_video}songs.txt', 'a') as _f:
            _f.write(f'''file '{music_dir}{music_names}'\n''')
    except Exception as e:
        print(f'''We have an error from step {n}: {e}''')
        pass

    while music_lengths > 0:
        n += 1
        if music_lengths < v_[0]:
            _, music_lengths_ = random.choice(list(music_list.items()))
            music_lengths += music_lengths_
            print(f'''Time {n}. {music_names}: {music_lengths}''')
            try:
                with open(f'{path_video}songs.txt', 'a') as _f:
                    _f.write(f'''file '{music_dir}{music_names}'\n''')
            except Exception as e:
                print(f'''We have an error from step {n}: {e}''')
                pass
            continue
        else:
            break
    os.system(f'''ffmpeg -f concat -safe 0 -i {path_video_[0]}songs.txt -c copy {path_video_[0]}bg.wav''')

def Addsong():
    for f in files:
        path = f'''{input_dir}{f}{os.sep}'''

        #Add song
        os.system(f'''ffmpeg -i {path}output.mp4 -i {path}bg.wav -map 0:v -map 1:a -c:v copy -shortest {path}video.mp4"''')

        #Add outro
        os.system(f'''ffmpeg -i {path}video.mp4 -c copy -bsf:v h264_mp4toannexb -f mpegts {path}video.ts''')
        os.system(f'''ffmpeg -i "concat:{path}video.ts|{outro_dir}outro.ts" -c copy -bsf:a aac_adtstoasc "{output_dir}{f} ({datetime}).mp4"''') 

        _filename_ = [filename for filename in os.listdir(path) if (filename.endswith('.ts') or filename.endswith('.mp4'))]
        for f in _filename_:
            os.remove(f'''{path}{f}''')

if __name__ == "__main__":
    Joinvideo()
    # Joinsong()
    # Addsong()



