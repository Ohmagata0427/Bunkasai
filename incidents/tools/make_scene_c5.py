#!/usr/bin/env python3
"""事件4（id: c5）「ヘルプデスク問い合わせログ」の背景を img/scene-c5.svg として生成（標準ライブラリのみ）。
白基調の監査ログ・コンプライアンス管理ソフト。4つの領域（通話記録／本人確認手順書／社員プロフィール／監査ログ）は cases.js のスポット位置に合わせてある。答えが分かる強調表示は描かない。"""
import os, random
random.seed(21)
W, H = 1000, 440
F = 'font-family="Yu Gothic UI,Meiryo UI,Hiragino Sans,Noto Sans CJK JP,sans-serif"'
M = 'font-family="Cascadia Mono,Consolas,Menlo,monospace"'
o = []; a = o.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="none">')
a('<defs><filter id="sh" x="-5%" y="-5%" width="110%" height="112%"><feGaussianBlur stdDeviation="3"/></filter></defs>')
a(f'<rect width="{W}" height="{H}" fill="#e9edf2"/>')
a('<rect width="1000" height="30" fill="#dfe4eb"/><rect y="30" width="1000" height="1" fill="#c3cad4"/>')
for i, c in enumerate(("#ec6a5e", "#f4bf4f", "#61c554")): a(f'<circle cx="{18+i*18}" cy="15" r="5" fill="{c}"/>')
a(f'<text x="500" y="19" {F} font-size="11" fill="#555" text-anchor="middle">AUDIT LOG　監査ログ・コンプライアンス管理</text>')
a('<rect y="31" width="1000" height="22" fill="#f7f8fa"/><text x="16" y="46" ' + F + ' font-size="10" fill="#6a7482">ヘルプデスク　›　問い合わせ対応　›　10月15日</text><rect x="860" y="35" width="124" height="14" rx="7" fill="#e7ebf0"/><text x="872" y="45" ' + F + ' font-size="8.5" fill="#8a94a2">検索</text>')
def pane(x, y, w, h, title, tag=None):
    a(f'<rect x="{x+1}" y="{y+2}" width="{w}" height="{h}" rx="4" fill="#000" opacity=".12" filter="url(#sh)"/><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="#fff" stroke="#cdd3dc"/>')
    a(f'<text x="{x+12}" y="{y+20}" {F} font-size="12" font-weight="700" fill="#2a3340">{title}</text><rect x="{x}" y="{y+28}" width="{w}" height="1" fill="#e2e6ec"/>')
    if tag: a(f'<rect x="{x+w-52}" y="{y+8}" width="40" height="14" rx="3" fill="none" stroke="#4b7bbf"/><text x="{x+w-32}" y="{y+18.5}" {F} font-size="8.5" fill="#4b7bbf" text-anchor="middle">{tag}</text>')
# 通話記録（チャット風）
pane(16, 60, 324, 170, "通話記録")
for i in range(4):
    y = 98 + i * 32; left = i % 2 == 0; x = 28 if left else 120
    a(f'<circle cx="{34 if left else 322}" cy="{y+8}" r="9" fill="#cfd6e0"/><rect x="{x+22 if left else x}" y="{y}" width="{random.randint(120,170)}" height="22" rx="8" fill="{"#eef1f5" if left else "#dfeafa"}"/><rect x="{x+32 if left else x+10}" y="{y+8}" width="{random.randint(70,110)}" height="5" rx="2" fill="#aeb8c6"/>')
# 手順書
pane(352, 60, 324, 170, "本人確認手順書", "参照")
for i in range(5):
    y = 98 + i * 25
    a(f'<text x="366" y="{y+8}" {M} font-size="9" fill="#8a94a2">{i+1}.</text><rect x="386" y="{y+1}" width="{random.randint(200,270)}" height="5" rx="2" fill="#b4becb"/><rect x="386" y="{y+11}" width="{random.randint(100,190)}" height="5" rx="2" fill="#d3d9e1"/>')
# 社員プロフィール
pane(688, 60, 296, 170, "社員プロフィール（公開情報）")
a('<circle cx="722" cy="118" r="20" fill="#cfd6e0"/><circle cx="722" cy="112" r="7" fill="#aeb8c6"/><path d="M708 132 q14 -14 28 0" fill="#aeb8c6"/>')
for i in range(5):
    y = 100 + i * 20
    a(f'<rect x="756" y="{y}" width="{random.randint(80,150)}" height="5" rx="2" fill="{"#aeb8c6" if i == 0 else "#d3d9e1"}"/>')
a('<rect x="704" y="156" width="264" height="1" fill="#e2e6ec"/>')
for i in range(3): a(f'<rect x="704" y="{168+i*18}" width="{random.randint(150,240)}" height="5" rx="2" fill="#d3d9e1"/>')
# 監査ログ（表）
pane(16, 244, 968, 180, "監査ログ")
for t, x in (("日時", 30), ("操作", 170), ("対象ユーザー", 420), ("実行者", 600), ("結果", 760)): a(f'<text x="{x}" y="{288}" {F} font-size="9" fill="#7a8494">{t}</text>')
for i in range(6):
    y = 296 + i * 21; hh = random.choice(("13","14","14","14")); mm = random.randint(0, 59)
    a(f'<rect x="24" y="{y+14}" width="952" height="1" fill="#eaeef2"/><text x="30" y="{y+10}" {M} font-size="9" fill="#6a7482">10-15 {hh}:{mm:02d}</text><rect x="170" y="{y+4}" width="{random.randint(100,190)}" height="5" rx="2" fill="#b4becb"/><rect x="420" y="{y+4}" width="{random.randint(60,100)}" height="5" rx="2" fill="#c3ccd8"/><rect x="600" y="{y+4}" width="{random.randint(60,110)}" height="5" rx="2" fill="#c3ccd8"/><rect x="760" y="{y+3}" width="34" height="10" rx="3" fill="#dde9dd"/>')
a('</svg>')
out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "img", "scene-c5.svg")
open(out, "w", encoding="utf-8").write("\n".join(o)); print("作成:", out, round(len("\n".join(o)) / 1024), "KB")
