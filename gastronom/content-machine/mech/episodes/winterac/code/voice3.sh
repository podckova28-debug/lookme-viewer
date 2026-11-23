# v3: живой текст + 5 дублей, выбор — годный по QA и самый живой по интонации (voiceclone/expr/prosody.py)
cd /tmp/claude-0/-home-user-lookme-viewer/8420a68c-a72b-5ef9-9faf-653836f3526a/scratchpad
P=video/mech_winterac; L=$P/qa_out/clone3.log; REST="--ids F01 F03 F04 F06 F08 F10"
cbx_env/bin/python voiceclone/clone_tts.py --project $P --ref voiceclone/ref_alexey.wav --take a --seed 0 --exaggeration 0.5 --cfg 0.5 --temperature 0.8 $REST >> $L 2>&1
cbx_env/bin/python voiceclone/clone_tts.py --project $P --ref voiceclone/ref_alexey.wav --take b --seed 0 --exaggeration 0.8 --cfg 0.3 --temperature 0.8 $REST >> $L 2>&1
cbx_env/bin/python voiceclone/clone_tts.py --project $P --ref voiceclone/expr/ref_f1.wav --take e --seed 0 --exaggeration 0.8 --cfg 0.3 --temperature 0.8 $REST >> $L 2>&1
cbx_env/bin/python voiceclone/clone_tts.py --project $P --ref voiceclone/ref_alexey.wav --take f --seed 7 --exaggeration 0.65 --cfg 0.4 --temperature 0.8 >> $L 2>&1
cbx_env/bin/python voiceclone/clone_tts.py --project $P --ref voiceclone/expr/ref_f1.wav --take g --seed 3 --exaggeration 0.65 --cfg 0.4 --temperature 0.8 >> $L 2>&1
echo CLONEDONE >> $L
