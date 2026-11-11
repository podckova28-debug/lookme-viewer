/* LookMe — Telegram Mini App.
 * Данные читаются из Google-таблицы «Лента образов» (листы «Образы», «Состав», «#Данные»).
 * Таблица должна быть открыта по ссылке на просмотр. Правки в таблице появляются в приложении
 * при следующем открытии (кэш — 5 минут).
 */
(function () {
  'use strict';

  var CONFIG = {
    sheetId: '10AjEv53PMaN1TlXLvd9r-sZQ0SmYpfqJHhzh7ZSER8s',
    gids: { looks: '0', items: '1404258100', products: '175139528' },
    bot: 'lookmewebbot',
    cacheKey: 'lookme_sheet_v1',
    cacheTtlMs: 5 * 60 * 1000,
    pageSize: 40
  };

  /* ------------------------------------------------------------------ Telegram */
  var tg = window.Telegram && window.Telegram.WebApp;
  var inTg = !!(tg && tg.initData);
  function tgAtLeast(v) { return inTg && typeof tg.isVersionAtLeast === 'function' && tg.isVersionAtLeast(v); }
  if (inTg) {
    document.documentElement.classList.add('in-tg');
    try { tg.ready(); tg.expand(); } catch (e) {}
    try { if (tgAtLeast('6.1')) { tg.setHeaderColor('#ffffff'); tg.setBackgroundColor('#ffffff'); } } catch (e) {}
  }
  function haptic() { try { if (tgAtLeast('6.1')) tg.HapticFeedback.impactOccurred('light'); } catch (e) {} }

  /* ------------------------------------------------------------------ helpers */
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function clean(s) { return String(s == null ? '' : s).replace(/\s+/g, ' ').trim(); }
  function bad(s) { return !s || /^#(N\/A|REF!|VALUE!|ERROR!|NAME\?)/i.test(s); }
  function digits(s) { var m = String(s || '').match(/\d{4,}/); return m ? m[0] : ''; }
  function int(s) { var n = parseInt(String(s || '').replace(/[^\d]/g, ''), 10); return isFinite(n) ? n : 0; }
  function money(s) {
    s = String(s || '').replace(/[^\d.,]/g, '');
    if (!s) return 0;
    if (s.indexOf('.') >= 0 && s.indexOf(',') >= 0) s = s.replace(/,/g, '');          // 4,219.00
    else if (/,\d{3}(,|$)/.test(s)) s = s.replace(/,/g, '');                           // 4,219
    else s = s.replace(',', '.');                                                      // 4219,50
    var n = Math.round(parseFloat(s));
    return isFinite(n) && n > 0 ? n : 0;
  }
  function rating(s) { var n = parseFloat(String(s || '').replace(',', '.')); return isFinite(n) && n > 0 ? Math.round(n * 10) / 10 : 0; }
  function fmt(n) { return Math.round(n).toLocaleString('ru-RU'); }
  function plural(n, one, few, many) {
    var m10 = n % 10, m100 = n % 100;
    if (m10 === 1 && m100 !== 11) return one;
    if (m10 >= 2 && m10 <= 4 && (m100 < 12 || m100 > 14)) return few;
    return many;
  }

  function parseCSV(text) {
    var rows = [], row = [], field = '', i = 0, q = false, c;
    while (i < text.length) {
      c = text[i];
      if (q) {
        if (c === '"') { if (text[i + 1] === '"') { field += '"'; i += 2; continue; } q = false; i++; continue; }
        field += c; i++; continue;
      }
      if (c === '"') { q = true; i++; continue; }
      if (c === ',') { row.push(field); field = ''; i++; continue; }
      if (c === '\r') { i++; continue; }
      if (c === '\n') { row.push(field); rows.push(row); row = []; field = ''; i++; continue; }
      field += c; i++;
    }
    if (field !== '' || row.length) { row.push(field); rows.push(row); }
    return rows;
  }
  function toObjects(text) {
    var rows = parseCSV(text);
    var head = (rows.shift() || []).map(function (h) { return clean(h); });
    return rows.map(function (r) {
      var o = {};
      head.forEach(function (h, i) { if (h && !(h in o)) o[h] = r[i] == null ? '' : r[i]; });
      return o;
    });
  }

  /* ------------------------------------------------------------------ catalog */
  var ALIAS = { 'Ботильноы': 'Ботильоны', 'Сумк': 'Сумка', 'Блузка': 'Блуза', 'Жилетка': 'Жилет', 'Каблуки': 'Туфли' };
  var GROUPS = [
    ['Головной убор', ['Шапка', 'Кепка', 'Берет', 'Наушники', 'Платок']],
    ['Верх', ['Блуза', 'Боди', 'Бомбер', 'Водолазка', 'Джемпер', 'Дубленка', 'Жакет', 'Жилет', 'Кардиган', 'Корсет', 'Костюм', 'Куртка', 'Лонгслив', 'Майка', 'Пальто', 'Пиджак', 'Пижама', 'Платье', 'Плащ', 'Пуховик', 'Рубашка', 'Свитер', 'Свитшот', 'Топ', 'Футболка', 'Худи', 'Шуба']],
    ['Низ', ['Брюки', 'Джинсы', 'Леггинсы', 'Шорты', 'Штаны', 'Юбка']],
    ['Обувь', ['Балетки', 'Босоножки', 'Ботильоны', 'Ботинки', 'Ботфорты', 'Казаки', 'Кеды', 'Кроссовки', 'Лоферы', 'Обувь', 'Полуботинки', 'Полусапоги', 'Сапоги', 'Тапочки', 'Туфли', 'Угги']],
    ['Сумки', ['Сумка', 'Рюкзак']],
    ['Аксессуары', ['Ремень', 'Очки', 'Шарф', 'Перчатки', 'Серьги', 'Носки', 'Колготки', 'Гетры']]
  ];
  var GROUP_OF = {};
  GROUPS.forEach(function (g) { g[1].forEach(function (c) { GROUP_OF[c] = g[0]; }); });
  function normCat(s) {
    s = clean(s);
    if (!s) return '';
    s = s.charAt(0).toUpperCase() + s.slice(1).toLowerCase();
    return ALIAS[s] || s;
  }
  function groupOf(cat) { return GROUP_OF[cat] || 'Другое'; }

  var STYLE_LABEL = { 'Повседневный': 'Повседневные', 'Досуговый': 'Досуговые', 'Деловой': 'Деловые', 'Вечерний': 'Вечерние', 'Домашний': 'Домашние' };
  function styleLabel(s) { return STYLE_LABEL[s] || s; }

  function weatherOf(w) {
    w = String(w || '').toLowerCase();
    return {
      temp: w.indexOf('тепл') >= 0 ? 'warm' : w.indexOf('прохлад') >= 0 ? 'cool' : w.indexOf('холод') >= 0 ? 'cold' : '',
      rain: w.indexOf('осадки') >= 0 && w.indexOf('без осадков') < 0
    };
  }
  var TEMP_LABEL = { warm: 'Тепло', cool: 'Прохладно', cold: 'Холодно' };
  function seasonTemps(d) {
    var m = (d || new Date()).getMonth(); // 0 = январь
    if (m === 11 || m <= 1) return ['cold'];
    if (m === 2 || m === 10) return ['cold', 'cool'];
    if (m === 3 || m === 9) return ['cool'];
    if (m === 4 || m === 8) return ['cool', 'warm'];
    return ['warm'];
  }
  function seasonScore(look) {
    var t = seasonTemps(), i = t.indexOf(look.w.temp);
    return i < 0 ? 0 : 2 - i;
  }

  function drivePhoto(v, width) {
    v = clean(v);
    if (!v) return '';
    var m = v.match(/\/d\/([\w-]{20,})/) || v.match(/[?&]id=([\w-]{20,})/);
    var id = m ? m[1] : (/^[\w-]{20,}$/.test(v) ? v : '');
    if (id) return 'https://lh3.googleusercontent.com/d/' + id + '=w' + (width || 800);
    return /^https?:\/\//.test(v) ? v : '';
  }
  function wbPhoto(u) {
    u = clean(u);
    if (!/^https?:\/\//.test(u)) return '';
    if (/\/images\/?$/.test(u)) u = u.replace(/\/?$/, '/') + 'c516x688/1.webp';
    return u.replace('/images/big/', '/images/c516x688/');
  }
  function bigPhoto(u) { return String(u || '').replace('/images/c516x688/', '/images/big/').replace(/=w\d+$/, '=w1400'); }
  function wbUrl(art, u) {
    u = clean(u);
    if (/^https?:\/\/(www\.)?wildberries\.ru\//.test(u)) return u;
    return art ? 'https://www.wildberries.ru/catalog/' + art + '/detail.aspx' : '';
  }

  function buildModel(raw) {
    var productByArt = new Map(), lookById = new Map();

    toObjects(raw.products).forEach(function (r) {
      var art = digits(r['Артикулы']);
      if (!art) return;
      productByArt.set(art, {
        art: art,
        name: bad(r['Название']) ? '' : clean(r['Название']),
        price: money(r['Цена']),
        rating: rating(r['Рейтинг']),
        reviews: int(r['Кол-во оценок']),
        url: wbUrl(art, r['Ссылка на товар']),
        photo: wbPhoto(r['Ссылка на фото']) || wbPhoto(r['Фото']),
        cat: '',
        looks: []
      });
    });

    toObjects(raw.looks).forEach(function (r) {
      var id = int(r['№ образа']);
      var title = clean(r['Название']);
      if (!id || !title || bad(title)) return;
      lookById.set(id, {
        id: id,
        title: title,
        desc: bad(r['Описание']) ? '' : clean(r['Описание']),
        photo: drivePhoto(r['Ссылка на Фото (Drive)'] || r['Фото']),
        sheetPrice: money(r['Цена']),
        style: clean(r['Стиль']),
        weather: clean(r['Погода']),
        w: weatherOf(r['Погода']),
        items: []
      });
    });

    toObjects(raw.items).forEach(function (r) {
      var look = lookById.get(int(r['№ образа']));
      if (!look) return;
      var art = digits(r['Цифра артикула']) || digits(r['Ссылка']);
      var cat = normCat(r['Предмет']);
      var row = {
        art: art,
        name: bad(r['Название']) ? '' : clean(r['Название']),
        price: money(r['Цена']),
        rating: rating(r['Рейтинг']),
        reviews: int(r['Кол-во оценок']),
        url: wbUrl(art, r['Ссылка']),
        photo: wbPhoto(r['Ссылка на фото']),
        cat: cat,
        looks: []
      };
      var p = art && productByArt.get(art);
      if (!p) { p = row; if (art) productByArt.set(art, p); }
      else {
        ['name', 'price', 'rating', 'reviews', 'photo', 'url', 'cat'].forEach(function (k) { if (!p[k] && row[k]) p[k] = row[k]; });
      }
      if (look.items.indexOf(p) < 0) look.items.push(p);
      if (p.looks.indexOf(look.id) < 0) p.looks.push(look.id);
    });

    var looks = Array.from(lookById.values()).filter(function (l) { return l.photo; });
    looks.forEach(function (l) {
      l.cats = l.items.map(function (p) { return p.cat; }).filter(Boolean);
      l.search = (l.title + ' ' + l.desc + ' ' + l.style + ' ' + l.cats.join(' ') + ' ' +
        l.items.map(function (p) { return p.name; }).join(' ')).toLowerCase();
    });
    looks.sort(function (a, b) { return seasonScore(b) - seasonScore(a) || b.id - a.id; });

    var products = Array.from(productByArt.values()).filter(function (p) { return p.photo && (p.name || p.cat); });
    products.forEach(function (p) { p.search = (p.name + ' ' + p.cat).toLowerCase(); });
    products.sort(function (a, b) { return (b.price > 0) - (a.price > 0) || b.reviews - a.reviews; });

    return { looks: looks, lookById: lookById, products: products, productByArt: productByArt };
  }

  function lookPrice(l) {
    var sum = 0, missing = 0;
    l.items.forEach(function (p) { if (p.price) sum += p.price; else missing++; });
    if (sum && !missing) return { text: '≈ ' + fmt(sum) + ' ₽', value: sum };
    if (l.sheetPrice) return { text: '≈ ' + fmt(l.sheetPrice) + ' ₽', value: l.sheetPrice };
    if (sum) return { text: 'от ' + fmt(sum) + ' ₽', value: sum };
    return null;
  }

  /* ------------------------------------------------------------------ data loading */
  var model = null, rawTexts = null;

  function csvUrl(gid) {
    return 'https://docs.google.com/spreadsheets/d/' + CONFIG.sheetId + '/export?format=csv&gid=' + gid;
  }
  function fetchText(url) {
    return fetch(url, { cache: 'no-store' }).then(function (r) {
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.text();
    });
  }
  function readCache() {
    try { var c = JSON.parse(localStorage.getItem(CONFIG.cacheKey) || 'null'); return c && c.looks ? c : null; } catch (e) { return null; }
  }
  function writeCache(raw) {
    try { localStorage.setItem(CONFIG.cacheKey, JSON.stringify(Object.assign({ t: Date.now() }, raw))); } catch (e) {}
  }
  function loadFresh() {
    var g = CONFIG.gids;
    return Promise.all([fetchText(csvUrl(g.looks)), fetchText(csvUrl(g.items)), fetchText(csvUrl(g.products))])
      .then(function (t) {
        if (t[0].trim().charAt(0) === '<') throw new Error('Таблица закрыта для просмотра по ссылке');
        return { looks: t[0], items: t[1], products: t[2] };
      });
  }
  function setData(raw) {
    rawTexts = raw;
    model = buildModel(raw);
  }

  /* ------------------------------------------------------------------ favorites */
  var fav = { looks: [], items: [] };
  var useCloud = tgAtLeast('6.9') && tg.CloudStorage;
  function favLoad() {
    var local = {};
    try { local = JSON.parse(localStorage.getItem('lookme_fav') || '{}') || {}; } catch (e) {}
    fav.looks = (local.looks || []).map(Number);
    fav.items = (local.items || []).map(String);
    if (!useCloud) return Promise.resolve();
    return new Promise(function (resolve) {
      try {
        tg.CloudStorage.getItems(['fav_looks', 'fav_items'], function (err, v) {
          if (!err && v) {
            if (v.fav_looks) fav.looks = v.fav_looks.split(',').filter(Boolean).map(Number);
            if (v.fav_items) fav.items = v.fav_items.split(',').filter(Boolean);
          }
          resolve();
        });
      } catch (e) { resolve(); }
      setTimeout(resolve, 1500);
    });
  }
  function favSave() {
    try { localStorage.setItem('lookme_fav', JSON.stringify(fav)); } catch (e) {}
    if (useCloud) {
      try {
        tg.CloudStorage.setItem('fav_looks', fav.looks.join(','));
        tg.CloudStorage.setItem('fav_items', fav.items.slice(-300).join(','));
      } catch (e) {}
    }
  }
  function isFav(kind, id) { return kind === 'look' ? fav.looks.indexOf(Number(id)) >= 0 : fav.items.indexOf(String(id)) >= 0; }
  function toggleFav(kind, id) {
    var list = kind === 'look' ? fav.looks : fav.items;
    var key = kind === 'look' ? Number(id) : String(id);
    var i = list.indexOf(key);
    if (i >= 0) list.splice(i, 1); else list.push(key);
    favSave();
    haptic();
    return i < 0;
  }

  /* ------------------------------------------------------------------ WB live prices (best effort) */
  var wbTried = new Set();
  function refreshFromWB(products) {
    var arts = products.filter(function (p) { return p.art && !wbTried.has(p.art); }).map(function (p) { return p.art; }).slice(0, 60);
    if (!arts.length || !window.fetch || !window.AbortController) return;
    arts.forEach(function (a) { wbTried.add(a); });
    var ctrl = new AbortController();
    var timer = setTimeout(function () { ctrl.abort(); }, 6000);
    var route = location.hash;
    fetch('https://card.wb.ru/cards/v4/detail?appType=1&curr=rub&dest=-1257786&nm=' + arts.join(';'), { signal: ctrl.signal })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (j) {
        clearTimeout(timer);
        var list = j && (j.products || (j.data && j.data.products)) || [];
        var changed = false;
        list.forEach(function (w) {
          var p = model && model.productByArt.get(String(w.id));
          if (!p) return;
          var size = (w.sizes || []).filter(function (s) { return s && s.price; })[0];
          var kop = size ? (size.price.product || size.price.total) : (w.salePriceU || 0);
          if (kop > 0) { p.price = Math.round(kop / 100); changed = true; }
          var rt = w.reviewRating || w.nmReviewRating || w.rating;
          if (rt) p.rating = rating(rt);
          var fb = w.feedbacks != null ? w.feedbacks : w.nmFeedbacks;
          if (fb != null) p.reviews = int(fb);
        });
        if (changed && location.hash === route) render({ keepScroll: true });
      })
      .catch(function () { clearTimeout(timer); });
  }

  /* ------------------------------------------------------------------ UI pieces */
  var HEART = '<svg viewBox="0 0 24 24"><path d="M12 20.5s-7.5-4.6-7.5-10.2A4.3 4.3 0 0 1 12 7.6a4.3 4.3 0 0 1 7.5 2.7c0 5.6-7.5 10.2-7.5 10.2z"/></svg>';
  function heart(kind, id) {
    var on = isFav(kind, id);
    return '<span class="heart' + (on ? ' on' : '') + '" role="button" tabindex="0" data-fav="' + kind + ':' + esc(id) +
      '" aria-pressed="' + on + '" aria-label="В избранное">' + HEART + '</span>';
  }
  function img(src, alt) {
    return '<div class="img-fallback">Фото недоступно</div>' +
      (src ? '<img loading="lazy" decoding="async" src="' + esc(src) + '" alt="' + esc(alt || '') + '" onerror="this.remove()">' : '');
  }
  function lookCard(l) {
    return '<a class="card" href="#/look/' + l.id + '">' +
      '<div class="ph">' + img(l.photo, l.title) + '</div>' + heart('look', l.id) +
      '<div class="body"><div class="title">' + esc(l.title) + '</div></div></a>';
  }
  function priceHtml(p) { return p.price ? fmt(p.price) + ' ₽' : '<span class="meta">Цена на WB</span>'; }
  function productCard(p) {
    return '<a class="card" href="#/product/' + p.art + '">' +
      '<div class="ph">' + img(p.photo, p.name) + '</div>' + heart('item', p.art) +
      '<div class="body"><div class="title">' + esc(p.name || p.cat) + '</div>' +
      '<div class="price">' + priceHtml(p) + '</div></div></a>';
  }
  function emptyState(title, text) { return '<div class="empty"><b>' + esc(title) + '</b>' + esc(text || '') + '</div>'; }
  function backLink() { return '<a class="back" href="#" data-back>‹ Назад</a>'; }

  var toastTimer;
  function toast(msg) {
    var el = document.querySelector('.toast');
    if (!el) { el = document.createElement('div'); el.className = 'toast'; document.body.appendChild(el); }
    el.textContent = msg;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { el.remove(); }, 2200);
  }

  function openExternal(url) {
    if (!url) return;
    if (inTg) { try { tg.openLink(url); return; } catch (e) {} }
    window.open(url, '_blank', 'noopener');
  }
  function shareLook(l) {
    var link = 'https://t.me/' + CONFIG.bot + '?startapp=look_' + l.id;
    var text = l.title + ' — образ в LookMe';
    if (inTg) {
      try { tg.openTelegramLink('https://t.me/share/url?url=' + encodeURIComponent(link) + '&text=' + encodeURIComponent(text)); return; } catch (e) {}
    }
    if (navigator.share) { navigator.share({ title: 'LookMe', text: text, url: link }).catch(function () {}); return; }
    try { navigator.clipboard.writeText(link).then(function () { toast('Ссылка скопирована'); }); } catch (e) { toast(link); }
  }

  /* ------------------------------------------------------------------ state */
  var state = {
    looks: { style: '', q: '', cats: [], bag: '', temps: [], rain: false, shown: CONFIG.pageSize },
    products: { group: '', q: '', shown: CONFIG.pageSize },
    favTab: 'looks',
    ai: { style: '', temp: '', rain: '', want: [], done: false }
  };
  var scrollMemo = {};

  function filterLooks(f) {
    var q = f.q.trim().toLowerCase();
    return model.looks.filter(function (l) {
      if (f.style && l.style !== f.style) return false;
      if (q && l.search.indexOf(q) < 0) return false;
      for (var i = 0; i < f.cats.length; i++) if (l.cats.indexOf(f.cats[i]) < 0) return false;
      var hasBag = l.cats.indexOf('Сумка') >= 0;
      if (f.bag === 'yes' && !hasBag) return false;
      if (f.bag === 'no' && hasBag) return false;
      if (f.temps.length && f.temps.indexOf(l.w.temp) < 0) return false;
      if (f.rain && !l.w.rain) return false;
      return true;
    });
  }
  function filterCount(f) { return f.cats.length + (f.bag ? 1 : 0) + f.temps.length + (f.rain ? 1 : 0); }

  /* ------------------------------------------------------------------ views */
  var view = document.getElementById('view');

  function viewHome() {
    var u = inTg && tg.initDataUnsafe && tg.initDataUnsafe.user;
    var name = u ? clean((u.first_name || '') + ' ' + (u.last_name || '')) : '';
    var avatar = u && u.photo_url
      ? '<img src="' + esc(u.photo_url) + '" alt="">'
      : esc((name || 'L').charAt(0).toUpperCase());

    var pool = model.looks.filter(function (l) { return seasonScore(l) > 0; });
    if (!pool.length) pool = model.looks;
    var day = Math.floor(Date.now() / 864e5);
    var daily = pool[day % pool.length];
    var price = daily && lookPrice(daily);
    var products = model.products.filter(function (p) { return p.price; }).slice(0, 12);

    return '<div class="greeting"><div class="avatar">' + avatar + '</div><div>' +
      '<div class="hello">Привет 👋' + (name ? ' ' + esc(name) : '') + '</div>' +
      '<div class="sub">Рады видеть Вас</div></div></div>' +
      (daily ? '<a class="hero" href="#/look/' + daily.id + '"><div class="ph">' + img(daily.photo, daily.title) + '</div>' +
        '<div class="body"><span class="badge">Образ дня</span><div class="title">' + esc(daily.title) + '</div>' +
        '<div class="desc">' + esc(daily.desc) + '</div>' +
        (price ? '<div class="price"><b>' + price.text + '</b></div>' : '') + '</div></a>' : '') +
      '<div class="section-head"><h2>Лента образов</h2><a href="#/looks">Смотреть все</a></div>' +
      '<div class="rail">' + model.looks.slice(0, 12).map(lookCard).join('') + '</div>' +
      '<div class="section-head"><h2>Лента товаров</h2><a href="#/products">Смотреть все</a></div>' +
      '<div class="rail">' + products.map(productCard).join('') + '</div>';
  }

  function lookGridHtml() {
    var f = state.looks, list = filterLooks(f);
    var shown = list.slice(0, f.shown);
    if (!list.length) return emptyState('Ничего не нашлось', 'Попробуйте изменить фильтры или запрос.');
    return '<div class="found">' + list.length + ' ' + plural(list.length, 'образ', 'образа', 'образов') + '</div>' +
      '<div class="grid">' + shown.map(lookCard).join('') + '</div>' +
      (list.length > shown.length ? '<button class="btn ghost" data-more="looks">Показать ещё</button>' : '');
  }
  function viewLooks() {
    var f = state.looks;
    var styles = [];
    model.looks.forEach(function (l) { if (l.style && styles.indexOf(l.style) < 0) styles.push(l.style); });
    var order = ['Повседневный', 'Досуговый', 'Деловой', 'Вечерний', 'Особый случай', 'Домашний'];
    styles.sort(function (a, b) { return (order.indexOf(a) + 1 || 99) - (order.indexOf(b) + 1 || 99); });
    var cnt = filterCount(f);
    return '<h1 class="page-title">Образы</h1>' +
      '<div class="chips solid">' +
      '<button class="chip' + (!f.style ? ' on' : '') + '" data-style="">Все</button>' +
      styles.map(function (s) { return '<button class="chip' + (f.style === s ? ' on' : '') + '" data-style="' + esc(s) + '">' + esc(styleLabel(s)) + '</button>'; }).join('') +
      '</div>' +
      '<div class="searchrow"><label class="search"><svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>' +
      '<input type="search" placeholder="Я ищу..." value="' + esc(f.q) + '" data-search="looks" enterkeyhint="search"></label>' +
      '<button class="filter-btn" data-open-filter aria-label="Фильтры"><svg viewBox="0 0 24 24"><path d="M4 7h10M18 7h2M4 17h4M12 17h8"/><circle cx="16" cy="7" r="2"/><circle cx="10" cy="17" r="2"/></svg>' +
      (cnt ? '<span class="count">' + cnt + '</span>' : '') + '</button></div>' +
      '<div id="lookGrid">' + lookGridHtml() + '</div>';
  }

  function viewLook(id) {
    var l = model.lookById.get(Number(id));
    if (!l) return backLink() + emptyState('Образ не найден', 'Возможно, его убрали из ленты.');
    var price = lookPrice(l);
    refreshFromWB(l.items);
    var tags = [l.style ? styleLabel(l.style) : '', l.w.temp ? TEMP_LABEL[l.w.temp] : '', l.w.rain ? 'Для дождя/снега' : '']
      .filter(Boolean).map(function (t) { return '<span class="tag">' + esc(t) + '</span>'; }).join('');
    return '<div class="detail">' + backLink() +
      '<div class="detail-photo">' + img(bigPhoto(l.photo), l.title) + heart('look', l.id) + '</div>' +
      '<h1>' + esc(l.title) + '</h1>' +
      (tags ? '<div class="tags">' + tags + '</div>' : '') +
      (l.desc ? '<p class="desc">' + esc(l.desc) + '</p>' : '') +
      (l.items.length ? '<div class="section-head"><h2 class="link">Состав образа</h2><span class="meta">' + l.items.length + ' ' + plural(l.items.length, 'вещь', 'вещи', 'вещей') + '</span></div>' +
        '<div class="rail">' + l.items.filter(function (p) { return p.art; }).map(productCard).join('') + '</div>' : '') +
      (price ? '<div class="total"><span>Образ целиком</span><b>' + price.text + '</b></div>' : '') +
      '<div class="btn-row"><button class="btn ghost" data-share="' + l.id + '">Поделиться</button>' +
      '<a class="btn" href="#/looks">Ещё образы</a></div>' +
      '</div>';
  }

  function productGridHtml() {
    var f = state.products, q = f.q.trim().toLowerCase();
    var list = model.products.filter(function (p) {
      if (f.group && groupOf(p.cat) !== f.group) return false;
      return !q || p.search.indexOf(q) >= 0;
    });
    if (!list.length) return emptyState('Ничего не нашлось', 'Попробуйте другой запрос.');
    var shown = list.slice(0, f.shown);
    return '<div class="found">' + list.length + ' ' + plural(list.length, 'товар', 'товара', 'товаров') + '</div>' +
      '<div class="grid">' + shown.map(productCard).join('') + '</div>' +
      (list.length > shown.length ? '<button class="btn ghost" data-more="products">Показать ещё</button>' : '');
  }
  function viewProducts() {
    var f = state.products;
    var groups = [];
    model.products.forEach(function (p) { var g = p.cat && groupOf(p.cat); if (g && groups.indexOf(g) < 0) groups.push(g); });
    var order = GROUPS.map(function (g) { return g[0]; }).concat(['Другое']);
    groups.sort(function (a, b) { return order.indexOf(a) - order.indexOf(b); });
    return '<h1 class="page-title">Товары</h1>' +
      '<div class="chips solid"><button class="chip' + (!f.group ? ' on' : '') + '" data-group="">Все</button>' +
      groups.map(function (g) { return '<button class="chip' + (f.group === g ? ' on' : '') + '" data-group="' + esc(g) + '">' + esc(g) + '</button>'; }).join('') +
      '</div>' +
      '<div class="searchrow"><label class="search"><svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>' +
      '<input type="search" placeholder="Я ищу..." value="' + esc(f.q) + '" data-search="products" enterkeyhint="search"></label></div>' +
      '<div id="productGrid">' + productGridHtml() + '</div>';
  }

  function viewProduct(art) {
    var p = model.productByArt.get(String(art));
    if (!p) return backLink() + emptyState('Товар не найден', '');
    refreshFromWB([p]);
    var looks = p.looks.map(function (id) { return model.lookById.get(id); }).filter(function (l) { return l && l.photo; });
    return '<div class="detail">' + backLink() +
      '<div class="detail-photo">' + img(bigPhoto(p.photo), p.name) + heart('item', p.art) + '</div>' +
      '<h1>' + esc(p.name || p.cat) + '</h1>' +
      (p.rating ? '<div class="rating">★ <b>' + String(p.rating).replace('.', ',') + '</b>' +
        (p.reviews ? ' · ' + fmt(p.reviews) + ' ' + plural(p.reviews, 'оценка', 'оценки', 'оценок') : '') + '</div>' : '') +
      '<div class="total"><span>Цена на Wildberries</span><b>' + (p.price ? fmt(p.price) + ' ₽' : 'уточните на WB') + '</b></div>' +
      '<button class="btn" data-open="' + esc(p.url) + '">Открыть на Wildberries</button>' +
      (looks.length ? '<div class="section-head"><h2>Образы с этой вещью</h2></div><div class="grid">' + looks.map(lookCard).join('') + '</div>' : '') +
      '</div>';
  }

  function viewFavorites() {
    var tab = state.favTab;
    var body;
    if (tab === 'looks') {
      var looks = fav.looks.slice().reverse().map(function (id) { return model.lookById.get(id); }).filter(Boolean);
      body = looks.length ? '<div class="grid">' + looks.map(lookCard).join('') + '</div>'
        : emptyState('Пока пусто', 'Нажмите ♥ на образе, чтобы сохранить его здесь.');
    } else {
      var items = fav.items.slice().reverse().map(function (a) { return model.productByArt.get(a); }).filter(Boolean);
      body = items.length ? '<div class="grid">' + items.map(productCard).join('') + '</div>'
        : emptyState('Пока пусто', 'Нажмите ♥ на вещи, чтобы сохранить её здесь.');
    }
    return '<h1 class="page-title">Избранное</h1>' +
      '<div class="segmented"><button class="' + (tab === 'looks' ? 'on' : '') + '" data-favtab="looks">Образы</button>' +
      '<button class="' + (tab === 'items' ? 'on' : '') + '" data-favtab="items">Вещи</button></div>' + body;
  }

  function aiResults() {
    var a = state.ai;
    var adj = { warm: ['cool'], cool: ['warm', 'cold'], cold: ['cool'] };
    return model.looks.map(function (l) {
      var s = 0;
      if (a.style) s += l.style === a.style ? 3 : -2;
      if (a.temp) s += l.w.temp === a.temp ? 3 : (adj[a.temp] || []).indexOf(l.w.temp) >= 0 ? 0 : -3;
      if (a.rain === 'yes') s += l.w.rain ? 1 : 0;
      if (a.rain === 'no') s += l.w.rain ? -1 : 0;
      a.want.forEach(function (c) { s += l.cats.indexOf(c) >= 0 ? 2 : -1; });
      return { l: l, s: s };
    }).sort(function (x, y) { return y.s - x.s || y.l.id - x.l.id; }).slice(0, 6).map(function (x) { return x.l; });
  }
  function viewAI() {
    var a = state.ai;
    var styles = ['Повседневный', 'Деловой', 'Вечерний', 'Досуговый'];
    var want = ['Джинсы', 'Брюки', 'Юбка', 'Платье', 'Кроссовки', 'Ботинки', 'Туфли', 'Сумка'];
    function opt(attr, val, label, on) { return '<button class="chip' + (on ? ' on' : '') + '" data-ai="' + attr + '" data-val="' + esc(val) + '">' + esc(label) + '</button>'; }
    var html = '<h1 class="page-title">ИИ‑стилист</h1>' +
      '<div class="ai-intro"><h2>Подберём образ за 10 секунд</h2><p>Ответьте на пару вопросов, и мы предложим готовые образы со ссылками на вещи. Скоро здесь появится подбор по фото.</p></div>' +
      '<div class="q"><h3>Куда идём?</h3><div class="opts">' + styles.map(function (s) { return opt('style', s, styleLabel(s), a.style === s); }).join('') + '</div></div>' +
      '<div class="q"><h3>Какая погода?</h3><div class="opts">' + ['warm', 'cool', 'cold'].map(function (t) { return opt('temp', t, TEMP_LABEL[t], a.temp === t); }).join('') + '</div></div>' +
      '<div class="q"><h3>Осадки?</h3><div class="opts">' + opt('rain', 'no', 'Без осадков', a.rain === 'no') + opt('rain', 'yes', 'Дождь или снег', a.rain === 'yes') + '</div></div>' +
      '<div class="q"><h3>Что обязательно в образе? <span class="meta">(необязательно)</span></h3><div class="opts">' +
      want.map(function (c) { return opt('want', c, c, a.want.indexOf(c) >= 0); }).join('') + '</div></div>' +
      '<button class="btn" data-ai-go>Подобрать образ</button>';
    if (a.done) {
      var res = aiResults();
      html += '<div class="section-head" id="aiResults"><h2>Вам подойдут</h2></div>' +
        (res.length ? '<div class="grid">' + res.map(lookCard).join('') + '</div>' : emptyState('Ничего не нашлось', ''));
    }
    return html;
  }

  /* ------------------------------------------------------------------ filter sheet */
  var sheet = document.getElementById('sheet');
  var backdrop = document.getElementById('sheetBackdrop');
  var draft = null;

  function renderSheet() {
    var present = {};
    model.looks.forEach(function (l) { l.cats.forEach(function (c) { present[c] = 1; }); });
    function chip(attr, val, label, on) { return '<button class="chip' + (on ? ' on' : '') + '" data-f="' + attr + '" data-val="' + esc(val) + '">' + esc(label) + '</button>'; }
    var groups = GROUPS.filter(function (g) { return g[0] !== 'Сумки'; }).map(function (g) {
      var cats = g[1].filter(function (c) { return present[c]; });
      if (!cats.length) return '';
      return '<div class="fgroup"><h4>' + esc(g[0]) + '</h4><div class="opts">' +
        cats.map(function (c) { return chip('cat', c, c, draft.cats.indexOf(c) >= 0); }).join('') + '</div></div>';
    }).join('');
    var n = filterLooks(draft).length;
    sheet.innerHTML = '<div class="grabber"></div>' +
      '<div class="sheet-head"><h2>Выберите параметры</h2><button class="close" data-close-sheet aria-label="Закрыть">×</button></div>' +
      groups +
      '<div class="fgroup"><h4>Сумки</h4><div class="opts">' + chip('bag', 'yes', 'Есть в образе', draft.bag === 'yes') + chip('bag', 'no', 'Нет в образе', draft.bag === 'no') + '</div></div>' +
      '<div class="fgroup"><h4>Погода</h4><div class="opts">' +
      ['warm', 'cool', 'cold'].map(function (t) { return chip('temp', t, TEMP_LABEL[t], draft.temps.indexOf(t) >= 0); }).join('') +
      chip('rain', '1', 'Для дождя/снега', draft.rain) + '</div></div>' +
      '<div class="sheet-actions"><button class="btn ghost" data-reset-filter>Сбросить</button>' +
      '<button class="btn" data-apply-filter>Показать ' + n + ' ' + plural(n, 'образ', 'образа', 'образов') + '</button></div>';
  }
  function openSheet() {
    var f = state.looks;
    draft = { style: f.style, q: f.q, cats: f.cats.slice(), bag: f.bag, temps: f.temps.slice(), rain: f.rain };
    renderSheet();
    sheet.hidden = false; backdrop.hidden = false;
    document.body.style.overflow = 'hidden';
  }
  function closeSheet() {
    sheet.hidden = true; backdrop.hidden = true;
    document.body.style.overflow = '';
  }

  /* ------------------------------------------------------------------ router */
  var TABS = ['home', 'looks', 'ai', 'products', 'favorites'];
  var navDepth = 0, currentKey = '';

  function route() {
    var h = location.hash.replace(/^#\/?/, '').split('/');
    return { name: h[0] || 'home', arg: h[1] ? decodeURIComponent(h[1]) : '' };
  }

  function render(opts) {
    opts = opts || {};
    var r = route();
    var key = r.name + '/' + r.arg;
    if (currentKey && currentKey !== key) scrollMemo[currentKey] = window.scrollY;
    if (!model) { renderLoading(); return; }
    var html;
    switch (r.name) {
      case 'looks': html = viewLooks(); break;
      case 'look': html = viewLook(r.arg); break;
      case 'products': html = viewProducts(); break;
      case 'product': html = viewProduct(r.arg); break;
      case 'favorites': html = viewFavorites(); break;
      case 'ai': html = viewAI(); break;
      default: html = viewHome(); r.name = 'home';
    }
    var y = opts.keepScroll ? window.scrollY : (scrollMemo[key] || 0);
    view.innerHTML = html;
    currentKey = key;
    window.scrollTo(0, (opts.keepScroll || TABS.indexOf(r.name) >= 0) ? y : 0);

    var tab = TABS.indexOf(r.name) >= 0 ? r.name : (r.name === 'look' ? 'looks' : r.name === 'product' ? 'products' : '');
    Array.prototype.forEach.call(document.querySelectorAll('.tabbar a'), function (a) {
      a.classList.toggle('on', a.getAttribute('data-tab') === tab);
    });
    if (inTg && tgAtLeast('6.1')) {
      if (TABS.indexOf(r.name) < 0) tg.BackButton.show(); else tg.BackButton.hide();
    }
  }

  function renderLoading() {
    var sk = '';
    for (var i = 0; i < 4; i++) sk += '<div class="skeleton" style="aspect-ratio:3/4"></div>';
    view.innerHTML = '<div class="skeleton" style="height:48px;width:60%;margin:4px 0 24px"></div><div class="grid">' + sk + '</div>';
  }
  function renderError(err) {
    view.innerHTML = emptyState('Не удалось загрузить образы', (err && err.message ? err.message + '. ' : '') + 'Проверьте интернет и попробуйте ещё раз.') +
      '<button class="btn" data-retry>Повторить</button>';
  }

  function goBack() {
    if (navDepth > 0) { navDepth--; history.back(); }
    else location.replace('#/home');
  }

  /* ------------------------------------------------------------------ events */
  document.addEventListener('click', function (e) {
    var t = e.target;
    var el;

    if ((el = t.closest('[data-fav]'))) {
      e.preventDefault(); e.stopPropagation();
      var parts = el.getAttribute('data-fav').split(':');
      var on = toggleFav(parts[0], parts[1]);
      el.classList.toggle('on', on);
      el.setAttribute('aria-pressed', on);
      if (route().name === 'favorites') render({ keepScroll: true });
      return;
    }
    if ((el = t.closest('[data-back]'))) { e.preventDefault(); goBack(); return; }
    if ((el = t.closest('[data-open]'))) { e.preventDefault(); openExternal(el.getAttribute('data-open')); return; }
    if ((el = t.closest('[data-share]'))) { var l = model.lookById.get(Number(el.getAttribute('data-share'))); if (l) shareLook(l); return; }
    if ((el = t.closest('[data-retry]'))) { start(); return; }

    if ((el = t.closest('[data-style]'))) {
      state.looks.style = el.getAttribute('data-style'); state.looks.shown = CONFIG.pageSize;
      render({ keepScroll: true }); return;
    }
    if ((el = t.closest('[data-group]'))) {
      state.products.group = el.getAttribute('data-group'); state.products.shown = CONFIG.pageSize;
      render({ keepScroll: true }); return;
    }
    if ((el = t.closest('[data-more]'))) {
      var which = el.getAttribute('data-more');
      state[which].shown += CONFIG.pageSize;
      document.getElementById(which === 'looks' ? 'lookGrid' : 'productGrid').innerHTML = which === 'looks' ? lookGridHtml() : productGridHtml();
      return;
    }
    if ((el = t.closest('[data-favtab]'))) { state.favTab = el.getAttribute('data-favtab'); render({ keepScroll: true }); return; }

    if ((el = t.closest('[data-ai]'))) {
      var a = state.ai, k = el.getAttribute('data-ai'), v = el.getAttribute('data-val');
      if (k === 'want') { var i = a.want.indexOf(v); if (i >= 0) a.want.splice(i, 1); else a.want.push(v); }
      else a[k] = a[k] === v ? '' : v;
      render({ keepScroll: true }); return;
    }
    if ((el = t.closest('[data-ai-go]'))) {
      state.ai.done = true; render({ keepScroll: true });
      var res = document.getElementById('aiResults');
      if (res) res.scrollIntoView({ behavior: 'smooth', block: 'start' });
      return;
    }

    if ((el = t.closest('[data-open-filter]'))) { openSheet(); return; }
    if ((el = t.closest('[data-close-sheet]')) || t === backdrop) { closeSheet(); return; }
    if ((el = t.closest('[data-f]'))) {
      var fk = el.getAttribute('data-f'), fv = el.getAttribute('data-val');
      if (fk === 'cat' || fk === 'temp') {
        var arr = fk === 'cat' ? draft.cats : draft.temps, j = arr.indexOf(fv);
        if (j >= 0) arr.splice(j, 1); else arr.push(fv);
      } else if (fk === 'bag') draft.bag = draft.bag === fv ? '' : fv;
      else if (fk === 'rain') draft.rain = !draft.rain;
      renderSheet(); return;
    }
    if ((el = t.closest('[data-reset-filter]'))) { draft.cats = []; draft.bag = ''; draft.temps = []; draft.rain = false; renderSheet(); return; }
    if ((el = t.closest('[data-apply-filter]'))) {
      Object.assign(state.looks, { cats: draft.cats, bag: draft.bag, temps: draft.temps, rain: draft.rain, shown: CONFIG.pageSize });
      closeSheet(); render({ keepScroll: true }); return;
    }

    if ((el = t.closest('a[href^="#/"]'))) {
      var target = el.getAttribute('href');
      if (target === location.hash) { e.preventDefault(); window.scrollTo(0, 0); return; }
      if (!el.closest('.tabbar')) navDepth++;
      else navDepth = 0;
    }
  });

  document.addEventListener('keydown', function (e) {
    var el = e.target.closest && e.target.closest('[data-fav]');
    if (el && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); el.click(); }
    if (e.key === 'Escape' && !sheet.hidden) closeSheet();
  });

  var searchTimer;
  document.addEventListener('input', function (e) {
    var which = e.target.getAttribute && e.target.getAttribute('data-search');
    if (!which) return;
    state[which].q = e.target.value;
    state[which].shown = CONFIG.pageSize;
    clearTimeout(searchTimer);
    searchTimer = setTimeout(function () {
      if (which === 'looks') document.getElementById('lookGrid').innerHTML = lookGridHtml();
      else document.getElementById('productGrid').innerHTML = productGridHtml();
    }, 150);
  });

  window.addEventListener('hashchange', function () { closeSheet(); render(); });
  if (inTg && tgAtLeast('6.1')) tg.BackButton.onClick(goBack);

  /* ------------------------------------------------------------------ deep links */
  function startRoute() {
    var p = (inTg && tg.initDataUnsafe && tg.initDataUnsafe.start_param) || '';
    if (!p) {
      var qs = new URLSearchParams(location.search);
      p = qs.get('tgWebAppStartParam') || qs.get('startapp') || qs.get('look') || '';
    }
    p = String(p).trim();
    var m;
    if ((m = p.match(/^(?:look_?|l_?)?(\d{1,6})$/i))) return '#/look/' + m[1];
    if ((m = p.match(/^(?:item|product|p)_?(\d{4,})$/i))) return '#/product/' + m[1];
    if (TABS.indexOf(p) >= 0) return '#/' + p;
    return '';
  }

  /* ------------------------------------------------------------------ start */
  function start() {
    var cached = readCache();
    var deep = startRoute();
    if (deep && !location.hash.replace(/^#\/?/, '')) {
      history.replaceState(null, '', location.pathname + location.search + '#/home');
      history.pushState(null, '', location.pathname + location.search + deep);
      navDepth = 1;
    }
    var favReady = favLoad();
    if (cached) {
      try { setData(cached); } catch (e) { model = null; }
    }
    favReady.then(function () { render(); });

    if (cached && model && Date.now() - cached.t < CONFIG.cacheTtlMs) return;
    loadFresh().then(function (raw) {
      writeCache(raw);
      var same = rawTexts && raw.looks === rawTexts.looks && raw.items === rawTexts.items && raw.products === rawTexts.products;
      if (same) return;
      var active = document.activeElement && document.activeElement.getAttribute && document.activeElement.getAttribute('data-search');
      setData(raw);
      if (!active) favReady.then(function () { render({ keepScroll: true }); });
    }).catch(function (err) {
      if (!model) renderError(err);
    });
  }

  start();
})();
