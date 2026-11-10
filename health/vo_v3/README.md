# Здоровье: проба голоса на коммерческих моделях (v3)

Замена дорожек OmniVoice (веса CC-BY-NC, для монетизированного канала нельзя).
Только модели с коммерческой лицензией, клонирование только из синтезированных голосов Kokoro.

## Модели
| Модель | Версия | Лицензия |
|---|---|---|
| Chatterbox (английская), ResembleAI/chatterbox | chatterbox-tts 0.1.7, git | MIT |
| Kokoro-82M, hexgrad/Kokoro-82M | kokoro 0.9.4 | Apache-2.0 |

## Варианты
| Файл | Как сделан | Опорный голос | Высота | Whisper en |
|---|---|---|---|---|
| H1_michael_fingers.wav | Chatterbox, клон | refs/kokoro_am_michael.wav (Kokoro am_michael) | 113 Hz | дословно |
| H2_fenrir_fingers.wav | Chatterbox, клон | refs/kokoro_am_fenrir.wav (Kokoro am_fenrir) | 124 Hz | дословно |
| H3_builtin_fingers.wav | Chatterbox, встроенный голос | нет | 120 Hz | дословно |
| H4_kokoro_michael_fingers.wav | Kokoro напрямую, am_michael, speed 1.0 | нет | 113 Hz | дословно |

Фраза: «Your fingers don't wrinkle because they soak up water. They wrinkle on purpose.»
Файлы H1_michael.wav, H2_fenrir.wav, H3_builtin.wav: первые четыре строки «пальцев» с паузой 0,35 с.
Настройки Chatterbox: exaggeration 0.5, cfg_weight 0.5, temperature 0.7. WAV mono 24 kHz, тишина обрезана.
