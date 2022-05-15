import subprocess

# command_1 = "ffmpeg -ss 00:00:15 -t 00:00:10 -i haha.mp4 -vcodec copy -an -y output.mp4 "
# subprocess.Popen(command_1, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
command_2 = "ffmpeg -i 'mm.mp4' -vf fps=0.2 -q:v 15 -f image2 pic/pic-%d.jpg"
subprocess.Popen(command_2, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
