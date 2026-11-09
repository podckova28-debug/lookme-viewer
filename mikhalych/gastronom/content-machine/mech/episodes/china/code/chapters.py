import sys; sys.argv = ['cut.py']; sys.path.insert(0, '.')
import cut
from timeline import CHAPTERS
shots, total = cut.plan()
names = {'A1': 'Кто продает', 'B1': 'Куда пропадают китайские марки', 'C1': 'Почему продают', 'D1': 'Что ломается',
         'E1': 'Запчасти', 'F1': 'Честно о плюсах', 'G1': 'Брать ли с пробегом', 'Z1': 'Итоги'}
fmt = lambda t: f'{int(t // 60)}:{int(t % 60):02d}'
out = ['0:00 Вступление'] + [f"{fmt(cut.LT[k][0] + (1.4 if k != 'Z1' else 0))} {v}" for k, v in names.items()]
print('\n'.join(out)); print('итого', fmt(total))
open('work/chapters.txt', 'w').write('\n'.join(out) + '\n')
