"""Таймкоды глав для описания YouTube из раскладки монтажа (начало первой реплики главы, вместе с паузой под заставку)."""
import os, sys; sys.argv = ["cut.py"]
_here = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [_here, os.path.dirname(_here)]  # рядом с cut.py (репозиторий) или в work/ черновика
import cut, timeline as T
shots, total = cut.plan()
LT = cut.LT
names = ['1. Колготки вместо ремня', '2. Сахар в бак', '3. Мыло в бензобак', '4. Яйцо в радиатор', '5. Паяльная лампа под поддоном',
         '6. Аккумулятор домой', '7. Мешки с песком в багажник', '8. Картошка на стекло', '9. Кола от ржавчины', '10. Зубная паста для фар']
f = lambda t: f'{int(t // 60)}:{int(t % 60):02d}'
out = ['0:00 Вступление'] + [f'{f(LT[a][0])} {n}' for (a, b, _), n in zip(T.CHAPTERS, names)] + \
      [f'{f(LT["B1"][0])} Бонус: завести с толкача', f'{f(LT["L52"][0])} Итоги']
print('\n'.join(out)); print('длина', f(total), round(total, 1), file=sys.stderr)
