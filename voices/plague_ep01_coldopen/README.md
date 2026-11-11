# Plague ep01 cold open — озвучка

Рассказчик: N1_george (Chatterbox MIT + Kokoro bm_george, Apache-2.0), exaggeration 0.45, cfg 0.5.
Чума: P2_isabella_low (Kokoro bf_isabella −1,5 полутона), exaggeration 0.6, cfg 0.4.
WAV 24 кГц моно, тишина обрезана. Основной дубль — `<id>.wav`, запасной — `<id>_alt.wav`.

| id | роль | сек | whisper en | 
|---|---|---|---|
| n1 | NARRATOR | 6.2 | дословно («1347», «12» цифрами) |
| n2 | NARRATOR | 6.8 | дословно |
| p1 | PLAGUE | 3.2 | дословно |
| n3 | NARRATOR | 6.5 | дословно |
| n4 | NARRATOR | 11.8 | дословно («thirteen minutes» → «13 minutes») |

Запасной n4 отброшен: whisper услышал «30 minutes» вместо «thirteen».
Сумма основных дублей 34,5 с чистой речи; до 54 с добирается паузами и музыкой.

## Мужская Чума (версия _m)
Опорный голос: `voices/refs/role_plague_m_lewis.wav` = Kokoro bm_lewis (speed 0.9), опущен на 2 полутона (asetrate 0.89). exaggeration 0.6, cfg 0.4.
Запасной вариант: `role_plague_m_daniel.wav` (bm_daniel, −2 полутона).

| файл | роль | сек | F0 | whisper en |
|---|---|---|---|---|
| p1_m.wav (= p1_m_lewis) | PLAGUE | 4.0 | 111 Гц | дословно |
| p1_m_lewis_alt.wav | PLAGUE | 3.8 | 116 Гц | дословно |
| p1_m_daniel.wav / _alt | PLAGUE | 2.7 / 3.1 | 116–117 Гц | дословно |
| n3_m.wav / _alt | NARRATOR | 6.7 / 6.0 | 134 Гц | дословно |
| n4_m.wav / _alt | NARRATOR | 11.0 / 11.4 | 128–132 Гц | дословно («13 minutes» цифрами) |

Рассказчик George ~133–139 Гц, Чума Lewis ~111 Гц: разница около 3,5 полутона, плюс медленнее.
