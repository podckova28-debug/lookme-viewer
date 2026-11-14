cd /tmp/claude-0/-home-user-lookme-viewer/8420a68c-a72b-5ef9-9faf-653836f3526a/scratchpad
until grep -q ALLDONE3 taxi90/work/extra3.log; do sleep 10; done
R="--project taxi90 --ref voiceclone/ref_alexey.wav --ids D3"
cbx_env/bin/python voiceclone/clone_tts.py $R --take c --seed 0 --exaggeration 0.5 --cfg 0.5 --temperature 0.8 > taxi90/work/clone_d_c.log 2>&1
cbx_env/bin/python voiceclone/clone_tts.py $R --take v --seed 6 --exaggeration 0.5 --cfg 0.5 --temperature 0.8 > taxi90/work/clone_d_v.log 2>&1
cbx_env/bin/python voiceclone/clone_tts.py $R --take q --seed 5 --exaggeration 0.45 --cfg 0.5 --temperature 0.8 > taxi90/work/clone_d_q.log 2>&1
cbx_env/bin/python voiceclone/clone_tts.py $R --take x --seed 3 --exaggeration 0.5 --cfg 0.7 --temperature 0.6 > taxi90/work/clone_d_x.log 2>&1
cbx_env/bin/python voiceclone/clone_tts.py $R --take y --seed 11 --exaggeration 0.5 --cfg 0.5 --temperature 0.8 > taxi90/work/clone_d_y.log 2>&1
for t in c v q x y; do python3.13 qa/stress_audit.py --project taxi90 --take $t --picks qa_out/textgate.json --ids D3 --out qa_out/aud_d$t.json > taxi90/work/aud_d$t.log 2>&1; done
echo ALLDONE4
