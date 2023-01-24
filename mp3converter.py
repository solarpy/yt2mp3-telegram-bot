from pytube import YouTube
import os
yt = YouTube("https://youtu.be/LLaa5-uSSGY")
video = yt.streams.filter(only_audio=True).first()
destination = '.'
out_file = video.download(output_path=destination)
base, ext = os.path.splitext(out_file)
new_file = base + '.mp3'
os.rename(out_file, new_file)
print(out_file, new_file)
yttitle = new_file[75 : len(new_file)]
print(yttitle + " has been successfully downloaded.")
os.remove(new_file)
print(yttitle + " has been successfully deleted")
