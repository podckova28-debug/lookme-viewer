cd /tmp/claude-0/-home-user-lookme-viewer/8420a68c-a72b-5ef9-9faf-653836f3526a/scratchpad
R="--project taxi90 --ref voiceclone/ref_alexey.wav --ids Z7 --exaggeration 0.5 --cfg 0.5 --temperature 0.8"
for s in 21 22 23 24; do t=s$s; cbx_env/bin/python voiceclone/clone_tts.py $R --take $t --seed $s > taxi90/work/clone_z7_$t.log 2>&1; done
for s in 21 22 23 24; do python3.13 qa/stress_audit.py --project taxi90 --take s$s --picks qa_out/textgate.json --ids Z7 --out qa_out/aud_z7s$s.json > taxi90/work/aud_z7s$s.log 2>&1; done
echo ALLDONE5
