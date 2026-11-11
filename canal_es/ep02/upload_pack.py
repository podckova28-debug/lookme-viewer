"""Writes out/subida_youtube.md: title, short neutral description with chapters (from timing.json), tags, pinned comment, Shorts titles."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); T = json.load(open(os.path.join(HERE, 'timing.json')))
# the short, neutral chapter list used in the description
CH_SHORT = [('s00', 'Inicio'), ('s05', 'Quemados'), ('s10', 'Todo dos veces'), ('s14', 'La pregunta'), ('s16', 'Pepe'), ('s17', '¿Algo de esto es real?')]
def mmss(x): x = int(x); return f'{x // 60}:{x % 60:02d}'
chap = '\n'.join(f"{mmss(T['scenes'][s]['start'])} {n}" for s, n in CH_SHORT)
md = f"""# Subida a YouTube · Episodio 2

## Título
¿Qué pasaría si pudieras ver 5 segundos del futuro?

Alternativa para prueba A/B: ¿Qué pasaría si vieras 5 segundos del futuro… y lo arruinaras todo?

## Miniatura
Mismo estilo que el episodio 1 (ilustración brillante, título de dos líneas blanco + amarillo, un poco inclinado), compuesta con `../../marca/miniatura.py`; el arte sin texto está en `miniaturas_arte/`.
- A (principal): `miniatura_A.jpg`
- B: `miniatura_B.jpg`
- C: `miniatura_C.jpg`

YouTube Studio → Probar y comparar: subir A, B y C juntas.

## Descripción
¿Qué pasaría si pudieras ver cinco segundos del futuro? Una historia animada sobre lo que ganarías y lo que perderías. Al final, la ciencia real detrás de la idea.

{chap}

Animación original.

#quepasariasi #animacion

## Etiquetas
qué pasaría si pudieras ver 5 segundos del futuro, que pasaria si pudieras ver el futuro, ver el futuro, 5 segundos del futuro, y si pudieras ver el futuro, qué pasaría si, que pasaria si, historias animadas, animación en español, qué harías si, superpoderes en la vida real, ponle que, pepe la paloma, alerta sísmica

## Comentario fijado
Pepe nunca tuvo fantasma… hasta el final. ¿Qué crees que dijo Pepe? Las mejores respuestas salen en el próximo episodio. 🐦

## Subtítulos
`subtitulos_es.srt`: subir en YouTube Studio → Subtítulos → Español.

## Pantalla final y tarjetas
- Pantalla final (últimos 10 s): «Suscribirse» + «Video: episodio 1».
- Tarjeta en 0:15: episodio 1 («¿Qué pasaría si pudieras detener el tiempo?»).

## Shorts
1. `short1_taza.mp4`: Ves el futuro… y atrapas la taza ☕ #shorts #quepasariasi
2. `short2_quemados.mp4`: ¿Y si vieras cada balón antes de que lo lancen? #shorts #quepasariasi
3. `short3_cumple.mp4`: Tu fiesta sorpresa… cinco segundos antes 🎉 #shorts #quepasariasi
4. `short4_pizza.mp4`: Respondes antes de que te pregunten 🍕 #shorts #quepasariasi
5. `short5_pregunta.mp4`: Ya sabes lo que te va a preguntar #shorts #quepasariasi
6. `short6_pepe.mp4`: En 5 segundos, Pepe va a hablar 🐦 #shorts #quepasariasi
7. `short7_ciencia.mp4`: 3 cosas reales sobre ver el futuro 🧠 #shorts #ciencia

Duración total: {mmss(T['total'])} · voz: {T['vo']}
"""
os.makedirs(os.path.join(HERE, 'out'), exist_ok=True); open(os.path.join(HERE, 'out', 'subida_youtube.md'), 'w', encoding='utf-8').write(md); print(chap)
