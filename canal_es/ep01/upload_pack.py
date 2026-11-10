"""Writes out/subida_youtube.md: title, description with chapters (from timing.json), tags, pinned comment, Shorts titles."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); T = json.load(open(os.path.join(HERE, 'timing.json')))
CH = [('s00', 'La maceta'), ('s01', '¿Qué pasaría si…?'), ('s03', 'El primer aplauso'), ('s04', 'Regla #1'), ('s05', 'Ocho horas más de sueño'), ('s06', 'El examen de matemáticas'),
      ('s07', 'El bigote (y el monóculo)'), ('s08', 'La lluvia congelada'), ('s09', 'Los libros de Renata'), ('s10', 'El penal imposible'), ('s11', 'El precio: una cana'),
      ('s11b', 'La cena'), ('s12', 'Nada funciona'), ('s13', 'El cumpleaños de Nacho'), ('s14', 'Pepe'), ('s15', 'La maceta'), ('s16', 'No eres el único'), ('s17', 'Pepe nunca se puso gris'),
      ('s18', '¿Algo de esto es real?'), ('s19', 'Final')]
def mmss(x): x = int(x); return f'{x // 60}:{x % 60:02d}'
chap = '\n'.join(f"{mmss(T['scenes'][s]['start'])} {n}" for s, n in CH)
md = f"""# Subida a YouTube · Episodio 1

## Título
¿Qué pasaría si pudieras detener el tiempo… y no fueras el único?

Alternativa para prueba A/B: ¿Qué pasaría si pudieras detener el tiempo con un aplauso?

(vidIQ: 84 y 83 puntos; el título simple «¿Qué pasaría si pudieras detener el tiempo?» saca 81. Los tres empiezan con la búsqueda exacta, 29,7 mil al mes.)

## Miniatura
- A (principal): `miniatura_A.jpg`: «¿ELLA TAMBIÉN?» (los dos en color en el mundo congelado)
- B: `miniatura_B.jpg`: «1 APLAUSO»
- C: `miniatura_C.jpg`: «¿ÉL TAMBIÉN?» (Pepe; para probar después del primer día)

## Descripción
¿Qué pasaría si pudieras detener el tiempo con un aplauso? Al principio es increíble: duermes ocho horas más, sacas diez en matemáticas y metes el gol imposible. Pero cada segundo detenido lo vives tú solo… y alguien más está dejando pistas en el mundo congelado.

Al final: ¿algo de esto es real? Cronostasis, tu corazón que no se pausa y los relojes atómicos que demostraron que tu cabeza envejece más rápido que tus pies.

¿Qué harías tú con el tiempo detenido? Déjalo en los comentarios.
¿Viste a Renata parpadear al principio? ¿Y en cuántas escenas Pepe sigue en color? 🐦

{chap}

Historia de ficción animada. Personajes, guion y animación originales.

#quepasariasi #detenereltiempo #animacion

## Etiquetas
qué pasaría si, que pasaria si pudieras detener el tiempo, detener el tiempo, pudieras detener el tiempo, qué pasaría si animación, historias animadas, superpoderes en la vida real, qué harías si, animación en español, pepe la paloma, cronostasis, dilatación del tiempo, relojes atómicos

## Comentario fijado
Pepe nunca se pone gris. ¿En cuántas escenas del mundo congelado lo encontraste? 🐦 Y la pregunta de verdad: ¿quién es Pepe? Las mejores teorías salen en el próximo episodio.

## Subtítulos
`subtitulos_es.srt`: subir en YouTube Studio → Subtítulos → Español.

## Shorts
1. `short1_penal.mp4`: ¿Y si detienes el tiempo en un penal? #shorts #quepasariasi
2. `short2_cumple.mp4`: Detienes el tiempo… y todos aplauden 😅 #shorts #quepasariasi
3. `short3_giro.mp4`: ¿Y si no eres el único que detiene el tiempo? #shorts #quepasariasi
4. `short4_maceta.mp4`: Todo se congeló… menos tú. #shorts #quepasariasi
5. `short5_ciencia.mp4`: Tu cabeza es más vieja que tus pies (es real) #shorts #ciencia
6. `short6_pepe.mp4`: Nadie se mueve… excepto la paloma 🐦 #shorts #quepasariasi

Duración total: {mmss(T['total'])} · voz: {T['vo']}
"""
os.makedirs(os.path.join(HERE, 'out'), exist_ok=True); open(os.path.join(HERE, 'out', 'subida_youtube.md'), 'w', encoding='utf-8').write(md); print(chap)
