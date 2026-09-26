/*
 * RavijnEffect - openscheurende grond voor Amir - King of Africa
 *
 * Zelfstandige module, geen dependencies, tekent op een gewone 2D canvas context.
 * Alle timings staan in seconden, dus framerate-onafhankelijk.
 *
 * Gebruik:
 *   const fx = new RavijnEffect({ wallImage, stoneImages, x, groundY, width });
 *   fx.start();
 *   // per frame:
 *   fx.update(dt);
 *   ctx.save(); ctx.translate(fx.shakeX, fx.shakeY);
 *     ...teken je wereld...
 *     fx.drawGap(ctx);        // direct na de grond
 *     ...teken je personages...
 *     fx.drawOverlay(ctx);    // stof, barst, steentjes, gruis
 *   ctx.restore();
 *   // collider:
 *   if (fx.colliderActive) { gatVan = fx.gapLeft; gatTot = fx.gapRight; }
 */
(function (root) {
  'use strict';

  // ---------------------------------------------------------------- fasen
  var PHASES = {
    tremor: 0.50,
    crack:  0.93,
    hush:   0.16,   // de stilte voor de klap, niet weglaten
    open:   1.20,
    settle: 1.07
  };

  var CFG = {
    edgeBand:        60,    // px van de wand die zijn vorm houdt aan elke kant
    lipSampleFrom:   80,    // strook zonder graspollen, voor de middenvulling bovenaan
    lipSampleTo:    116,
    lipRows:         40,
    depthNear:       0.10,  // blijvende verdonkering onderin
    depthFar:        0.58,  // extra verdonkering zolang het gat nog dichtgaat
    contactShadow:   20,
    crackDepth:      0.62,  // hoe diep de barst de wand in zakt, deel van de wandhoogte
    shakeTremorFrom: 1.1,
    shakeTremorTo:   2.0,
    shakeCrack:      1.6,
    shakeCrackSnap:  4.8,
    shakeOpen:       10.5,
    shakeSettle:     2.4,
    maxParticles:    220
  };

  var DUST = {
    deep: { rgb: [168, 122, 80], alpha: 0.26, flat: 0.85, grow: 120, burst: 20, rate: 9 },
    low:  { rgb: [214, 184, 140], alpha: 0.30, flat: 0.42, grow: 156, burst: 26, rate: 12 },
    high: { rgb: [216, 186, 142], alpha: 0.33, flat: 0.82, grow: 114, burst: 34, rate: 15 }
  };

  var SAND_COLORS = ['#D6A062', '#C18850', '#AC7442'];
  var CRACK_DARK  = 'rgba(112,66,31,0.96)';
  var CRACK_LIGHT = 'rgba(231,172,118,0.45)';
  var CHUNK_FILL  = '#B07646';
  var CHUNK_LINE  = '#6C4426';

  // ------------------------------------------------------- wolk-sprites
  // Zes bobbelige wolkjes, elk uit zeven overlappende radiale verlopen.
  // Eenmalig bij het laden gerenderd, per kleur. Daarna alleen nog drawImage.
  var SPRITE_SIZE = 96;
  var spriteCache = null;

  function buildSprite(seed, rgb) {
    var c = document.createElement('canvas');
    c.width = c.height = SPRITE_SIZE;
    var g = c.getContext('2d');
    var rnd = mulberry32(seed);
    for (var i = 0; i < 7; i++) {
      var cx = SPRITE_SIZE / 2 + (rnd() - 0.5) * SPRITE_SIZE * 0.38;
      var cy = SPRITE_SIZE / 2 + (rnd() - 0.5) * SPRITE_SIZE * 0.34;
      var r  = SPRITE_SIZE * (0.17 + rnd() * 0.16);
      var grad = g.createRadialGradient(cx, cy, 0, cx, cy, r);
      grad.addColorStop(0.00, 'rgba(' + rgb[0] + ',' + rgb[1] + ',' + rgb[2] + ',0.85)');
      grad.addColorStop(0.50, 'rgba(' + rgb[0] + ',' + rgb[1] + ',' + rgb[2] + ',0.45)');
      grad.addColorStop(1.00, 'rgba(' + rgb[0] + ',' + rgb[1] + ',' + rgb[2] + ',0)');
      g.fillStyle = grad;
      g.beginPath();
      g.arc(cx, cy, r, 0, Math.PI * 2);
      g.fill();
    }
    return c;
  }

  function sprites() {
    if (spriteCache) return spriteCache;
    spriteCache = {};
    ['deep', 'low', 'high'].forEach(function (k) {
      spriteCache[k] = [];
      for (var s = 0; s < 6; s++) spriteCache[k].push(buildSprite(1000 + s * 77, DUST[k].rgb));
    });
    return spriteCache;
  }

  function mulberry32(a) {
    return function () {
      a |= 0; a = (a + 0x6D2B79F5) | 0;
      var t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  function rr(a, b) { return a + Math.random() * (b - a); }

  // ------------------------------------------------------------- effect
  function RavijnEffect(opts) {
    this.wall   = opts.wallImage;               // Image met alpha, rij 0 = grondlijn
    this.stones = opts.stoneImages || [];
    this.x      = opts.x;                       // midden van het toekomstige gat
    this.groundY = opts.groundY;                // y van de grondlijn
    this.width  = opts.width || (this.wall ? this.wall.width : 277);
    this.quality = opts.quality != null ? opts.quality : 1;
    this.onEvent = opts.onEvent || function () {};
    this.stoneSpots = opts.stoneSpots || [];    // [{x, y}] in wereldcoordinaten

    this.half = this.width / 2;
    this.scaleFactor = this.width / (this.wall ? this.wall.width : 277);

    // langere barst en opening bij een breder ravijn
    this.tCrack = PHASES.crack * (0.72 + 0.28 * this.scaleFactor);
    this.tOpen  = PHASES.open  * (0.68 + 0.32 * this.scaleFactor);

    this.buf = document.createElement('canvas');
    this.buf.width = Math.ceil(this.width) + 4;
    this.buf.height = this.wall ? this.wall.height : 189;
    this.bufCtx = this.buf.getContext('2d');

    this._buildCrack();
    this._resetParticles();
    this.reset();
  }

  RavijnEffect.prototype.reset = function () {
    this.t = 0;
    this.phase = 'idle';
    this.p = 0;          // openingsgraad 0..1
    this.g = 0;          // barstvoortgang 0..1
    this.shakeX = 0;
    this.shakeY = 0;
    this.running = false;
    this.colliderActive = false;
    this._snapped = false;
    this._crackStepDone = 0;
    this._resetParticles();
    this._resetStones();
  };

  RavijnEffect.prototype.start = function () {
    this.reset();
    this.running = true;
    this.phase = 'tremor';
    this.onEvent('onTremorStart');
  };

  RavijnEffect.prototype.openInstantly = function () {
    this.reset();
    this.p = 1; this.g = 1;
    this.phase = 'done';
    this.colliderActive = true;
  };

  RavijnEffect.prototype._resetParticles = function () {
    this.deep = []; this.low = []; this.high = [];
    this.sand = []; this.chunks = [];
  };

  RavijnEffect.prototype._resetStones = function () {
    var self = this;
    this.stonesOnGround = this.stoneSpots.map(function (s, i) {
      return { x: s.x, y: s.y, base: s.y, vx: 0, vy: 0, rot: 0, vr: 0,
               img: self.stones[i % Math.max(1, self.stones.length)], falling: false };
    });
  };

  // ------------------------------------------------------------- update
  RavijnEffect.prototype.update = function (dt) {
    if (dt > 0.05) dt = 0.05;                   // na een hapering niet doorschieten
    if (this.running) {
      this.t += dt;
      this._advancePhase();
    }
    this._spawn(dt);
    this._moveParticles(dt);
    this._moveStones(dt);
    this._shake();
  };

  RavijnEffect.prototype._advancePhase = function () {
    var t = this.t;
    if (this.phase === 'tremor') {
      if (t >= PHASES.tremor) { this.phase = 'crack'; this.t = 0; }
    } else if (this.phase === 'crack') {
      var u = Math.min(1, t / this.tCrack);
      this.g = u < 0.70 ? 0.34 * Math.pow(u / 0.70, 1.7)
                        : 0.34 + 0.66 * Math.pow((u - 0.70) / 0.30, 0.55);
      var step = Math.floor(this.g * 9);
      if (step > this._crackStepDone) { this._crackStepDone = step; this.onEvent('onCrackStep'); }
      if (!this._snapped && this.g >= 0.34) { this._snapped = true; this.onEvent('onCrackSnap'); }
      if (u >= 1) { this.g = 1; this.phase = 'hush'; this.t = 0; this.onEvent('onSilence'); }
    } else if (this.phase === 'hush') {
      if (t >= PHASES.hush) {
        this.phase = 'open'; this.t = 0;
        this.onEvent('onBreak');
        this._burst();
      }
    } else if (this.phase === 'open') {
      var v = Math.min(1, t / this.tOpen);
      var smooth = v * v * (3 - 2 * v);
      this.p = 0.015 + 0.985 * Math.pow(smooth, 1.25);
      if (v >= 1) {
        this.p = 1; this.phase = 'settle'; this.t = 0;
        this.colliderActive = true;
        this.onEvent('onSettle');
      }
    } else if (this.phase === 'settle') {
      if (t >= PHASES.settle) { this.phase = 'done'; this.running = false; }
    }
  };

  RavijnEffect.prototype._shake = function () {
    var a = 0;
    if (this.phase === 'tremor') {
      a = CFG.shakeTremorFrom +
          (CFG.shakeTremorTo - CFG.shakeTremorFrom) * (this.t / PHASES.tremor);
    } else if (this.phase === 'crack') {
      a = CFG.shakeCrack + CFG.shakeCrackSnap * Math.max(0, this.g - 0.34);
    } else if (this.phase === 'hush') {
      a = 0;                                   // volledig stil, dat is het punt
    } else if (this.phase === 'open') {
      // hardst op het moment dat het gat het snelst groeit
      var v = Math.min(1, this.t / this.tOpen);
      var speed = 6 * v * (1 - v);
      a = CFG.shakeOpen * Math.pow(speed, 0.75);
    } else if (this.phase === 'settle') {
      var s = 1 - this.t / PHASES.settle;
      a = CFG.shakeSettle * s * s;
    }
    this.shakeX = a ? (Math.random() * 2 - 1) * a : 0;
    this.shakeY = a ? (Math.random() * 2 - 1) * a * 0.7 : 0;
  };

  Object.defineProperty(RavijnEffect.prototype, 'gapLeft', {
    get: function () { return this.x - this.half * this.p; }
  });
  Object.defineProperty(RavijnEffect.prototype, 'gapRight', {
    get: function () { return this.x + this.half * this.p; }
  });

  // -------------------------------------------------------------- barst
  // De barst splijt naar BENEDEN, dwars door de zandband en de rotslaag eronder.
  // Coordinaten zijn relatief aan (this.x, this.groundY), dy positief is omlaag.
  RavijnEffect.prototype._buildCrack = function () {
    var rnd = mulberry32(5);
    var h = this.buf.height;
    this.crackDepth = Math.round(h * CFG.crackDepth);

    function down(x0, y0, depth, wobble, stepLen) {
      var pts = [[x0, y0]], x = x0, y = y0, vx = 0;
      while (y < y0 + depth) {
        y += stepLen + (rnd() - 0.5) * stepLen * 0.6;
        vx = vx * 0.45 + (rnd() - 0.5) * wobble;
        x += vx;
        pts.push([x, y]);
      }
      return pts;
    }

    this.crackMain = down(0, 0, this.crackDepth, 7.5, 6);
    this.crackForks = [];
    var n = 3 + Math.round(2 * this.scaleFactor);
    for (var i = 0; i < n; i++) {
      var k = 2 + Math.floor(rnd() * (this.crackMain.length - 4));
      var bx = this.crackMain[k][0], by = this.crackMain[k][1];
      var dir = rnd() < 0.5 ? -1 : 1;
      var pts = [[bx, by]], x = bx, y = by;
      var segs = 2 + Math.floor(rnd() * 3);
      for (var j = 0; j < segs; j++) {
        x += dir * (4 + rnd() * 8);
        y += 4 + rnd() * 9;
        pts.push([x, y]);
      }
      this.crackForks.push({ depth: by, pts: pts });
    }
  };

  // ----------------------------------------------------------- deeltjes
  RavijnEffect.prototype._count = function () {
    return this.deep.length + this.low.length + this.high.length;
  };

  RavijnEffect.prototype._burst = function () {
    var q = this.quality;
    this._emit('high', Math.round(DUST.high.burst * q));
    this._emit('low',  Math.round(DUST.low.burst  * q));
    this._emit('deep', Math.round(DUST.deep.burst * q));
    var n = Math.round(7 * this.scaleFactor * q);
    for (var i = 0; i < n; i++) {
      var left = Math.random() < 0.5;
      this.chunks.push({
        x: (left ? this.gapLeft : this.gapRight) + rr(-4, 4),
        y: this.groundY + rr(4, 18),
        vx: rr(10, 48) * (left ? 1 : -1), vy: rr(-22, 22),
        r: rr(2.4, 5.2), rot: rr(0, 6.2), vr: rr(-4.2, 4.2)
      });
    }
  };

  RavijnEffect.prototype._emit = function (kind, n) {
    if (this._count() > CFG.maxParticles) return;
    var lp = this.gapLeft, rp = this.gapRight;
    for (var i = 0; i < n; i++) {
      if (kind === 'high') {
        var sx = Math.random() < 0.45 ? rr(lp, rp) : (Math.random() < 0.5 ? lp : rp);
        this.high.push({ x: sx + rr(-22, 22), y: this.groundY + rr(-6, 22),
          vx: rr(-25, 25), vy: rr(-70, -14), r: rr(3, 30), life: 1,
          decay: rr(0.56, 1.19), a: rr(0.45, 1.15), s: (i * 7) % 6 });
      } else if (kind === 'low') {
        var left = Math.random() < 0.5, d = left ? -1 : 1;
        this.low.push({ x: (left ? lp : rp) + d * rr(0, 16), y: this.groundY + rr(0, 22),
          vx: d * rr(56, 175), vy: rr(-11, 5), r: rr(4, 26), life: 1,
          decay: rr(0.77, 1.40), a: rr(0.45, 1.1), s: (i * 5) % 6 });
      } else {
        var yy = this.groundY + rr(22, this.buf.height - 6);
        var e = this._edgesAt(yy);
        if (e[1] - e[0] < 4) continue;
        var x0, vx;
        if (Math.random() < 0.7) {
          var lf = Math.random() < 0.5;
          x0 = lf ? e[0] + rr(0, 10) : e[1] - rr(0, 10);
          vx = (lf ? 1 : -1) * rr(6, 24);
        } else { x0 = rr(e[0], e[1]); vx = rr(-14, 14); }
        this.deep.push({ x: x0, y: yy, vx: vx, vy: -rr(13, 39), r: rr(4, 24), life: 1,
          decay: rr(0.50, 0.98), a: rr(0.5, 1.1), s: (i * 3) % 6 });
      }
    }
  };

  RavijnEffect.prototype._edgesAt = function () { return [this.gapLeft, this.gapRight]; };

  // wereldpositie van de punt van de barst
  RavijnEffect.prototype._crackTip = function () {
    var reach = this.g * this.crackDepth, pt = this.crackMain[0];
    for (var i = 0; i < this.crackMain.length; i++) {
      if (this.crackMain[i][1] <= reach) pt = this.crackMain[i]; else break;
    }
    return [this.x + pt[0], this.groundY + pt[1]];
  };

  RavijnEffect.prototype._spawn = function (dt) {
    var q = this.quality, f = dt * 14;           // referentie was 14 fps
    if (this.phase === 'crack') {
      this._emit('high', Math.round((this.g < 0.34 ? 2 : 5) * q * f * 0.5));
      var tip = this._crackTip();
      var nt = Math.round((this.g < 0.34 ? 1 : 3) * q * f);
      for (var t = 0; t < nt; t++) {
        this.deep.push({ x: tip[0] + rr(-5, 5), y: tip[1] + rr(-4, 6),
          vx: rr(-12, 12), vy: -rr(6, 22), r: rr(3, 10), life: 1,
          decay: rr(0.8, 1.5), a: rr(0.4, 0.9), s: (t * 3) % 6 });
      }
    } else if (this.phase === 'open' || this.phase === 'settle') {
      var fade = this.phase === 'settle' ? Math.max(0, 1 - this.t / (PHASES.settle * 0.6)) : 1;
      if (fade > 0) {
        this._emit('high', Math.round(DUST.high.rate * q * f * fade));
        this._emit('low',  Math.round(DUST.low.rate  * q * f * fade));
        this._emit('deep', Math.round(DUST.deep.rate * q * f * fade));
      }
      // zandstraaltjes over de rand
      var strength = this.phase === 'settle'
        ? Math.max(0, 1 - this.t / (PHASES.settle * 0.8)) : 1;
      if (this.p > 0.10) {
        var offs = [[-1, 3], [-1, 11], [1, 2.5], [1, 12]];
        for (var i = 0; i < offs.length; i++) {
          if (Math.random() > strength) continue;
          var ex = offs[i][0] < 0 ? this.gapLeft + offs[i][1] : this.gapRight - offs[i][1];
          var k = Math.max(1, Math.round(2 * f));
          for (var j = 0; j < k; j++) {
            var y0 = this.groundY + rr(3, 8);
            this.sand.push({ x: ex + rr(-1.6, 1.6), y: y0, y0: y0,
              vx: -offs[i][0] * rr(0.7, 6.3), vy: rr(7, 25),
              span: rr(38, 95), col: SAND_COLORS[(Math.random() * 3) | 0] });
          }
        }
      }
    }
  };

  RavijnEffect.prototype._moveParticles = function (dt) {
    function step(arr, growPerSec, spin) {
      for (var i = arr.length - 1; i >= 0; i--) {
        var q = arr[i];
        q.x += q.vx * dt; q.y += q.vy * dt;
        q.vx *= spin.dragX; q.vy *= spin.dragY;
        q.r += growPerSec * dt;
        q.life -= q.decay * dt;
        if (q.life <= 0) arr.splice(i, 1);
      }
    }
    step(this.deep, DUST.deep.grow, { dragX: 1 + 0.3 * dt, dragY: 1 - 0.42 * dt });
    step(this.low,  DUST.low.grow,  { dragX: 1 - 1.12 * dt, dragY: 1 });
    step(this.high, DUST.high.grow, { dragX: 1 + 0.42 * dt, dragY: 1 - 0.21 * dt });
    for (var i = this.deep.length - 1; i >= 0; i--) {
      if (this.deep[i].y < this.groundY - 40) this.deep.splice(i, 1);
    }
    for (var s = this.sand.length - 1; s >= 0; s--) {
      var p = this.sand[s];
      p.x += p.vx * dt; p.y += p.vy * dt; p.vy += 110 * dt;
      if (p.y - p.y0 > p.span) this.sand.splice(s, 1);
    }
    for (var c = this.chunks.length - 1; c >= 0; c--) {
      var k = this.chunks[c];
      k.x += k.vx * dt; k.y += k.vy * dt; k.vy += 300 * dt; k.rot += k.vr * dt;
      if (k.y > this.groundY + this.buf.height + 30) this.chunks.splice(c, 1);
    }
  };

  RavijnEffect.prototype._moveStones = function (dt) {
    var lp = this.gapLeft, rp = this.gapRight;
    var shake = Math.abs(this.shakeX) + Math.abs(this.shakeY);
    for (var i = 0; i < this.stonesOnGround.length; i++) {
      var s = this.stonesOnGround[i];
      if (!s.falling && this.p > 0.02 && s.x > lp - 2 && s.x < rp + 2) {
        s.falling = true; s.vy = -17; s.vx = rr(-15, 15); s.vr = rr(-3.5, 3.5);
      }
      if (s.falling) {
        s.x += s.vx * dt; s.y += s.vy * dt; s.vy += 260 * dt; s.rot += s.vr * dt;
      } else if (shake > 0.6) {
        if (s.y >= s.base - 0.1 && Math.random() < 0.45 * dt * 14) {
          s.vy = -rr(9, 8 + shake * 8);
        }
        s.y += s.vy * dt; s.vy += 175 * dt;
        if (s.y > s.base) { s.y = s.base; s.vy = 0; }
      }
    }
  };

  // -------------------------------------------------------------- gat
  // Teken dit direct nadat je je grond hebt getekend. Het gat dekt de grond af.
  RavijnEffect.prototype.drawGap = function (ctx) {
    if (this.p <= 0 || !this.wall) return;
    var w = this.wall.width, h = this.wall.height;
    var lp = this.gapLeft, rp = this.gapRight;
    var gw = rp - lp;
    if (gw < 1) return;

    var g = this.bufCtx;
    g.clearRect(0, 0, this.buf.width, this.buf.height);
    var B = Math.min(CFG.edgeBand, gw / 2);

    g.drawImage(this.wall, 0, 0, B, h, 0, 0, B, h);              // linkerwand
    g.drawImage(this.wall, w - B, 0, B, h, gw - B, 0, B, h);     // rechterwand

    var midW = gw - 2 * B;
    if (midW > 0.5) {
      // bovenrand uit een stuk zonder graspollen, daaronder uit de brede wandstrook
      this._tile(g, CFG.lipSampleFrom, CFG.lipSampleTo, 0, CFG.lipRows, B, midW);
      this._tile(g, B, w - B, CFG.lipRows, h - CFG.lipRows, B, midW);
    }

    // diepte, alleen waar de wand staat
    var amt = CFG.depthNear + CFG.depthFar * (1 - this.p);
    var grad = g.createLinearGradient(0, 0, 0, h);
    grad.addColorStop(0, 'rgba(0,0,0,0)');
    grad.addColorStop(1, 'rgba(0,0,0,' + amt.toFixed(3) + ')');
    g.globalCompositeOperation = 'source-atop';
    g.fillStyle = grad;
    g.fillRect(0, 0, gw, h);
    g.globalCompositeOperation = 'source-over';

    ctx.drawImage(this.buf, 0, 0, Math.ceil(gw), h, Math.round(lp), this.groundY, Math.ceil(gw), h);

    if (this.p < 0.999) this._contactShadow(ctx, lp, rp);
  };

  RavijnEffect.prototype._tile = function (g, sx0, sx1, sy, sh, dx, dw) {
    var tw = sx1 - sx0;
    if (tw < 3) return;
    var drawn = 0, flip = false;
    while (drawn < dw) {
      var piece = Math.min(tw, dw - drawn);
      g.save();
      if (flip) {
        g.translate(dx + drawn + piece, 0);
        g.scale(-1, 1);
        g.drawImage(this.wall, sx0, sy, piece, sh, 0, sy, piece, sh);
      } else {
        g.drawImage(this.wall, sx0, sy, piece, sh, dx + drawn, sy, piece, sh);
      }
      g.restore();
      drawn += piece; flip = !flip;
    }
  };

  RavijnEffect.prototype._contactShadow = function (ctx, lp, rp) {
    var d = CFG.contactShadow, hgt = 90;
    var gl = ctx.createLinearGradient(lp - d, 0, lp, 0);
    gl.addColorStop(0, 'rgba(0,0,0,0)');
    gl.addColorStop(1, 'rgba(0,0,0,0.24)');
    ctx.fillStyle = gl; ctx.fillRect(lp - d, this.groundY, d, hgt);
    var gr = ctx.createLinearGradient(rp + d, 0, rp, 0);
    gr.addColorStop(0, 'rgba(0,0,0,0)');
    gr.addColorStop(1, 'rgba(0,0,0,0.24)');
    ctx.fillStyle = gr; ctx.fillRect(rp, this.groundY, d, hgt);
  };

  // ---------------------------------------------------------- overlay
  RavijnEffect.prototype.drawOverlay = function (ctx) {
    var sp = sprites();
    this._drawDust(ctx, this.deep, sp.deep, DUST.deep);
    this._drawDust(ctx, this.low,  sp.low,  DUST.low);
    this._drawDustHigh(ctx, sp.high, DUST.high);
    this._drawCrack(ctx);
    this._drawChunks(ctx);
    this._drawSand(ctx);
    this._drawStones(ctx);
  };

  RavijnEffect.prototype._drawDust = function (ctx, arr, sps, cfg) {
    for (var i = 0; i < arr.length; i++) {
      var q = arr[i];
      var a = cfg.alpha * q.a * Math.max(0, q.life);
      if (a <= 0.01) continue;
      ctx.globalAlpha = Math.min(1, a);
      var w = q.r * 2, h = w * cfg.flat;
      ctx.drawImage(sps[q.s], q.x - w / 2, q.y - h / 2, w, h);
    }
    ctx.globalAlpha = 1;
  };

  RavijnEffect.prototype._drawDustHigh = function (ctx, sps, cfg) {
    for (var i = 0; i < this.high.length; i++) {
      var q = this.high[i];
      var rise = Math.min(1, Math.max(0, (this.groundY - q.y) / 175));
      var a = cfg.alpha * q.a * Math.max(0, q.life) * (1 - 0.62 * rise);
      if (a <= 0.01) continue;
      ctx.globalAlpha = Math.min(1, a);
      var w = q.r * 2, h = w * cfg.flat;
      ctx.drawImage(sps[q.s], q.x - w / 2, q.y - h / 2, w, h);
    }
    ctx.globalAlpha = 1;
  };

  RavijnEffect.prototype._drawCrack = function (ctx) {
    if (this.g <= 0 || this.p >= 0.999) return;
    var reach = this.g * this.crackDepth;          // hoe diep hij al gezakt is
    var self = this;
    function draw(pts, scale, color, dx) {
      var run = [];
      for (var i = 0; i < pts.length; i++) {
        var wx = self.x + pts[i][0], wy = self.groundY + pts[i][1];
        var inGap = wx > self.gapLeft - 1 && wx < self.gapRight + 1;
        if (!inGap && pts[i][1] <= reach) {
          run.push([wx + dx, wy, pts[i][1]]);
        } else if (run.length) { stroke(run, scale, color); run = []; }
      }
      if (run.length) stroke(run, scale, color);
    }
    function stroke(run, scale, color) {
      if (run.length < 2) return;
      ctx.strokeStyle = color;
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';
      for (var i = 0; i < run.length - 1; i++) {
        var md = (run[i][2] + run[i + 1][2]) / 2;
        // breed aan de bovenkant, spits toelopend naar de punt
        var taper = Math.max(0.6, 3.4 * (1 - Math.pow(md / self.crackDepth, 1.15)));
        ctx.lineWidth = Math.max(0.6, taper * scale);
        ctx.beginPath();
        ctx.moveTo(run[i][0], run[i][1]);
        ctx.lineTo(run[i + 1][0], run[i + 1][1]);
        ctx.stroke();
      }
    }
    draw(this.crackMain, 0.70, CRACK_LIGHT, 1.7);   // hooglicht naast de scheur
    draw(this.crackMain, 1.00, CRACK_DARK, 0);
    for (var f = 0; f < this.crackForks.length; f++) {
      if (this.crackForks[f].depth <= reach) {
        draw(this.crackForks[f].pts, 0.40, CRACK_LIGHT, 1.3);
        draw(this.crackForks[f].pts, 0.58, CRACK_DARK, 0);
      }
    }
  };

  RavijnEffect.prototype._drawChunks = function (ctx) {
    ctx.lineWidth = 1;
    for (var i = 0; i < this.chunks.length; i++) {
      var c = this.chunks[i];
      ctx.beginPath();
      for (var k = 0; k < 6; k++) {
        var a = c.rot + k * 1.05;
        var px = c.x + c.r * Math.cos(a), py = c.y + c.r * 0.8 * Math.sin(a);
        if (k === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
      }
      ctx.closePath();
      ctx.fillStyle = CHUNK_FILL; ctx.fill();
      ctx.strokeStyle = CHUNK_LINE; ctx.stroke();
    }
  };

  RavijnEffect.prototype._drawSand = function (ctx) {
    ctx.lineWidth = 1;
    for (var i = 0; i < this.sand.length; i++) {
      var p = this.sand[i];
      var f = 1 - (p.y - p.y0) / p.span;
      if (f <= 0) continue;
      ctx.globalAlpha = 0.35 + 0.65 * f;
      ctx.strokeStyle = p.col;
      var len = Math.min(3.2, 1 + p.vy * 0.05);
      ctx.beginPath();
      ctx.moveTo(p.x, p.y);
      ctx.lineTo(p.x - p.vx * 0.006, p.y - len);
      ctx.stroke();
    }
    ctx.globalAlpha = 1;
  };

  RavijnEffect.prototype._drawStones = function (ctx) {
    for (var i = 0; i < this.stonesOnGround.length; i++) {
      var s = this.stonesOnGround[i];
      if (!s.img) continue;
      if (s.rot) {
        ctx.save();
        ctx.translate(s.x, s.y - s.img.height / 2);
        ctx.rotate(s.rot);
        ctx.drawImage(s.img, -s.img.width / 2, -s.img.height / 2);
        ctx.restore();
      } else {
        ctx.drawImage(s.img, Math.round(s.x - s.img.width / 2), Math.round(s.y - s.img.height));
      }
    }
  };

  root.RavijnEffect = RavijnEffect;
  root.RavijnEffect.PHASES = PHASES;
  root.RavijnEffect.CFG = CFG;
})(typeof window !== 'undefined' ? window : this);
