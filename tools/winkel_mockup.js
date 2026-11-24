// Mockup van de winkel als kamer (richting C, zie claude/winkel_c_ontwerp.md in het project): de echte winkelkamer met
// de bordjes, de uitstalplek en het doek als DOM erover. V=S (Spears) of V=V (Supplies). node tools/winkel_mockup.js [uitnaam]
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '..');
const srv = http.createServer((q, r) => { const f = path.join(ROOT, decodeURIComponent(q.url.split('?')[0]));
  fs.readFile(f, (e, d) => { if (e){ r.writeHead(404); r.end(); return; } r.writeHead(200, {'Content-Type': {'.html':'text/html','.js':'text/javascript','.png':'image/png','.json':'application/json','.webp':'image/webp','.jpg':'image/jpeg','.woff2':'font/woff2'}[path.extname(f)]||'application/octet-stream'}); r.end(d); }); })
.listen(0, async () => {
  const b = await chromium.launch(), p = await b.newPage({ viewport: { width: 1280, height: 720 } });
  p.on('pageerror', e => console.log('fout:', e.message));
  await p.goto('http://127.0.0.1:' + srv.address().port + '/amir-king-of-africa.html');
  await p.waitForFunction(() => typeof mpSoloOpen === 'function'); await p.waitForTimeout(1500);
  await p.evaluate(() => mpSoloOpen()); await p.waitForTimeout(1500);
  await p.evaluate(() => { pvp.inst.coop.winkelEerst = true; pvp.inst.coop.goud0 = 140; mpStart(); });
  await p.waitForFunction(() => pvp && pvp.coop && running && !laadWacht, null, { timeout: 120000 });
  await p.waitForTimeout(2000);
  await p.evaluate(() => { if (!pvp.coop.inWinkel) mpcWinkelIn(); });
  await p.waitForTimeout(4000);
  await p.evaluate(() => { world -= 740; facing = -1; });
  await p.waitForTimeout(1500);
  await p.evaluate((V) => {
    // HUD-hints weg voor de mockup
    pvp.banner=''; for (const s of ['#hint', '#pvpbanner', '#pvpscore', '#lives', '#hudrij', '#actiebalk', '#pausebtn']) document.querySelectorAll(s).forEach(e => e.style.display = 'none');
    const css = document.createElement('style'); css.textContent = `
      @font-face{font-family:'Bree';src:url(design/fonts/bree-serif.woff2) format('woff2')}
      #wm{position:fixed;inset:0;z-index:99999;pointer-events:none;font-family:'Bree',Georgia,serif}
      #wm img{position:absolute;image-rendering:auto}
      #wm .it{position:absolute;filter:drop-shadow(0 4px 3px rgba(0,0,0,.45))}
      #wm .tag{position:absolute;width:40px;height:98px;background:url(design/winkel_ui/label.png) center/100% 100% no-repeat;filter:drop-shadow(0 3px 2px rgba(0,0,0,.5))}
      #wm .tag span{position:absolute;left:0;right:0;top:50px;text-align:center;color:#f3dfb4;font-size:15px;line-height:1;text-shadow:0 1px 0 #1c1008}
      #wm .tag i{display:block;width:13px;height:13px;margin:3px auto 0;background:url(design/winkel_ui/munt.png) center/contain no-repeat}
      #wm .gloed{position:absolute;filter:drop-shadow(0 0 6px #ffd56a) drop-shadow(0 0 14px rgba(255,196,80,.8)) drop-shadow(0 4px 3px rgba(0,0,0,.45))}
      #wm .doek{position:absolute;left:1012px;top:60px;width:248px;height:507px;background:url(design/winkel_ui/doek.png) center/100% 100% no-repeat;filter:drop-shadow(0 8px 10px rgba(0,0,0,.55))}
      #wm .touw{position:absolute;top:0px;height:66px;width:3px;height:40px;background:#6b4a2a;border-left:1px solid #3a2414}
      #wm .doek .in{position:absolute;left:50px;right:50px;top:58px;bottom:62px;display:flex;flex-direction:column;align-items:center;text-align:center;color:#3a2414}
      #wm .doek h2{margin:6px 0 0;font-size:27px;line-height:1.02;font-weight:400;letter-spacing:.5px;color:#2e1a0c}
      #wm .doek .lijn{width:70%;height:2px;background:#5a3a1c;margin:10px 0;position:relative}
      #wm .doek .lijn::after{content:'';position:absolute;left:50%;top:-4px;width:8px;height:8px;background:#5a3a1c;transform:translateX(-50%) rotate(45deg)}
      #wm .doek .upg{font-size:11px;letter-spacing:1px;color:#6a3a12;text-transform:uppercase}
      #wm .doek p{margin:8px 0 0;font-size:15px;line-height:1.3;font-family:Georgia,serif;color:#3a2414}
      #wm .doek .sfeer{font-style:italic;font-size:13px;color:#6b5236;margin-top:12px}
      #wm .doek .prijs{margin-top:auto;font-size:30px;display:flex;align-items:center;gap:6px;color:#2e1a0c}
      #wm .doek .prijs i{width:28px;height:28px;background:url(design/winkel_ui/munt.png) center/contain no-repeat}
      #wm .knop{position:absolute;width:150px;height:100px;background:url(design/winkel_ui/knop.png) center/100% 100% no-repeat;display:flex;align-items:center;justify-content:center;color:#f3dfb4;font-size:30px;letter-spacing:2px;text-shadow:0 2px 0 #1c1008;filter:drop-shadow(0 4px 3px rgba(0,0,0,.5))}
      #wm .knop.klein{width:112px;height:62px;font-size:19px;letter-spacing:1px}
      #wm .goud{position:absolute;left:50%;top:14px;transform:translateX(-50%);display:flex;align-items:center;gap:8px;font-size:28px;color:#f6d77a;text-shadow:0 2px 0 #1c1008,0 0 6px rgba(0,0,0,.6)}
      #wm .goud i{width:30px;height:30px;background:url(design/winkel_ui/munt.png) center/contain no-repeat}
      #wm .naam{position:absolute;font-size:14px;color:#f3dfb4;text-shadow:0 1px 0 #1c1008,0 0 4px #1c1008}
      #wm .wolk{position:absolute;left:300px;top:232px;max-width:230px;padding:8px 12px;font-size:15px;color:#f3dfb4;background:rgba(28,16,8,.82);border-radius:4px;border:2px solid #5a3a1c}
    `; document.head.append(css);
    const w = document.createElement('div'); w.id = 'wm';
    const plain = javImg.src;
    const vert = (src, x, y, h, kl='it') => `<img class="${kl}" src="${src}" style="left:${x}px;top:${y}px;width:${h}px;transform-origin:0 0;transform:rotate(-90deg) translateX(-${h}px)">`;
    const tag = (x, y, prijs) => `<div class="tag" style="left:${x}px;top:${y}px"><span>${prijs}<i></i></span></div>`;
    const bordjes = ['Spears','Supplies','Charms','Team'].map((n,i)=>{
      const aan = (V==='S' && i===0) || (V==='V' && i===1);
      const x = 598 + i*100;
      return `<div class="touw" style="left:${x+22}px;top:186px;height:${aan?40:30}px"></div><div class="touw" style="left:${x+70}px;top:186px;height:${aan?40:30}px"></div>
        <div class="knop bord${aan?' aan':''}" style="left:${x}px;top:${aan?212:202}px">${n}</div>`;}).join('');
    const css2=document.createElement('style'); css2.textContent=`
      #wm .bord{width:96px;height:52px;font-size:16px;letter-spacing:.5px;opacity:.72;filter:brightness(.8) drop-shadow(0 3px 2px rgba(0,0,0,.5))}
      #wm .bord.aan{opacity:1;filter:drop-shadow(0 0 5px #ffd56a) drop-shadow(0 0 10px rgba(255,196,80,.6)) drop-shadow(0 3px 2px rgba(0,0,0,.5));color:#ffe6a6}
      #wm .wolk{left:40px;top:330px}`; document.head.append(css2);
    let stal = '', doek = '';
    if (V === 'S'){
      stal = `<img src="design/stad/wapenrek/wapenrek.png" style="left:628px;top:352px;width:310px;filter:drop-shadow(0 4px 4px rgba(0,0,0,.4))">
      ${vert(plain, 668, 318, 290)}${vert('design/speer/pathfinder/jav.png', 728, 318, 290)}${vert('design/speer/piercer/jav.png', 792, 318, 290)}${vert('design/speer/ardhi/jav.png', 852, 312, 296, 'gloed')}
      ${tag(664,532,10)}${tag(724,532,40)}${tag(788,532,40)}${tag(848,532,40)}`;
      doek = `<div class="upg">Upgrade of your plain spear</div><h2>Ardhi's<br>Reach</h2><div class="lijn"></div>
        <p>A hit can give you a life back.</p><p class="sfeer">"The root does not ask the rain to come. It waits, and drinks."</p><div class="prijs">40<i></i></div>`;
    } else {
      stal = `<img src="design/stad/binnen/plank_touw.png" style="left:630px;top:370px;width:300px;filter:drop-shadow(0 4px 4px rgba(0,0,0,.4))">
      <img class="gloed" src="items/potions/hppotion.png" style="left:668px;top:296px;height:80px">
      <img class="it" src="items/winkel/gif.png" style="left:752px;top:316px;height:60px">
      <img class="it" src="items/winkel/slot.png" style="left:840px;top:300px;height:76px">
      ${tag(666,432,5)}${tag(760,432,25)}${tag(852,432,45)}`;
      doek = `<h2>Gourd</h2><div class="lijn"></div><p>One life back, until your lives are full.</p>
        <p class="sfeer">"Drink slow. The road is long."</p><p style="font-size:13px;margin-top:14px;color:#6a3a12">You carry 1</p><div class="prijs">5<i></i></div>`;
    }
    w.innerHTML = `<div class="goud"><i></i>140</div>${bordjes}${stal}
      <div class="touw" style="left:1060px"></div><div class="touw" style="left:1210px"></div>
      <div class="doek"><div class="in">${doek}</div></div>
      <div class="knop" style="left:1061px;top:548px">BUY</div>
      <div class="knop klein" style="left:1150px;top:648px">Ready</div>
      <div class="knop klein" style="left:1030px;top:648px">Leave</div>
      <div class="wolk">Sharp spears for hunters, gourds for the wounded.</div>`;
    document.body.append(w);
  }, process.env.V);
  await p.waitForTimeout(1500);
  await p.screenshot({ path: (process.argv[2] || 'winkel_mockup') + '_' + (process.env.V || 'S') + '.png' });
  await b.close(); srv.close();
});
