import sys, schlib, scenes
from plan import plan
shots, used, marks, total = plan()
nm = sys.argv[1]; T = used[nm] + 0.4
schlib.render(scenes.SCENES[nm], T, f'sch/{nm}.mp4', m=marks[nm])
print(nm, round(T, 2))
