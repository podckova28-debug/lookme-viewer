"""Writes out/subida_youtube.md: title, description with chapters (from timing.json), tags, pinned comment, Shorts titles."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); T = json.load(open(os.path.join(HERE, 'timing.json')))
CH = [('s00', 'La maceta'), ('s01', '¿Qué pasaría si…?'), ('s03', 'El primer aplauso'), ('s04', 'Regla #1'), ('s05', 'Ocho horas más de sueño'), ('s06', 'El examen de matemáticas'),
      ('s07', 'El bigote de Nacho'), ('s08', 'La lluvia congelada'), ('s09', 'Los libros de Valeria'), ('s10', 'El penal imposible'), ('s11', 'El precio: una cana'),
      ('s12', 'Nada funciona'), ('s13', 'El cumpleaños de Nacho'), ('s14', 'Pepe'), ('s15', 'La maceta'), ('s16', 'No eres el único'), ('s17', 'Final')]
def mmss(x): x = int(x); return f'{x // 60}:{x % 60:02d}'
chap = '\n'.join(f"{mmss(T['scenes'][s]['start'])} {n}" for s, n in CH)
md = f"""# Subida a YouTube · Episodio 1

## Título
¿Qué pasaría si pudieras detener el tiempo… y no fueras el único?

Alternativa para prueba A/B: ¿Qué pasaría si pudieras detener el tiempo con un aplauso?

(vidIQ: 84 y 83 puntos; el título simple «¿Qué pasaría si pudieras detener el tiempo?» saca 81. Los tres empiezan con la búsqueda exacta, 29,7 mil al mes.)

## Miniatura
- A (principal): `miniatura_A.png`: «1 APLAUSO»
- B: `miniatura_B.png`: «¿TÚ TAMBIÉN?»

## Descripción
¿Qué pasaría si pudieras detener el tiempo con un aplauso? Al principio es increíble: duermes ocho horas más, sacas diez en matemáticas y metes el gol imposible. Pero el tiempo detenido tiene un precio… y no eres el único que lo sabe.

¿Qué harías tú con el tiempo detenido? Déjalo en los comentarios.
¿En qué escenas encontraste a Pepe? 🐦

{chap}

Historia de ficción animada. Personajes, guion y animación originales.

#quepasariasi #detenereltiempo #animacion

## Etiquetas
qué pasaría si, que pasaria si pudieras detener el tiempo, detener el tiempo, pudieras detener el tiempo, qué pasaría si animación, historias animadas, superpoderes en la vida real, qué harías si, animación en español, pepe la paloma

## Comentario fijado
¿En cuántas escenas aparece Pepe? 🐦 Pista: más de cinco. El primero en encontrarlas todas elige el próximo «¿qué pasaría si…?»

## Subtítulos
`subtitulos_es.srt`: subir en YouTube Studio → Subtítulos → Español.

## Shorts
1. `short1_penal.mp4`: ¿Y si detienes el tiempo en un penal? #shorts #quepasariasi
2. `short2_cumple.mp4`: Detienes el tiempo… y todos aplauden 😅 #shorts #quepasariasi
3. `short3_giro.mp4`: ¿Y si no eres el único que detiene el tiempo? #shorts #quepasariasi

Duración total: {mmss(T['total'])} · voz: {T['vo']}
"""
os.makedirs(os.path.join(HERE, 'out'), exist_ok=True); open(os.path.join(HERE, 'out', 'subida_youtube.md'), 'w', encoding='utf-8').write(md); print(chap)
