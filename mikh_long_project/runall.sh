#!/bin/bash
cd /home/user/mk
J=$(nproc); [ $J -gt 8 ] && J=8
ls spec/ch*.json spec/t00.json spec/e99.json | xargs -P $J -I{} sh -c 'n=$(basename {} .json); [ -s out/$n.mp4 ] || python3 render.py {} out/$n.mp4 > out/$n.log 2>&1'
echo ALL_RENDERED > out/runall.done
