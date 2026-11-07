#!/usr/bin/env python3
"""事件2「新入社員・高橋のPCデスクトップ」の背景を img/scene-c2.svg として生成（標準ライブラリのみ）。
ウィンドウの位置は cases.js のスポット位置（ブラウザ／文書／ネットワーク）に合わせてある。通知（ad）は6秒後にHTML側で現れるため、ここには描かない。"""
import os, random
random.seed(5)
W, H = 1000, 440
F = 'font-family="Yu Gothic UI,Meiryo UI,Hiragino Sans,Noto Sans CJK JP,sans-serif"'
M = 'font-family="Cascadia Mono,Consolas,Menlo,monospace"'
o = []; a = o.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="none">')
a('''<defs>
<linearGradient id="wp" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0a3585"/><stop offset=".55" stop-color="#1768cf"/><stop offset="1" stop-color="#0a2c6c"/></linearGradient>
<linearGradient id="petal" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#52b6ff" stop-opacity=".0"/><stop offset=".5" stop-color="#4aa6f5" stop-opacity=".75"/><stop offset="1" stop-color="#1a58c6" stop-opacity=".85"/></linearGradient>
<linearGradient id="task" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#18212e"/><stop offset="1" stop-color="#0d131c"/></linearGradient>
<filter id="sh" x="-10%" y="-10%" width="120%" height="125%"><feGaussianBlur stdDeviation="7"/></filter>
<filter id="b2"><feGaussianBlur stdDeviation="2"/></filter>
<filter id="noise" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="3"/><feColorMatrix type="saturate" values="0"/></filter>
<radialGradient id="vig" cx=".5" cy=".45" r=".8"><stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".28"/></radialGradient>
</defs>''')
a(f'<rect width="{W}" height="{H}" fill="url(#wp)"/>')
for i in range(9):
    a(f'<ellipse cx="740" cy="250" rx="190" ry="52" fill="url(#petal)" transform="rotate({i*40-10} 640 250)" opacity=".62"/>')
a('<ellipse cx="640" cy="250" rx="46" ry="36" fill="#7cc8ff" opacity=".35" filter="url(#sh)"/>')
# --- デスクトップのアイコン（ブラウザの下に見える） ---
def label(x, t): a(f'<text x="{x}" y="392" {F} font-size="10" fill="#fff" text-anchor="middle" style="paint-order:stroke" stroke="#0a2a5c" stroke-width="2.5">{t}</text>')
a('<path d="M26 318 h24 l-2 38 h-20 z" fill="#c9d3df"/><path d="M24 316 h28 v4 h-28 z" fill="#e6ecf3"/><path d="M33 325 v26 M38 325 v26 M43 325 v26" stroke="#8b99aa" stroke-width="1.5"/>'); label(38, "ごみ箱")
a('<path d="M84 322 h14 l4 5 h22 v28 h-40 z" fill="#f0c23d"/><path d="M84 330 h40 v25 h-40 z" fill="#ffd966"/>'); label(104, "資料")
a('<path d="M156 318 l20 7 v16 q0 14 -20 21 q-20 -7 -20 -21 v-16 z" fill="#3b8f6c"/><path d="M146 340 l7 7 l13 -14" stroke="#fff" stroke-width="3" fill="none"/>'); label(156, "Vault")
# --- ウィンドウ共通 ---
def win(x, y, w, h, bar, barfill, title, tcol):
    a(f'<rect x="{x+3}" y="{y+6}" width="{w}" height="{h}" rx="7" fill="#000" opacity=".42" filter="url(#sh)"/>')
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="#fbfbfc" stroke="#b6bdc8"/>')
    a(f'<path d="M{x} {y+bar} v-{bar-7} a7 7 0 0 1 7 -7 h{w-14} a7 7 0 0 1 7 7 v{bar-7} z" fill="{barfill}"/>')
    if title: a(f'<text x="{x+34}" y="{y+bar/2+4}" {F} font-size="11" fill="{tcol}">{title}</text>')
    for i, g in enumerate(("—", "□", "×")): a(f'<text x="{x+w-62+i*22}" y="{y+bar/2+4}" {F} font-size="12" fill="{tcol}" text-anchor="middle">{g}</text>')
# --- ブラウザ（社内ポータル） ---
win(30, 26, 460, 264, 30, "#dfe4ec", "", "#333")
a('<path d="M40 56 v-18 a6 6 0 0 1 6 -6 h118 a6 6 0 0 1 6 6 v18 z" fill="#fbfbfc"/><circle cx="54" cy="45" r="5" fill="#2b6cb0"/><text x="66" y="49" ' + F + ' font-size="11" fill="#222">社内ポータル</text><text x="150" y="49" ' + F + ' font-size="11" fill="#555">×</text><text x="184" y="50" ' + F + ' font-size="13" fill="#444">＋</text>')
a('<rect x="31" y="56" width="458" height="32" fill="#fbfbfc"/><text x="44" y="77" ' + F + ' font-size="14" fill="#555">←　→　⟳</text><rect x="114" y="61" width="366" height="22" rx="11" fill="#e8ecf2"/>')
a('<path d="M130 78 l7 -13 l7 13 z" fill="#e8a317"/><rect x="136.4" y="68" width="1.4" height="5" fill="#fff"/><text x="152" y="76" ' + F + ' font-size="10" font-weight="700" fill="#b3261e">保護されていない通信</text><text x="262" y="76" ' + M + ' font-size="9" fill="#333">http://portal.hokushin-ds.example/login</text>')
a('<rect x="31" y="88" width="458" height="201" fill="#eaeff6"/><rect x="150" y="104" width="220" height="172" rx="8" fill="#000" opacity=".12" filter="url(#b2)" transform="translate(2,3)"/><rect x="150" y="104" width="220" height="172" rx="8" fill="#fff"/>')
a(f'<text x="260" y="136" {F} font-size="18" font-weight="700" fill="#1d2430" text-anchor="middle">社内ポータル</text><text x="170" y="158" {F} font-size="10" fill="#555">ID</text><rect x="170" y="162" width="180" height="20" rx="3" fill="#fff" stroke="#aab4c2"/><text x="177" y="176" {F} font-size="10" fill="#333">takahashi</text>')
a(f'<text x="170" y="200" {F} font-size="10" fill="#555">パスワード</text><rect x="170" y="204" width="180" height="20" rx="3" fill="#fff" stroke="#aab4c2"/><text x="177" y="218" {F} font-size="11" fill="#333" letter-spacing="2">●●●●●●●●●</text><rect x="170" y="238" width="180" height="24" rx="4" fill="#2b6cb0"/><text x="260" y="254" {F} font-size="12" font-weight="700" fill="#fff" text-anchor="middle">ログイン</text>')
# --- 文書（パスワード一覧.docx） ---
win(520, 26, 440, 106, 24, "#2b579a", "パスワード一覧.docx - 文書", "#fff")
a('<rect x="521" y="50" width="438" height="20" fill="#f1f2f4"/><text x="532" y="64" ' + F + ' font-size="9.5" fill="#444">ファイル　ホーム　挿入　レイアウト　表示</text><rect x="521" y="70" width="438" height="61" fill="#dde0e5"/><rect x="570" y="74" width="340" height="58" fill="#fff"/>')
a(f'<text x="584" y="90" {F} font-size="12" font-weight="700" fill="#222">パスワード一覧</text><text x="584" y="104" {M} font-size="9.5" fill="#333">社内ポータル　takahashi / Hk#2024pass</text><text x="584" y="117" {M} font-size="9.5" fill="#333">メール　　　　t.takahashi / Mail-0928</text><text x="584" y="130" {M} font-size="9.5" fill="#333">VPN　　　　　takahashi / vpn!Secret1</text>')
# --- ネットワーク設定（Wi-Fi） ---
win(520, 150, 440, 106, 26, "#f3f3f3", "設定　›　ネットワークとインターネット　›　Wi-Fi", "#333")
a(f'<text x="536" y="190" {F} font-size="12" font-weight="700" fill="#222">Wi-Fi</text><rect x="912" y="178" width="30" height="14" rx="7" fill="#2b6cb0"/><circle cx="935" cy="185" r="5" fill="#fff"/>')
def wifi(cx, cy, col): a(f'<path d="M{cx-9} {cy-3} a13 13 0 0 1 18 0 M{cx-6} {cy+1} a8 8 0 0 1 12 0" stroke="{col}" stroke-width="2" fill="none"/><circle cx="{cx}" cy="{cy+5}" r="1.8" fill="{col}"/>')
a('<rect x="530" y="196" width="420" height="26" fill="#eaf2fb"/>'); wifi(550, 207, "#2b6cb0")
a(f'<text x="572" y="206" {F} font-size="11.5" font-weight="700" fill="#222">Free_WiFi_Station</text><text x="572" y="218" {F} font-size="9.5" font-weight="700" fill="#b3261e">接続済み　セキュリティ保護なし</text>')
a('<path d="M922 205 v-4 a5 5 0 0 1 9 -2" stroke="#e8a317" stroke-width="2" fill="none"/><rect x="918" y="205" width="13" height="10" rx="2" fill="#e8a317"/>')
wifi(550, 236, "#888"); a(f'<text x="572" y="238" {F} font-size="11" fill="#333">Hokushin-Office</text><text x="572" y="250" {F} font-size="9.5" fill="#666">セキュリティ保護あり</text><rect x="918" y="236" width="13" height="10" rx="2" fill="#777"/><path d="M921 236 v-4 a3.5 3.5 0 0 1 7 0 v4" stroke="#777" stroke-width="2" fill="none"/>')
# --- タスクバー ---
a(f'<rect y="404" width="{W}" height="36" fill="url(#task)"/><rect y="404" width="{W}" height="1" fill="#34455c"/>')
for i, (x, c) in enumerate(((480, "#4aa6f5"), (506, "#5a6472"), (532, "#5a6472"))):
    pass
a('<g fill="#4aa6f5"><rect x="480" y="414" width="8" height="8"/><rect x="490" y="414" width="8" height="8"/><rect x="480" y="424" width="8" height="8"/><rect x="490" y="424" width="8" height="8"/></g>')
a('<circle cx="522" cy="423" r="6" fill="none" stroke="#cfd8e3" stroke-width="2"/><path d="M527 428 l5 5" stroke="#cfd8e3" stroke-width="2"/><rect x="552" y="414" width="18" height="18" rx="3" fill="#2d78d4"/><rect x="582" y="414" width="18" height="18" rx="3" fill="#f0c23d"/><rect x="612" y="414" width="18" height="18" rx="3" fill="#2b579a"/><rect x="552" y="436" width="18" height="2" fill="#4aa6f5"/>')
a(f'<path d="M845 420 a9 9 0 0 1 12 0 M848 424 a5 5 0 0 1 6 0" stroke="#e5ecf4" stroke-width="1.6" fill="none"/><circle cx="851" cy="428" r="1.4" fill="#e5ecf4"/><rect x="876" y="419" width="16" height="9" rx="1.5" fill="none" stroke="#e5ecf4" stroke-width="1.4"/><text x="965" y="420" {F} font-size="10.5" fill="#e5ecf4" text-anchor="end">12:08</text><text x="965" y="432" {F} font-size="9" fill="#b9c6d6" text-anchor="end">2026/10/14</text>')
a(f'<rect width="{W}" height="{H}" fill="url(#vig)"/><rect width="{W}" height="{H}" filter="url(#noise)" opacity=".07" style="mix-blend-mode:overlay"/></svg>')
out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "img", "scene-c2.svg")
open(out, "w", encoding="utf-8").write("\n".join(o)); print("作成:", out, round(len("\n".join(o)) / 1024), "KB")
