"""Maak index.html van de Animeer tool Mkuki uit de ren-speer-tool plus D.json."""
import sys, json
src, dj, uit = sys.argv[1:4]
h = open(src).read().split('\n')
D = json.load(open(dj))
TW = {
 'idle_sp': ([11, 13], 'Grok zette het hoofd iets omhoog (hoofd komt uit het origineel).'),
 'ren_sp': ([3, 4, 10], '4 en 10 noodgreep (benen uit het origineel, vuist rafelig); 3 onderbeen achter de speer afgeknipt.'),
 'ren_ns': ([10], 'IoU 0,64.'),
 'jump_ns': ([3, 4, 5], 'Afzet met het hoofd van Grok; 4 en 5 IoU laag maar pose goed.'),
 'rol_sp': ([3, 16, 17, 18, 19, 20, 21, 22], 'Draaiende speer 16-22 (lengte 16 en 18 aangevuld); 3 en 19 geen vuist op alle handpunten; vanaf 11 hoofd van Grok.'),
 'rol_ns': ([14, 15, 16, 17, 18, 19, 20, 21, 23, 25], 'Ondersteboven 14-21 (vuisten wat anders); 25 hand reikt minder ver.'),
 'sluip_ns': ([15, 18, 19, 28], 'Ver been niet donker zoals in het origineel.'),
 'strike_sp': ([4, 9], '2-8 rug naar de camera; 4 leunt minder voorover, 9 staat rechter.'),
 'worp_sp': ([9, 13, 16, 17, 18], '9 speer naast de vuist; 13 vuist i.p.v. open hand; 16 arm te gestrekt; 17-18 voorste arm korter. Vanaf 12 zonder speer.'),
 'sweep_sp': ([3, 5, 6, 8, 9, 10, 13], 'Armen korter of hoger dan het origineel; 3, 5, 9 draaiende speer; 13 zijtrap.'),
 'combo_sp': ([3, 4, 8, 9, 13, 14, 15], '3 voeten smaller; 4 stompje stok; 8-9 vuist lager; 13-15 achterste vuist bij de heup.'),
 'stof_sp': ([8, 9, 11, 12, 13, 14], '8-9 hoger dan het origineel; 11-14 vuisten voor het gezicht waar het origineel de speer achter de rug heeft.'),
 'rolworp_sp': ([1, 5, 12, 13, 14, 15, 24, 26, 27], 'Speer 12-15 nakijken; 15-23 en 29-33 een Grok-beeld per groep; 24 arm lager; 26-27 draaiing.'),
}
for a in D['anims']:
    t = TW.get(a['id'])
    a['twijfel'] = t[0] if t else []
    a['twijfelTekst'] = t[1] if t else ''
def rep(i, old, new, cnt=1):
    assert h[i].count(old) >= 1, (i, old)
    h[i] = h[i].replace(old, new) if cnt == 0 else h[i].replace(old, new, cnt)
# kop
h[1] = '<title>Animeer tool Amir Mkuki</title>'
rep(92, 'Amir ren speer', 'Amir Mkuki')
h[97] = ('    <div class="row" style="gap:8px"><button class="ib" id="aprev" aria-label="Vorige animatie">&#8249;</button>'
         '<select id="animsel" aria-label="Animatie" style="flex:1;font-size:15px;font-weight:600"></select>'
         '<button class="ib" id="anext" aria-label="Volgende animatie">&#8250;</button></div>')
h[123] = ('      <p class="hint" id="vernote">Lijf zonder speer, dan de speer, dan de vuist (de hand om de schacht). '
          'Maskeer waar de speer achter het lijf moet (Achter) of waar het lijf ervoor moet (Voor item).</p>')
# extra kaart voor origineel en vuist, voor de Versie-kaart
for i, l in enumerate(h):
    if l.strip() == '<div class="right">':
        h[i] = l + '''
    <div class="card">
      <h2>Vergelijken en lagen</h2>
      <div class="seg" id="origseg"><button data-id="uit" class="on">Origineel uit</button><button data-id="naast">Ernaast</button><button data-id="over">Eroverheen</button><button data-id="knip">Knipperen</button></div>
      <div class="row">
        <div class="ctrl"><label for="origop">Doorzicht origineel <span class="val" id="origopval">50%</span></label><input type="range" id="origop" min="10" max="100" step="1" value="50"></div>
        <label class="chk"><input type="checkbox" id="showvuist" checked> Vuist over de speer</label>
        <label class="chk"><input type="checkbox" id="pfspeer"> Pathfinder Spear tonen</label>
      </div>
      <div class="row">
        <label class="chk lock"><input type="checkbox" id="fok"> Frame nagekeken</label>
        <span class="pill" id="okinfo"></span>
        <button class="ghost" id="nextopen">Naar volgende open frame</button>
      </div>
      <p class="hint" id="twijfel"></p>
      <p class="hint">Pathfinder Spear: alleen om te kijken. Plek, lengte en maskers blijven gelijk; het vaantje hangt stil naar beneden (in het spel waait het).</p>
      <p class="hint">Toets O wisselt het origineel (uit, ernaast, eroverheen). Het origineel heeft de speer nog in het beeld, dus je ziet meteen waar hij zat.</p>
    </div>'''
        break
# script: data
for i, l in enumerate(h):
    if l.startswith('const D='):
        h[i] = 'const D=' + json.dumps(D, separators=(',', ':'), ensure_ascii=False) + ';'
        di = i; break
J = '\n'.join(h)
def R(old, new):
    global J
    assert J.count(old) == 1, old
    J = J.replace(old, new)
R("const W=D.W,H=D.H,MX=110,MT=180,MB=30,SW=W+2*MX,SH=MT+H+MB,OX=MX,OY=MT;\nconst CW=D.canvasW,CH=D.canvasH,GROND=D.grond,ANCHOR=D.anchorX;",
  "let W,H,SW,SH,CW,CH,GROND,ANCHOR;const MX=110,MT=140,MB=30,OX=MX,OY=MT;\nlet origMode='uit',knipT=null,knipAan=false;")
R("const LSKEY='animeer-'+D.personage.toLowerCase()+'-v2';   // v2: de nieuwe lage sets", "const LSKEY='animeer-'+D.personage.toLowerCase()+'-v1';")
R("function preload(){A().frames.forEach(f=>img(f.src));",
  "function preload(){const s=A().sheet;img(s.f);img(s.o);if(s.v)img(s.v);")
# afmetingen per animatie
R("const stage=el('stage');stage.width=SW;stage.height=SH;const sctx=stage.getContext('2d');",
  """const stage=el('stage');const sctx=stage.getContext('2d');
// Elke animatie heeft zijn eigen canvasmaat; bij wisselen rekenen we het werkvlak opnieuw uit.
function dims(){const a=A();W=a.W;H=a.H;CW=a.canvasW;CH=a.canvasH;GROND=a.grond;ANCHOR=a.anchorX;
  SW=W+2*MX+(origMode==='naast'?W+MX:0);SH=MT+H+MB;
  for(const k in POOL){POOL[k].width=SW;POOL[k].height=SH}
  if(stage.width!==SW||stage.height!==SH){stage.width=SW;stage.height=SH;if(window.__zoomKlaar&&zoom>1)setZoom(zoom)}}
// Een frame uit een spriteblad tekenen
function cell(x,im,i,dx,dy,dw,dh){const a=A(),c=a.cols;x.drawImage(im,(i%c)*a.W,Math.floor(i/c)*a.H,a.W,a.H,dx,dy,dw,dh)}
dims();""")
R("const bim=img(f.src);", "const bim=img(A().sheet.f);")
R("x.globalAlpha=.22;x.drawImage(bim,OX,OY,W,H);x.globalAlpha=1}", "x.globalAlpha=.22;cell(x,bim,f.i,OX,OY,W,H);x.globalAlpha=1}")
R("const body=cv('body'),bx=body.getContext('2d');bx.drawImage(bim,OX,OY,W,H);", "const body=cv('body'),bx=body.getContext('2d');cell(bx,bim,f.i,OX,OY,W,H);")
# vuist bovenop, na het Voor-stuk
R("vx.globalCompositeOperation='destination-in';vx.drawImage(mv,0,0);x.drawImage(vo,0,0);",
  "vx.globalCompositeOperation='destination-in';vx.drawImage(mv,0,0);x.drawImage(vo,0,0);\n    if(f.v&&A().sheet.v&&el('showvuist').checked){const vim=img(A().sheet.v);if(ready(vim))cell(x,vim,f.i,OX,OY,W,H)}")
# origineel tekenen in render
R("  compose(sctx,fr,f,mode==='mask'&&!playing);",
  """  compose(sctx,fr,f,mode==='mask'&&!playing);
  const oim=img(A().sheet.o);
  if(ready(oim)){if(origMode==='naast'){cell(sctx,oim,f.i,OX+W+MX,OY,W,H);sctx.save();sctx.font='600 22px sans-serif';sctx.fillStyle='rgba(255,255,255,.9)';sctx.fillText('origineel',OX+W+MX,OY-10);sctx.fillText('Mkuki',OX,OY-10);sctx.restore()}
    else if(origMode==='over'||(origMode==='knip'&&knipAan)){sctx.save();sctx.globalAlpha=origMode==='knip'?1:(+el('origop').value)/100;cell(sctx,oim,f.i,OX,OY,W,H);sctx.restore()}}""")
R("  sctx.save();sctx.strokeStyle='rgba(255,255,255,.55)';sctx.setLineDash([7,7]);sctx.lineWidth=2;sctx.strokeRect(OX,OY,W,H);",
  "  sctx.save();sctx.strokeStyle='rgba(255,255,255,.55)';sctx.setLineDash([7,7]);sctx.lineWidth=2;sctx.strokeRect(OX,OY,W,H);if(origMode==='naast')sctx.strokeRect(OX+W+MX,OY,W,H);")
# animatiekeuze
R("mkSeg(el('animseg'),D.anims,anim,id=>{stop();anim=id;cf=0;el('rfrom').value='';el('pfrom').value='';el('cfrom').value='';el('kfrom').value='';preload();schedule()});",
  """function kiesAnim(id){const was=playing;stop();anim=id;cf=0;el('rfrom').value='';el('pfrom').value='';el('cfrom').value='';el('kfrom').value='';dims();preload();schedule();if(was)el('play').click()}
function animLabels(){const s=el('animsel'),v=anim;s.innerHTML='';D.anims.forEach(a=>{const o=document.createElement('option');o.value=a.id;const n=a.frames.length,k=S.frames[a.id].filter(f=>f.ok).length;
  o.textContent=a.name+' ('+n+(n>1?' frames':' frame')+', '+a.fps+' fps)'+(k===n?'  ✓ klaar':k?'  '+k+'/'+n+' nagekeken':'');s.appendChild(o)});s.value=v}
el('animsel').onchange=e=>kiesAnim(e.target.value);
const animIdx=()=>D.anims.findIndex(a=>a.id===anim);
el('aprev').onclick=()=>{const i=animIdx();kiesAnim(D.anims[(i-1+D.anims.length)%D.anims.length].id);el('animsel').value=anim};
el('anext').onclick=()=>{const i=animIdx();kiesAnim(D.anims[(i+1)%D.anims.length].id);el('animsel').value=anim};
el('origseg').querySelectorAll('button').forEach(b=>b.onclick=()=>zetOrig(b.dataset.id));
function zetOrig(m){origMode=m;clearInterval(knipT);knipAan=false;if(m==='knip')knipT=setInterval(()=>{knipAan=!knipAan;schedule()},450);
  el('origseg').querySelectorAll('button').forEach(b=>b.classList.toggle('on',b.dataset.id===m));dims();schedule()}
el('origop').oninput=e=>{el('origopval').textContent=e.target.value+'%';schedule()};
el('showvuist').onchange=()=>schedule();
el('fok').onchange=e=>{const fr=FR();if(e.target.checked)fr.ok=true;else delete fr.ok;markFrame(anim,cf);animLabels();schedule()};
el('nextopen').onclick=()=>{const fs=S.frames[anim],N=fs.length;for(let d=1;d<=N;d++){const j=(cf+d)%N;if(!fs[j].ok){go(j);return}}toast('Alle frames van deze animatie zijn nagekeken')};""")
R("  onSeg(el('animseg'),anim);onSeg(el('verseg'),ver);", "  if(el('animsel').value!==anim)el('animsel').value=anim;onSeg(el('verseg'),ver);")
R("  el('fnum').textContent=(cf+1)+' / '+a.frames.length+'  bron '+f.orig;",
  """  el('fnum').textContent=(cf+1)+' / '+a.frames.length+'  '+f.orig+(a.twijfel.includes(cf+1)?'  ⚠ twijfel':'')+(fr.ok?'  ✓':'');
  el('fok').checked=!!fr.ok;{const k=S.frames[anim].filter(q=>q.ok).length;el('okinfo').textContent=k+' van '+a.frames.length+' nagekeken'}
  {const sn=(a.speerNoten||{})[cf+1];el('twijfel').innerHTML=(a.twijfel.length?'<b>Nakijken (TWIJFEL.md):</b> frame '+a.twijfel.join(', ')+'. '+a.twijfelTekst:'Geen twijfelgevallen genoteerd in TWIJFEL.md.')
    +'<br><b>Speer:</b> lengte '+a.speerL+' px in deze set'+(a.speerMaat!==a.speerL?' (dikte en punt van een speer van '+a.speerMaat+' px; het verschil zit in de schacht)':'')+(sn?'. Dit frame: '+sn+'.':'.')}""")
import re
_m=re.search(r"  el\('animnote'\)\.textContent=a\.zacht\?[^\n]*", J); assert _m
J=J.replace(_m.group(0), "  el('animnote').textContent=a.fps+' fps, canvas '+a.canvasW+'×'+a.canvasH+(a.vuist?'':', geen vuistlaag in deze set')+'.';")
# toets O
R("else if((e.key==='h'||e.key==='H')&&mode==='plaats'){cycleAngle(e.shiftKey?-1:1);e.preventDefault()}});",
  "else if((e.key==='h'||e.key==='H')&&mode==='plaats'){cycleAngle(e.shiftKey?-1:1);e.preventDefault()}else if(e.key==='o'||e.key==='O'){zetOrig(origMode==='uit'?'naast':origMode==='naast'?'over':'uit');e.preventDefault()}});")
# export met maat per animatie en bronpaden
R("el('export').onclick=()=>{const out={personage:D.personage,canvasW:CW,canvasH:CH,grond:GROND,anchorX:ANCHOR,frames:S.frames,hoekmaskers:S.am};",
  "el('export').onclick=()=>{const out={personage:D.personage,anims:D.anims.map(a=>({id:a.id,fps:a.fps,canvasW:a.canvasW,canvasH:a.canvasH,grond:a.grond,anchorX:a.anchorX,bron:a.frames.map(f=>D.bron[a.id+'-'+f.i])})),frames:S.frames,hoekmaskers:S.am};")
R("const wrap=el('stagewrap');let zoom=1,panMode=false;","const wrap=el('stagewrap');let zoom=1,panMode=false;window.__zoomKlaar=true;")
R("boot();\n</script>", "animLabels();\nboot().then(animLabels);\n</script>")
open(uit, 'w').write(J)
print('ok', len(J))

# Pathfinder: ander plaatje voor de speer en het vaantje eraan (na het schrijven nog eens bewerken)
J = open(uit).read()
def R2(old, new):
    global J
    assert J.count(old) == 1, old
    J = J.replace(old, new)
R2("function itemImg(id,angle){const it=IT[id];", "function itemImg(id,angle){const it=IT[id];if(id==='amirspeer'&&D.pf&&pfAan()&&D.pf.img[angle])return {e:D.pf.img[angle],fb:false};")
R2("function preload(){const s=A().sheet;", "function pfAan(){const c=document.getElementById('pfspeer');return !!(c&&c.checked)}\nfunction preload(){const s=A().sheet;if(D.pf){Object.values(D.pf.img).forEach(e=>img(e.src));img(D.pf.vaan.src)}")
R2("const full=cv(id+'_full'),fx=full.getContext('2d');fx.save();fx.globalAlpha=L.op;setup(fx);fx.drawImage(im,-g.w/2,-g.h/2,g.w,g.h);fx.restore();",
   """const full=cv(id+'_full'),fx=full.getContext('2d');fx.save();fx.globalAlpha=L.op;setup(fx);fx.drawImage(im,-g.w/2,-g.h/2,g.w,g.h);fx.restore();
  if(g.e.kx!=null){const V=D.pf.vaan,vi=img(V.src);if(ready(vi)){   // het vaantje hangt recht naar beneden, los van de hoek van de speer
    let lx=-g.w/2+g.e.kx*g.w,ly=-g.h/2+g.e.ky*g.h;if(L.flip)lx=-lx;const a=L.rot*Math.PI/180;
    const px=g.px+lx*Math.cos(a)-ly*Math.sin(a),py=g.py+lx*Math.sin(a)+ly*Math.cos(a),fk=g.w/g.e.wpx/V.k;
    fx.save();fx.globalAlpha=L.op;fx.drawImage(vi,px-V.kn[0]*fk,py-V.kn[1]*fk,vi.naturalWidth*fk,vi.naturalHeight*fk);fx.restore()}}""")
R2("el('showvuist').onchange=()=>schedule();", "el('showvuist').onchange=()=>schedule();\ntry{el('pfspeer').checked=localStorage.getItem('mkuki-pf')==='1'}catch(_){}\nel('pfspeer').onchange=e=>{try{localStorage.setItem('mkuki-pf',e.target.checked?'1':'0')}catch(_){}preload();schedule()};")
open(uit, 'w').write(J)
print('pf ok')
