import sys; sys.argv = ['cut.py']; sys.path.insert(0, '.')
import cut
from timeline import CHAPTERS
shots, total = cut.plan()
names = {'A1': 'Ошибка 1. Ручник на ночь', 'B1': 'Ошибка 2. Кипяток на стекло', 'C1': 'Ошибка 3. Примерзшие дворники и двери',
         'D1': 'Ошибка 4. Запуск в мороз как летом', 'E1': 'Ошибка 5. Прогрев 15 минут', 'F1': 'Ошибка 6. Газ на холодный мотор',
         'G1': 'Ошибка 7. Снег на крыше', 'H1': 'Бонус: печка и давление в шинах', 'Z1': 'Итоги'}
fmt = lambda t: f'{int(t // 60)}:{int(t % 60):02d}'
out = ['0:00 Вступление'] + [f"{fmt(cut.LT[k][0] + (1.4 if k != 'Z1' else 0))} {v}" for k, v in names.items()]
print('\n'.join(out)); print('итого', fmt(total))
open('work/chapters.txt', 'w').write('\n'.join(out) + '\n')
