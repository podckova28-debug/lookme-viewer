import sys, json, subprocess, os
# usage: dl.py <dest_dir> <json: {"name": "url", ...}>
dest, mapping = sys.argv[1], json.loads(sys.argv[2]); os.makedirs(dest, exist_ok=True)
procs=[subprocess.Popen(["curl","-s","-o",os.path.join(dest,name),url]) for name,url in mapping.items()]
for p in procs: p.wait()
print("downloaded", len(procs))
