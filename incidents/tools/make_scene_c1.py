#!/usr/bin/env python3
"""事件1「夜の机」の背景を img/scene-c1.svg として生成する（標準ライブラリのみ・ネット不要）。
配置は cases.js のスポット位置（日誌 7〜39%／端末 46〜70%／手順書 74〜93%）に合わせてある。"""
import random, os
random.seed(11)
W, H = 1000, 440
o = []; a = o.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="none">')
a('''<defs>
<linearGradient id="wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0c1015"/><stop offset="1" stop-color="#1b222b"/></linearGradient>
<radialGradient id="pool" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#ffd890" stop-opacity=".62"/><stop offset=".55" stop-color="#ffc766" stop-opacity=".2"/><stop offset="1" stop-color="#ffc766" stop-opacity="0"/></radialGradient>
<linearGradient id="cone" x1=".4" y1="0" x2=".5" y2="1"><stop offset="0" stop-color="#fff0c0" stop-opacity=".34"/><stop offset="1" stop-color="#ffd890" stop-opacity="0"/></linearGradient>
<linearGradient id="deskShade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity=".6"/><stop offset=".5" stop-color="#000" stop-opacity="0"/></linearGradient>
<linearGradient id="falloff" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset=".45" stop-color="#000" stop-opacity=".12"/><stop offset="1" stop-color="#000" stop-opacity=".62"/></linearGradient>
<radialGradient id="vig" cx=".42" cy=".55" r=".78"><stop offset=".5" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".72"/></radialGradient>
<linearGradient id="pageL" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#eae1c6"/><stop offset=".8" stop-color="#e2d8bb"/><stop offset="1" stop-color="#b5a886"/></linearGradient>
<linearGradient id="pageR" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#b5a886"/><stop offset=".2" stop-color="#e2d8bb"/><stop offset="1" stop-color="#eae1c6"/></linearGradient>
<linearGradient id="binder" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3c6199"/><stop offset="1" stop-color="#223e68"/></linearGradient>
<linearGradient id="screen" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b1d16"/><stop offset="1" stop-color="#06100c"/></linearGradient>
<filter id="b2"><feGaussianBlur stdDeviation="2"/></filter><filter id="b5"><feGaussianBlur stdDeviation="5"/></filter><filter id="b12"><feGaussianBlur stdDeviation="12"/></filter><filter id="b22"><feGaussianBlur stdDeviation="22"/></filter>
<filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.004 0.14" numOctaves="3" seed="7"/><feColorMatrix type="saturate" values="0"/></filter>
<filter id="noise" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="3"/><feColorMatrix type="saturate" values="0"/></filter>
</defs>''')
# --- 壁と窓（夜景） ---
a(f'<rect width="{W}" height="{H}" fill="url(#wall)"/>')
a('<rect x="650" y="26" width="290" height="152" fill="#0a1522"/>')
for _ in range(16):
    x = random.randint(655, 925); h = random.randint(24, 70); w = random.randint(14, 34)
    a(f'<rect x="{x}" y="{178-h}" width="{w}" height="{h}" fill="#07101a"/>')
for _ in range(46):
    cx = random.uniform(656, 934); cy = random.uniform(96, 172); c = random.choice(["#ffd27a", "#ffd27a", "#9fd0ff", "#ffb36b"])
    a(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{random.uniform(.7, 2.2):.1f}" fill="{c}" opacity="{random.uniform(.5, .95):.2f}"/>')
for _ in range(7):
    a(f'<circle cx="{random.uniform(670, 920):.0f}" cy="{random.uniform(110, 168):.0f}" r="{random.uniform(5, 10):.0f}" fill="#ffcf85" opacity=".28" filter="url(#b5)"/>')
for y in range(30, 176, 13): a(f'<rect x="650" y="{y}" width="290" height="5" fill="#131b25" opacity=".92"/><rect x="650" y="{y+5}" width="290" height="1" fill="#2b3644" opacity=".6"/>')
a('<rect x="650" y="26" width="290" height="152" fill="none" stroke="#232b35" stroke-width="7"/><line x1="795" y1="26" x2="795" y2="178" stroke="#232b35" stroke-width="5"/>')
a('<ellipse cx="250" cy="120" rx="330" ry="150" fill="url(#pool)" opacity=".5" style="mix-blend-mode:screen"/>')
# --- 机 ---
a('<rect y="205" width="1000" height="195" fill="#5a4330"/><rect y="205" width="1000" height="195" filter="url(#grain)" opacity=".34" style="mix-blend-mode:multiply"/>')
a('<rect y="205" width="1000" height="195" fill="url(#deskShade)"/><rect y="204" width="1000" height="3" fill="#0b0d10" opacity=".8"/>')
a('<ellipse cx="300" cy="305" rx="360" ry="125" fill="url(#pool)" style="mix-blend-mode:screen"/>')
a('<rect y="398" width="1000" height="11" fill="#6b523b"/><rect y="398" width="1000" height="2" fill="#8a6d4f" opacity=".8"/><rect y="409" width="1000" height="31" fill="#06080a"/>')
a('<path d="M350 440 Q372 404 500 401 Q628 404 650 440 Z" fill="#10151b"/><path d="M350 440 Q372 404 500 401 Q628 404 650 440" fill="none" stroke="#2a323c" stroke-width="2"/>')
# --- スタンドライト（奥） ---
a('<ellipse cx="118" cy="236" rx="46" ry="7" fill="#15181c"/><ellipse cx="118" cy="233" rx="40" ry="5" fill="#2a2e33"/>')
a('<path d="M118 232 L150 126" stroke="#1d2024" stroke-width="9" stroke-linecap="round"/><path d="M150 126 L248 78" stroke="#1d2024" stroke-width="7" stroke-linecap="round"/>')
a('<path d="M118 232 L150 126" stroke="#3a4048" stroke-width="2" stroke-linecap="round" transform="translate(-2,0)"/><circle cx="150" cy="126" r="7" fill="#2a2e33" stroke="#3c424a"/>')
a('<path d="M214 70 L276 84 L292 118 L226 112 Z" fill="#262a30"/><path d="M214 70 L276 84 L282 94 L218 80 Z" fill="#454c56"/><ellipse cx="258" cy="112" rx="30" ry="7" fill="#fff3c8" opacity=".95"/><ellipse cx="258" cy="116" rx="46" ry="14" fill="#ffe2a0" opacity=".5" filter="url(#b5)"/>')
a('<path d="M232 116 L284 118 L520 392 L110 372 Z" fill="url(#cone)" style="mix-blend-mode:screen"/>')
# --- マグカップ ---
a('<ellipse cx="432" cy="340" rx="26" ry="6" fill="#000" opacity=".5" filter="url(#b2)"/><path d="M414 304 L414 334 Q432 344 450 334 L450 304 Z" fill="#c9c2b2"/><path d="M414 304 L414 334 Q420 338 424 339 L424 304 Z" fill="#e4dece" opacity=".7"/><ellipse cx="432" cy="304" rx="18" ry="5" fill="#2a1b12"/><path d="M450 312 q14 2 12 14 q-2 8 -12 8" fill="none" stroke="#c9c2b2" stroke-width="5"/>')
a('<path d="M426 296 q-6 -14 2 -26 q6 -10 0 -22" fill="none" stroke="#fff" stroke-width="3" opacity=".16" filter="url(#b2)"/>')
# --- 端末（アクセスログ） ---
a('<rect x="468" y="150" width="226" height="160" fill="#6fe0b0" opacity=".12" filter="url(#b22)"/><ellipse cx="582" cy="338" rx="170" ry="30" fill="#5fd3a0" opacity=".10" filter="url(#b12)"/>')
a('<ellipse cx="586" cy="326" rx="64" ry="9" fill="#000" opacity=".55" filter="url(#b2)"/><path d="M550 332 L550 314 L624 314 L624 332" fill="none"/>')
a('<rect x="572" y="292" width="28" height="22" fill="#15181c"/><ellipse cx="586" cy="316" rx="48" ry="6" fill="#14171b"/><ellipse cx="586" cy="314" rx="46" ry="4.5" fill="#23282e"/>')
a('<rect x="474" y="164" width="224" height="132" rx="6" fill="#0c0f12" stroke="#2c3238" stroke-width="3"/><rect x="484" y="174" width="204" height="108" fill="url(#screen)"/>')
ys = 182
for i in range(12):
    n = random.randint(2, 4); x = 491
    for _ in range(n):
        w = random.randint(14, 56)
        if x + w > 678: break
        c = "#7fe0b4" if random.random() > .12 else "#e8d66a"
        a(f'<rect x="{x}" y="{ys}" width="{w}" height="3" fill="{c}" opacity="{random.uniform(.55, .9):.2f}"/>'); x += w + random.randint(5, 9)
    ys += 8.2
a('<rect x="491" y="270" width="6" height="7" fill="#7fe0b4" opacity=".9"/><path d="M484 174 L560 174 L520 282 L484 282 Z" fill="#fff" opacity=".035"/>')
a('<circle cx="686" cy="289" r="2" fill="#6fe0b0"/>')
a('<path d="M508 330 L672 330 L688 349 L492 349 Z" fill="#12161a" stroke="#2a3036"/>')
for r in range(3):
    y = 333 + r * 5.2; x0 = 512 - r * 3.5; k = 16
    for i in range(k): a(f'<rect x="{x0 + i * 10.3:.1f}" y="{y:.1f}" width="8.2" height="3.6" rx="0.8" fill="#272d34"/>')
a('<g transform="rotate(7 668 184)"><rect x="656" y="171" width="27" height="27" fill="#000" opacity=".35" filter="url(#b2)" transform="translate(2,3)"/><rect x="656" y="171" width="27" height="27" fill="#f3da52"/><path d="M660 179 h18 M660 184 h14 M660 189 h17" stroke="#6b5a14" stroke-width="1.3" opacity=".75"/></g>')
# --- 運用手順書（バインダー） ---
a('<ellipse cx="836" cy="370" rx="96" ry="9" fill="#000" opacity=".55" filter="url(#b5)"/>')
a('<rect x="760" y="190" width="152" height="178" fill="#cfc9b8"/><rect x="756" y="186" width="152" height="180" rx="3" fill="url(#binder)"/><rect x="746" y="184" width="14" height="184" fill="#1a3152"/><rect x="746" y="184" width="3" height="184" fill="#46618a" opacity=".6"/>')
a('<rect x="772" y="202" width="112" height="50" fill="#e9e6dc"/><text x="780" y="226" font-family="Yu Gothic UI,Hiragino Sans,Noto Sans CJK JP,sans-serif" font-size="18" font-weight="700" fill="#1d2430">運用手順書</text><path d="M780 238 h70" stroke="#7a7869" stroke-width="2"/>')
for i, c in enumerate(["#e0b030", "#e5534b", "#58b894", "#6a9ad6"]): a(f'<rect x="905" y="{222 + i * 26}" width="10" height="20" fill="{c}"/>')
a('<path d="M756 186 L908 186 L908 200 L756 220 Z" fill="#fff" opacity=".05"/>')
# --- 業務日誌（開いたノート） ---
a('<ellipse cx="232" cy="384" rx="190" ry="12" fill="#000" opacity=".6" filter="url(#b5)"/>')
a('<path d="M64 232 L228 222 L394 232 L398 376 L228 386 L60 376 Z" fill="#5a3d28"/>')
a('<path d="M72 378 L228 388 L388 378 L388 372 L228 382 L72 372 Z" fill="#cfc4a6"/>')
a('<path d="M74 232 L228 224 L228 380 L72 374 Z" fill="url(#pageL)"/><path d="M228 224 L384 232 L386 374 L228 380 Z" fill="url(#pageR)"/>')
a('<path d="M228 224 L228 380" stroke="#8d805e" stroke-width="2" opacity=".8"/>')
def edge(x0, x1, side):
    top = lambda x: (232 - 8 * (x - 74) / 154) if side == 0 else (224 + 8 * (x - 228) / 156)
    bot = lambda x: (374 + 6 * (x - 74) / 154) if side == 0 else (380 - 6 * (x - 228) / 158)
    return top, bot
for side, (xa, xb) in enumerate(((84, 220), (238, 376))):
    top, bot = edge(xa, xb, side)
    for t in [0.10 + 0.0835 * i for i in range(11)]:
        ya, yb = top(xa) + (bot(xa) - top(xa)) * t, top(xb) + (bot(xb) - top(xb)) * t
        a(f'<path d="M{xa} {ya:.1f} L{xb} {yb:.1f}" stroke="#b6aa8a" stroke-width=".9" opacity=".8"/>')
        if random.random() < .78:
            ln = random.randint(40, xb - xa - 8); pts = []
            for k in range(0, ln, 4):
                x = xa + 5 + k; y = ya + (yb - ya) * (k + 5) / (xb - xa) - 2 + random.uniform(-1.6, 1.6); pts.append(f"{x:.1f},{y:.1f}")
            a(f'<polyline points="{" ".join(pts)}" fill="none" stroke="#2b261e" stroke-width="1.1" opacity="{random.uniform(.55, .8):.2f}"/>')
a('<path d="M228 382 q4 14 10 20" stroke="#a1252b" stroke-width="4" fill="none" stroke-linecap="round"/>')
a('<path d="M290 342 L372 306" stroke="#000" stroke-width="7" stroke-linecap="round" opacity=".35" transform="translate(3,5)"/><path d="M290 342 L372 306" stroke="#1b1d20" stroke-width="5.5" stroke-linecap="round"/><path d="M292 340 L370 306" stroke="#4c525b" stroke-width="1.2"/><path d="M366 308 L374 305" stroke="#c9a24a" stroke-width="5"/>')
# --- 光の落ち込み・周辺減光・粒子 ---
a(f'<rect width="{W}" height="{H}" fill="url(#falloff)" style="mix-blend-mode:multiply"/><rect width="{W}" height="{H}" fill="url(#vig)"/>')
a(f'<rect width="{W}" height="{H}" filter="url(#noise)" opacity=".10" style="mix-blend-mode:overlay"/></svg>')
out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "img", "scene-c1.svg")
open(out, "w", encoding="utf-8").write("\n".join(o)); print("作成:", out, round(len("\n".join(o)) / 1024), "KB")
