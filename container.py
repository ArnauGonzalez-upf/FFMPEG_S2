import os
import wget
import shlex
import subprocess
from utils import contains


class Container:
    # Define class constructor
    def __init__(self):
        self.dvb_audio = ['aac', 'ac3', 'mp3']
        self.isdb_audio = ['aac']
        self.atsc_audio = ['ac3']
        self.dtmb_audio = ['aac', 'ac3', 'mp2', 'mp3']
        self.non_dtmb_video_codecs = ['mpeg2video', 'h264']
        self.dtmb_video_codecs = ['avs', 'avs2', 'avs3', 'mpeg2video', 'h264']

    @staticmethod
    def motion_vectors():
        # Execute command line
        os.system('ffmpeg -flags2 +export_mvs -i BBB_CUT.mp4 -vf codecview=mv=pf+bf+bb BBB_CUT_MV.mp4')

    @staticmethod
    def bbb_container():
        # Execute command lines
        os.system('ffmpeg -ss 00:00:00 -i BBB.mp4 -t 60 -c copy BBB_CUT_2.mp4')
        os.system('ffmpeg -i BBB_CUT_2.mp4 -acodec libmp3lame -ac 2 output-audio.mp3')
        os.system('ffmpeg -i BBB_CUT_2.mp4 -acodec libfdk_aac -b:a 16k output-audio.aac')
        os.system('ffmpeg -i BBB_CUT_2.mp4 -c copy -an BBB_CUT_2_NO_AUDIO.mp4')
        os.system('ffmpeg -i BBB_CUT_2_NO_AUDIO.mp4 -i output-audio.mp3 -i output-audio.aac -map 0 -map 1 -map 2 '
                  '-c copy BBB_MULTI_CHANNEL.mp4 ')

    def broadcast_standards(self):
        # Select video
        print("Write video file name without extension:")
        video_selected = input()

        # Set command line for video
        cmd = 'ffprobe -v error -select_streams v -show_entries stream=codec_name' \
              ' -of default=noprint_wrappers=1:nokey=1 ' + video_selected + '.mp4'
        cmd = shlex.split(cmd)  # Split by spaces
        process_video = subprocess.run(cmd,
                                       stdout=subprocess.PIPE,
                                       universal_newlines=True)  # Execute
        process_video = shlex.split(process_video.stdout)  # Split output by spaces
        if not process_video:  # Check if empty
            print("ERROR: No video track!")
            return
        print("Video codecs:", process_video)

        # Same for audio
        cmd = 'ffprobe -v error -select_streams a -show_entries stream=codec_name' \
              ' -of default=noprint_wrappers=1:nokey=1 ' + video_selected + '.mp4'
        cmd = shlex.split(cmd)
        process_audio = subprocess.run(cmd,
                                       stdout=subprocess.PIPE,
                                       universal_newlines=True)
        process_audio = shlex.split(process_audio.stdout)
        if not process_audio:  # Check if empty
            print("ERROR: No audio track!")
            return
        print("Audio codecs:", process_audio)

        # Check codecs
        codecs = []
        if contains(process_audio, self.dvb_audio) and contains(process_video, self.non_dtmb_video_codecs):
            codecs.append("DVB")
        if contains(process_audio, self.isdb_audio) and contains(process_video, self.non_dtmb_video_codecs):
            codecs.append("ISDB")
        if contains(process_audio, self.atsc_audio) and contains(process_video, self.non_dtmb_video_codecs):
            codecs.append("ATSC")
        if contains(process_audio, self.dtmb_audio) and contains(process_video, self.dtmb_video_codecs):
            codecs.append("DTMB")

        # Show codecs
        if codecs:
            print("Broadcast Standards:", codecs)
        else:  # Select codec to convert
            print("ERROR: NO BROADCAST STANDARD FOUND\nConvert to standard:")
            print("Select:")
            print("1) DVB")
            print("2) ISDB")
            print("3) ATSC")
            print("4) DTMB")
            select = input()

            # Convert video
            if select == "1" or select == "2" or select == "4":
                os.system('ffmpeg -i ' + video_selected + '.mp4 -c:v libx264 -c:a libfdk_aac '
                          + video_selected + '_standarized.mp4')
            elif select == "3":
                os.system('ffmpeg -i ' + video_selected + '.mp4 -c:v libx264 -c:a ac3 '
                          + video_selected + '_standarized.mp4')
            else:
                print("Not an option! Exiting")

    @staticmethod
    def non_standard_video():
        # Select video
        print("Write video file name without extension:")
        video_selected = input()
        # Create non broadcast standard video
        os.system('ffmpeg -i ' + video_selected + '.mp4 -c:v mpeg1video -c:a libvorbis '
                  + video_selected + '_no_standard.mp4')

    @staticmethod
    def insert_subtitles():
        # Download subtitles
        wget.download("https://drive.google.com/uc?export=download&id=1rU_zZfvx4mIgBR-OGGfDa9L8agN0jIzt")
        # Execute command line
        os.system("ffmpeg -i BBB_CUT_2.mp4 -vf subtitles=subs.srt -c:a copy BBB_CUT_2_SUBS.mp4")
