/* comic sound words on key actions (world coordinates; claps get "¡CLAP!" automatically) */
const COMIC = {
  s03: [{ t: () => Lt('s03_02') + .05, w: '¡RIIING!', x: 1075, y: 560 }],
  s04: [{ t: () => Lm('s04_06', .12) + .45, w: '¡SPLASH!', x: 960, y: 700 }],
  s05: [{ t: () => Lm('s05_01', .86), w: '¡PLOF!', x: 360, y: 600 }],
  s06: [{ t: () => Lt('s06_06') + .35, w: '¡RASS RASS!', x: 830, y: 600, size: 72 }],
  s07: [{ t: () => Lm('s07_02', .6), w: '¡ÑIIIC!', x: 1060, y: 520, size: 70 }],
  s09: [{ t: () => Lm('s09_01', .55), w: '¡PLAF!', x: 1180, y: 480 }],
  s10: [{ t: () => Lt('s10_02') + .25, w: '¡PUM!', x: 880, y: 820 }, { t: () => Lt('s10_05') + .3, w: '¡ZAS!', x: 1500, y: 420 }],
  s13: [{ t: () => Lm('s13_03', .45), w: '¡FFFUU!', x: 960, y: 560, size: 80 }],
  s16: [{ t: () => Lm('s16_04', .9) + .05, w: '¡CHAS!', x: 1390, y: 470, size: 80 }],
};
