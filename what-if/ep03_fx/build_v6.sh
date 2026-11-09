set -e
G=/tmp/claude-0/-home-user-lookme-viewer/15230ea4-cf3a-58b7-8157-8e72db0a2b22/scratchpad/ep03
cd $G
SR=48000
# 1) picture + scene audio: head, new act, tail
ffmpeg -v error -y -i e3_recut_a.mp4 -vf "select='lte(n\,3107)',setpts=N/24/TB" -af "atrim=end=129.5,asetpts=N/SR/TB" -c:v libx264 -crf 14 -pix_fmt yuv420p -c:a aac -ar 48000 -ac 2 p_head.mp4
ffmpeg -v error -y -i e3_recut_a.mp4 -vf "select='gte(n\,3374)',setpts=N/24/TB" -af "atrim=start=140.5833,asetpts=N/SR/TB" -c:v libx264 -crf 14 -pix_fmt yuv420p -c:a aac -ar 48000 -ac 2 p_tail.mp4
for k in n1f_fx n2f_fx n4f_fx n3f_fx shoes_red_fx n5f_fx; do
  ffmpeg -v error -y -i $k.mp4 -f lavfi -i anullsrc=r=48000:cl=stereo -filter_complex "[0:a]aresample=48000,aformat=channel_layouts=stereo,volume=0.8[a0];[1:a][a0]amix=inputs=2:duration=shortest:normalize=0[a]" -map 0:v -map "[a]" -c:v copy -c:a aac -ar 48000 -ac 2 -shortest p_$k.mp4 2>/dev/null || ffmpeg -v error -y -i $k.mp4 -f lavfi -i anullsrc=r=48000:cl=stereo -map 0:v -map 1:a -c:v copy -c:a aac -shortest p_$k.mp4
done
printf "file '%s'\n" p_head.mp4 p_n1f_fx.mp4 p_n2f_fx.mp4 p_n4f_fx.mp4 p_n3f_fx.mp4 p_shoes_red_fx.mp4 p_n5f_fx.mp4 p_tail.mp4 > v6_list.txt
ffmpeg -v error -y -f concat -safe 0 -i v6_list.txt -vf "settb=1/24,fps=24" -c:v libx264 -crf 14 -pix_fmt yuv420p -c:a aac -ar 48000 -ac 2 e3_v6_pic.mp4
N=$(ffprobe -v error -count_frames -select_streams v -show_entries stream=nb_read_frames -of csv=p=0 e3_v6_pic.mp4)
python3 -c "import json;json.dump([{'id':'all','start':0,'dur':$N/24}],open('e3_v6_pic.timeline.json','w'))"
echo frames $N
# 2) narration
python3 - <<EOF
import glob,os,shutil
G="$G"; out=G+'/vo/mix4'; shutil.rmtree(out,ignore_errors=True); os.makedirs(out)
SH=230/24
for f in glob.glob(G+'/vo/mix3/vo_all@*.wav'):
    t=float(f.rsplit('@',1)[1][:-4])
    if 129.5<=t<140.58:
        if abs(t-133.50)<0.05: t=142.6     # Nobody will ever know -> old lady
        elif abs(t-135.33)<0.05: t=145.0   # Uh-oh -> burning sneakers
        else: print('drop',t); continue
    elif t>=140.58: t+=SH
    shutil.copy(f,f'{out}/vo_all@{t:.2f}.wav')
shutil.copy(G+'/vo/new2/vo_costume.wav',out+'/vo_all@129.70.wav')
shutil.copy(G+'/vo/new2/vo_hide.wav',out+'/vo_all@147.35.wav')
print(sorted(os.listdir(out)))
EOF
cd "$(dirname "$0")/.."
python3 tools/mix_vo.py $G/e3_v6_pic.mp4 $G/e3_v6_vo.mp4 $G/vo/mix4 --lead 0
python3 tools/push_holds.py $G/e3_v6_vo.mp4 $G/e3_v6_push.mp4
ffmpeg -v error -y -i $G/e3_v6_push.mp4 -vf "scale=960:540:flags=area,scale=1920:1080:flags=lanczos,cas=0.9,unsharp=5:5:0.8:5:5:0" -c:v libx264 -preset medium -crf 15 -pix_fmt yuv420p -c:a copy $G/e3_v6_sharp.mp4
python3 - <<EOF
import json; fx=json.load(open('$G/fx_v3.json')); fx[3]['f0']+=230; fx[3]['f1']+=230; json.dump(fx,open('$G/fx_v6.json','w')); print(fx[3])
EOF
python3 tools/fx_overlay.py $G/e3_v6_sharp.mp4 $G/e3_v6_fx.mp4 $G/fx_v6.json
echo DONE
