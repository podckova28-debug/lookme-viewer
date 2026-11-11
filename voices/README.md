# Голоса для озвучки (коммерческая лицензия)

Синтез: **Chatterbox** (Resemble AI, MIT), клонирование голоса только из синтетических опорных
голосов **Kokoro-82M** (hexgrad, Apache-2.0). Чужие записи и голоса реальных людей не используются.
OmniVoice (веса CC-BY-NC) не используется.

## Установка (CPU, Python 3.11)
```
uv venv -p 3.11 venv && . venv/bin/activate
uv pip install torch==2.6.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cpu
uv pip install "chatterbox-tts @ git+https://github.com/resemble-ai/chatterbox" "setuptools<81"
uv pip install --no-deps chatterbox-tts   # если зависимости конфликтуют, ставить по ошибкам
python tts_en.py lines.txt out refs/kokoro_bm_george.wav 0.45 0.5
```
Скорость: примерно 5 с CPU на 1 с звука (4 ядра). Проверка: faster-whisper small, звук ресемплировать ffmpeg в 16 кГц.

## Опорные голоса (`refs/`)
| Файл | Kokoro voice | Тембр | Где используется |
|---|---|---|---|
| kokoro_am_michael.wav | am_michael | американский мужской, спокойный | «Здоровье» (голос H1) |
| kokoro_bm_george.wav | bm_george | британский мужской, ~133 Гц | рассказчик, кандидат N1 |
| kokoro_bm_fable.wav | bm_fable | британский мужской, ниже ~118 Гц | рассказчик, кандидат N2 |
| kokoro_bf_emma.wav | bf_emma | британский женский, ~179 Гц | Чума, кандидат P1 |
| role_plague_low.wav | bf_isabella, −1,5 полутона (asetrate 0.92) | британский женский, холоднее | Чума, кандидат P2 |

## Пробы «The ENTIRE History of the Plague» (`plague_trial/`)
- Рассказчик (exaggeration 0.45, cfg 0.5): N1_george, N2_fable.
- Чума (exaggeration 0.6, cfg 0.4 — медленнее, с нажимом): P1_emma, P2_isabella_low.
Whisper en: все четыре дословно.
