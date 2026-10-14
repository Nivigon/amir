/* Amir schok-herkomst: plak dit in de console terwijl het spel draait.
   Bij elk duur teken-moment (>16 ms) laat het zien UIT WELKE functie het komt,
   links onder en in de console. Zo weten we of de schokken bakwerk zijn (blur,
   per-pixel) of iets anders. Stoppen: __stapelUit(), of herlaad. */
(() => {
  if (window.__stapelAan){ console.log('draait al; __stapelUit() om te stoppen'); return; }
  window.__stapelAan = true;
  const proto = CanvasRenderingContext2D.prototype;
  const origDraw = proto.drawImage, origGet = proto.getImageData, origPut = proto.putImageData;
  const DREMPEL = 16;
  const log = [];

  // de aanroepende functie uit de stack halen (het spel is niet geminificeerd, dus echte namen)
  function herkomst(){
    const r = (new Error().stack || '').split('\n').slice(3, 7)
      .map(s => s.trim().replace(/^at\s+/, '').replace(/\s*\(.*$/, '').replace(/^.*\//, ''))
      .filter(s => s && !/^<anonymous>$/.test(s));
    return r.slice(0, 3).join(' < ') || '?';
  }
  function meet(naam, orig){
    return function(){
      const t = performance.now();
      const r = orig.apply(this, arguments);
      const d = performance.now() - t;
      if (d > DREMPEL){
        const a = arguments[0];
        const bron = naam !== 'drawImage' ? naam
          : (a && a.src ? a.src.split('/').slice(-1)[0] : (a ? (a.width || a.naturalWidth) + 'x' + (a.height || a.naturalHeight) + ' canvas' : '?'));
        const uit = herkomst();
        const x = (typeof world === 'number') ? Math.round(world) : '?';
        log.unshift({ ms: Math.round(d), op: naam, bron, uit, x });
        if (log.length > 10) log.pop();
        console.warn('[schok ' + Math.round(d) + 'ms] ' + naam + ' ' + bron + '  uit: ' + uit + '  @x' + x);
      }
      return r;
    };
  }
  proto.drawImage = meet('drawImage', origDraw);
  proto.getImageData = meet('getImageData', origGet);
  proto.putImageData = meet('putImageData', origPut);

  const box = document.createElement('div');
  box.style.cssText = 'position:fixed;left:8px;bottom:8px;z-index:2147483647;pointer-events:none;'
    + 'font:11px/1.35 ui-monospace,Menlo,Consolas,monospace;color:#ffe9c0;background:rgba(14,8,10,.88);'
    + 'border:1px solid #6a4848;border-radius:8px;padding:8px 10px;max-width:460px;white-space:pre-wrap;text-shadow:0 1px 1px #000';
  document.body.appendChild(box);
  const timer = setInterval(() => {
    box.textContent = 'SCHOKKEN (>' + DREMPEL + 'ms), met de functie die ze veroorzaakt:\n' + (log.length
      ? log.map(x => '  ' + (x.ms + 'ms').padEnd(7) + x.op + ' ' + x.bron + '\n       uit ' + x.uit + '  @x' + x.x).join('\n')
      : '  (nog geen schok gezien, speel een stukje)');
  }, 500);
  window.__stapelUit = () => { clearInterval(timer); box.remove(); proto.drawImage = origDraw; proto.getImageData = origGet; proto.putImageData = origPut; window.__stapelAan = false; console.log('schok-herkomst gestopt'); };
  console.log('Schok-herkomst aan. Speel tot het hapert; kijk linksonder of in de console. Stoppen: __stapelUit()');
})();
