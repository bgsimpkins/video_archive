# -crf- value between 0-51 for quantizer. 0 is lossless. Details here: https://trac.ffmpeg.org/wiki/Encode/H.264#a1.ChooseaCRFvalue
# -preset- time spent processing. Can improve quality. Values here: https://trac.ffmpeg.org/wiki/Encode/H.264#a2.Chooseapresetandtune

ffmpeg -i $1 -c:v libx264 -c:a aac -crf 10 -preset:v medium $2

# For .MOD files (actually just mpeg2) loop in shell script and convert to mp4
for i in ./*MOD; do ffmpeg -i "$i" -c:v libx264 -c:a aac -crf 10 -preset:v medium "converted/$i".mp4; done