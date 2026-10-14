/* Amir prestatie-meter: plak dit in de browserconsole terwijl het spel draait.
   Toont rechtsboven de FPS, de frametijd, de zwaarste functies en elke hapering,
   met waar in het level hij gebeurde. Haakt alleen in, verandert niets aan het spel.
   Stoppen: typ  __meterUit()  in de console, of herlaad de pagina. */
(() => {
  if (window.__meterAan){ console.log('meter draait al; __meterUit() om te stoppen'); return; }
  window.__meterAan = true;

  // de functies die we per beeld opmeten (bestaan ze niet, dan slaan we ze over)
  const NAMEN = ['scene','drawLichtkaart','drawLichtlaag','drawWaas','drawZon','drawVoorgrond','drawWeer',
    'drawSnowfall','updateSnowfall','updateWeer','drawWind','drawVeg','drawSchildStof','drawGrains','updateSand','updateSnowFx',
    'goudapenTeken','updateGoudapen','arenaTick','arenaHudTeken','baviaanTeken','drawAmirSchaduw',
    'drawClimb','drawGrotten','drawPlafond','drawZuilen','ravijnenTeken','drawHolte','savanneLaag',
    'dwarrelTeken','rijsTeken','drawMuur','drawMuurGrot','drawVillageFg'];

  let frameAcc = {};                 // ms per functie, in het huidige beeld
  const orig = {};
  for (const n of NAMEN){
    if (typeof window[n] !== 'function') continue;
    orig[n] = window[n];
    window[n] = function(){ const t = performance.now(); const r = orig[n].apply(this, arguments);
      frameAcc[n] = (frameAcc[n] || 0) + (performance.now() - t); return r; };
  }

  const venster = [];                // frametijden (ms) van de laatste ~3s
  const somFn = {};                  // cumulatieve ms per functie over het venster
  let somFrames = 0;
  const haper = [];                  // recente haperingen
  const DREMPEL = 45;                // ms: daarboven heet het een hapering

  let laatste = performance.now();
  const origLoop = window.loop;
  if (typeof origLoop !== 'function'){ console.warn('meter: window.loop niet gevonden, kan niet meten'); return; }
  window.loop = function(now){
    frameAcc = {};
    const t0 = performance.now();
    const r = origLoop.apply(this, arguments);
    const dt = performance.now() - t0;
    venster.push(dt); if (venster.length > 180) venster.shift();
    somFrames++;
    for (const k in frameAcc) somFn[k] = (somFn[k] || 0) + frameAcc[k];
    if (dt > DREMPEL){
      // de duurste deelfunctie, zonder de overkoepelende scene (die bevat de rest)
      let top = '', mx = 0; for (const k in frameAcc) if (k !== 'scene' && frameAcc[k] > mx){ mx = frameAcc[k]; top = k; }
      const sc = frameAcc['scene'] || 0;
      const wat = (mx >= sc * 0.5 && top) ? (top + ' ' + mx.toFixed(0) + 'ms') : ('scene ' + sc.toFixed(0) + 'ms');
      const lvl = (typeof level !== 'undefined' && level && level.name) || '?';
      const wx = (typeof world === 'number') ? Math.round(world) : '?';
      haper.unshift({ ms: Math.round(dt), top: wat, wx });
      if (haper.length > 6) haper.pop();
    }
    return r;
  };

  const box = document.createElement('div');
  box.style.cssText = 'position:fixed;top:8px;right:8px;z-index:2147483647;pointer-events:none;'
    + 'font:11px/1.35 ui-monospace,Menlo,Consolas,monospace;color:#d8f0c0;background:rgba(10,14,8,.82);'
    + 'border:1px solid #3a5a28;border-radius:8px;padding:8px 10px;max-width:320px;white-space:pre;'
    + 'text-shadow:0 1px 1px #000';
  document.body.appendChild(box);

  function q(a, p){ const s = [...a].sort((x,y)=>x-y); return s.length ? s[Math.min(s.length-1, Math.floor(p*s.length))] : 0; }
  const timer = setInterval(() => {
    if (!venster.length){ box.textContent = 'meter: wacht op beelden...'; return; }
    const p50 = q(venster,.5), p95 = q(venster,.95), mx = Math.max(...venster);
    const fps = p50 > 0 ? Math.round(1000/p50) : 0;
    const top = Object.entries(somFn).map(([k,v])=>[k, v/Math.max(1,somFrames)])
      .sort((a,b)=>b[1]-a[1]).slice(0,5)
      .map(([k,v])=>'  ' + k.padEnd(16).slice(0,16) + v.toFixed(2) + 'ms').join('\n');
    const lvl = (typeof level !== 'undefined' && level && level.name) || '?';
    const h = haper.length
      ? haper.map(x=>'  ' + (x.ms+'ms').padEnd(7) + x.top + '  @x' + x.wx).join('\n')
      : '  (nog geen hapering)';
    box.textContent =
      'AMIR METER   fps ' + fps + '\n' +
      'frame  p50 ' + p50.toFixed(1) + '  p95 ' + p95.toFixed(1) + '  max ' + mx.toFixed(0) + ' ms\n' +
      'level  ' + lvl + '\n' +
      'zwaarste functies (ms/beeld):\n' + (top || '  -') + '\n' +
      'haperingen (>' + DREMPEL + 'ms):\n' + h;
    // venster voor de functie-sommen langzaam laten vervagen zodat het meebeweegt
    if (somFrames > 180){ for (const k in somFn) somFn[k] *= 0.5; somFrames = Math.round(somFrames*0.5); }
  }, 500);

  window.__meterUit = () => {
    clearInterval(timer); box.remove();
    window.loop = origLoop; for (const n in orig) window[n] = orig[n];
    window.__meterAan = false; console.log('meter gestopt');
  };
  console.log('Amir meter aan. Speel een stukje; kijk rechtsboven. Stoppen: __meterUit()');
})();
