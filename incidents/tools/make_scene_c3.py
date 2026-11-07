#!/usr/bin/env python3
"""事件3「VPN管理コンソール」の背景を img/scene-c3.svg として生成（標準ライブラリのみ）。
4つのカード（アカウント一覧／認証ログ／退職手続／運用手順書）は cases.js のスポット位置に合わせてある。答えが分かる強調表示は描かない。"""
import os, random
random.seed(9)
W, H = 1000, 440
F = 'font-family="Yu Gothic UI,Meiryo UI,Hiragino Sans,Noto Sans CJK JP,sans-serif"'
M = 'font-family="Cascadia Mono,Consolas,Menlo,monospace"'
o = []; a = o.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="none">')
a('<defs><filter id="noise" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="3"/><feColorMatrix type="saturate" values="0"/></filter><radialGradient id="vig" cx=".5" cy=".5" r=".8"><stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".4"/></radialGradient></defs>')
a(f'<rect width="{W}" height="{H}" fill="#0f1623"/>')
a('<rect width="1000" height="34" fill="#0a0f18"/><rect y="33" width="1000" height="1" fill="#26364e"/><rect x="14" y="10" width="14" height="14" rx="3" fill="#4aa6f5"/>')
a(f'<text x="38" y="22" {F} font-size="12" font-weight="700" fill="#dbe6f3">NetAdmin　VPN管理コンソール</text><text x="940" y="22" {F} font-size="10" fill="#8ea3bd" text-anchor="end">管理者：運用担当</text><circle cx="954" cy="17" r="4" fill="#3fb27f"/>')
a('<rect y="34" width="150" height="406" fill="#0b1220"/><rect x="150" y="34" width="1" height="406" fill="#26364e"/>')
for i, t in enumerate(("ダッシュボード", "アカウント", "VPN接続", "認証ログ", "ポリシー", "設定")):
    y = 62 + i * 32
    if t == "アカウント": a(f'<rect x="0" y="{y-16}" width="150" height="28" fill="#16233a"/><rect x="0" y="{y-16}" width="3" height="28" fill="#4aa6f5"/>')
    a(f'<rect x="18" y="{y-8}" width="10" height="10" rx="2" fill="#2d4466"/><text x="38" y="{y+1}" {F} font-size="11" fill="{"#dbe6f3" if t=="アカウント" else "#8ea3bd"}">{t}</text>')
def card(x, y, w, h, title, tag=None):
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#161f30" stroke="#26364e"/><text x="{x+16}" y="{y+22}" {F} font-size="12" font-weight="700" fill="#dbe6f3">{title}</text><rect x="{x}" y="{y+32}" width="{w}" height="1" fill="#26364e"/>')
    if tag: a(f'<rect x="{x+w-64}" y="{y+9}" width="50" height="16" rx="3" fill="none" stroke="#4b7bbf"/><text x="{x+w-39}" y="{y+21}" {F} font-size="9.5" fill="#8fb4e8" text-anchor="middle">{tag}</text>')
card(170, 40, 450, 190, "アカウント一覧（VPN）")
for j, (t, x) in enumerate((("アカウント", 186), ("所有者", 296), ("最終ログイン", 410), ("多要素認証", 490), ("状態", 574))):
    a(f'<text x="{x}" y="{86}" {F} font-size="9" fill="#7389a6">{t}</text>')
for i in range(6):
    y = 96 + i * 21
    a(f'<rect x="178" y="{y}" width="434" height="1" fill="#22304a"/><rect x="186" y="{y+8}" width="{random.randint(52,84)}" height="5" rx="2" fill="#35496a"/><rect x="296" y="{y+8}" width="{random.randint(34,70)}" height="5" rx="2" fill="#2a3b58"/><rect x="410" y="{y+8}" width="{random.randint(30,48)}" height="5" rx="2" fill="#2a3b58"/><rect x="490" y="{y+8}" width="{random.randint(24,40)}" height="5" rx="2" fill="#2a3b58"/><rect x="574" y="{y+4}" width="32" height="13" rx="3" fill="#1f5b46"/><text x="590" y="{y+14}" {F} font-size="8.5" fill="#9fe0c3" text-anchor="middle">有効</text>')
card(640, 40, 340, 190, "VPN認証ログ")
for i in range(9):
    y = 76 + i * 17; t = f"{random.choice(('02','03','09','10','14'))}:{random.randint(10,59)}"
    a(f'<text x="654" y="{y+11}" {M} font-size="8.5" fill="#7f93ad">{t}</text><rect x="694" y="{y+5}" width="{random.randint(100,230)}" height="5" rx="2" fill="{random.choice(["#2f6f58","#2f6f58","#35496a"])}" opacity=".85"/>')
card(170, 250, 360, 168, "退職手続チェックリスト")
for i in range(4):
    y = 300 + i * 28
    a(f'<rect x="188" y="{y-10}" width="14" height="14" rx="3" fill="none" stroke="#4b6a94" stroke-width="1.5"/><rect x="214" y="{y-5}" width="{random.randint(150,250)}" height="5" rx="2" fill="#35496a"/><rect x="214" y="{y+5}" width="{random.randint(60,120)}" height="4" rx="2" fill="#26364e"/>')
card(560, 250, 420, 168, "運用手順書　第6章　アカウント管理", "参照")
for i in range(6):
    y = 286 + i * 18
    a(f'<rect x="578" y="{y}" width="{random.randint(250,380)}" height="5" rx="2" fill="#2f4668"/>')
a(f'<rect y="424" width="1000" height="16" fill="#0a0f18"/><text x="14" y="435" {F} font-size="9" fill="#6f87a6">接続中のセッション：3　／　最終更新：10月15日 09:10</text>')
a(f'<rect width="{W}" height="{H}" fill="url(#vig)"/><rect width="{W}" height="{H}" filter="url(#noise)" opacity=".06" style="mix-blend-mode:overlay"/></svg>')
out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "img", "scene-c3.svg")
open(out, "w", encoding="utf-8").write("\n".join(o)); print("作成:", out, round(len("\n".join(o)) / 1024), "KB")
