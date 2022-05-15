import subprocess

# command_1 = "ffmpeg -ss 00:00:15 -t 00:00:10 -i haha.mp4 -vcodec copy -an -y output.mp4 "
# subprocess.Popen(command_1, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
command_2 = "ffmpeg -i ../test_video.mp4 -vf 'fps=1/10:round=zero:start_time=-9,scale=160x90,tile=5x5' M%d.jpg"
subprocess.Popen(command_2, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
