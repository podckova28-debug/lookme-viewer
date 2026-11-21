cd /tmp/claude-0/-home-user-lookme-viewer/8420a68c-a72b-5ef9-9faf-653836f3526a/scratchpad
P=video/mech_winterac; R="--project $P --ref voiceclone/ref_alexey.wav"
cbx_env/bin/python voiceclone/clone_tts.py $R --take c --seed 0 --exaggeration 0.5 --cfg 0.5 --temperature 0.8 > $P/qa_out/clone_c.log 2>&1
cbx_env/bin/python voiceclone/clone_tts.py $R --take v --seed 6 --exaggeration 0.5 --cfg 0.5 --temperature 0.8 > $P/qa_out/clone_v.log 2>&1
cbx_env/bin/python voiceclone/clone_tts.py $R --take q --seed 5 --exaggeration 0.45 --cfg 0.5 --temperature 0.8 > $P/qa_out/clone_q.log 2>&1
cbx_env/bin/python voiceclone/clone_tts.py $R --take x --seed 3 --exaggeration 0.5 --cfg 0.7 --temperature 0.6 > $P/qa_out/clone_x.log 2>&1
cbx_env/bin/python voiceclone/clone_tts.py $R --take y --seed 11 --exaggeration 0.5 --cfg 0.5 --temperature 0.8 > $P/qa_out/clone_y.log 2>&1
for t in c v q x y; do python3.13 qa/stress_audit.py --project $P --take $t --picks qa_out/textgate.json --out qa_out/aud_$t.json > $P/qa_out/aud_$t.log 2>&1; done
echo VOICEDONE
