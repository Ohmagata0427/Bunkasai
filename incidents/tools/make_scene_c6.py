#!/usr/bin/env python3
"""事件5（id: c6）「委託業者経由の侵入」の背景を img/scene-c6.svg として生成（標準ライブラリのみ）。
ネットワーク運用センターの画面。5つの領域（構成図／取引先アクセス台帳／運用手順書／通信ログ／警告一覧）は cases.js のスポット位置に合わせてある。
答えが分かる強調表示は描かない。"""
import os, random
random.seed(36)
W, H = 1000, 440
F = 'font-family="Yu Gothic UI,Meiryo UI,Hiragino Sans,Noto Sans CJK JP,sans-serif"'
M = 'font-family="Cascadia Mono,Consolas,Menlo,monospace"'
o = []; a = o.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="none">')
a(f'<rect width="{W}" height="{H}" fill="#0c1620"/>')
a('<rect width="1000" height="30" fill="#101f2c"/><rect y="30" width="1000" height="1" fill="#25384a"/>')
for i, c in enumerate(("#ec6a5e", "#f4bf4f", "#61c554")): a(f'<circle cx="{18+i*18}" cy="15" r="5" fill="{c}"/>')
a(f'<text x="500" y="19" {F} font-size="11" fill="#8fa6ba" text-anchor="middle">NETWORK OPERATIONS　ネットワーク運用センター</text>')
a('<rect y="31" width="1000" height="20" fill="#0f1c28"/><text x="16" y="45" ' + F + ' font-size="10" fill="#6f879c">店舗システム　›　外部委託先アクセス　›　10月11日〜14日</text>')
def pane(x, y, w, h, title, tag=None):
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="#122231" stroke="#25384a"/>')
    a(f'<text x="{x+12}" y="{y+19}" {F} font-size="12" font-weight="700" fill="#cfe0ee">{title}</text><rect x="{x}" y="{y+27}" width="{w}" height="1" fill="#25384a"/>')
    if tag: a(f'<rect x="{x+w-52}" y="{y+7}" width="40" height="14" rx="2" fill="none" stroke="#4b7bbf"/><text x="{x+w-32}" y="{y+17.5}" {F} font-size="8.5" fill="#7fa6dd" text-anchor="middle">{tag}</text>')
# 構成図
pane(16, 56, 440, 190, "ネットワーク構成")
nodes = [(70, 120, "外部業者"), (170, 120, "空調監視"), (290, 120, "決済管理"), (400, 120, "バックアップ")]
a('<rect x="40" y="168" width="396" height="4" rx="2" fill="#2f4a62"/><text x="44" y="186" ' + M + ' font-size="8" fill="#5f7b92">店舗LAN</text>')
for x, y, t in nodes:
    a(f'<line x1="{x}" y1="{y+14}" x2="{x}" y2="168" stroke="#2f4a62" stroke-width="2"/>')
    a(f'<rect x="{x-34}" y="{y-14}" width="68" height="28" rx="3" fill="#183044" stroke="#3b5b77"/><text x="{x}" y="{y+4}" {F} font-size="10" fill="#cfe0ee" text-anchor="middle">{t}</text>')
a('<line x1="104" y1="120" x2="136" y2="120" stroke="#3b5b77" stroke-width="2" stroke-dasharray="4 3"/>')
a('<rect x="40" y="198" width="120" height="30" rx="3" fill="#183044" stroke="#3b5b77"/><text x="100" y="217" ' + F + ' font-size="10" fill="#cfe0ee" text-anchor="middle">インターネット</text>')
a('<line x1="100" y1="198" x2="100" y2="172" stroke="#3b5b77" stroke-width="2"/>')
for i in range(3): a(f'<rect x="200" y="{198+i*10}" width="{random.randint(150,220)}" height="4" rx="2" fill="#2a4256"/>')
# 取引先アクセス台帳
pane(468, 56, 250, 190, "取引先アクセス台帳")
for i in range(5):
    y = 96 + i * 28
    a(f'<rect x="482" y="{y}" width="{random.randint(150,220)}" height="5" rx="2" fill="#3b5b77"/><rect x="482" y="{y+11}" width="{random.randint(90,180)}" height="5" rx="2" fill="#2a4256"/>')
# 手順書（参照）
pane(730, 56, 254, 190, "運用手順書", "参照")
for i in range(4):
    y = 96 + i * 35
    a(f'<text x="744" y="{y+8}" {M} font-size="9" fill="#6f879c">§{i+1}</text><rect x="768" y="{y}" width="{random.randint(170,205)}" height="5" rx="2" fill="#3f5f85"/><rect x="768" y="{y+12}" width="{random.randint(90,170)}" height="5" rx="2" fill="#2a4256"/>')
# 通信ログ
pane(16, 258, 600, 166, "ファイアウォール通信ログ")
for i in range(6):
    y = 292 + i * 21
    a(f'<rect x="24" y="{y+14}" width="584" height="1" fill="#1b2e3f"/><text x="30" y="{y+10}" {M} font-size="9" fill="#6f879c">10-{random.randint(11,14)} {random.randint(0,23):02d}:{random.randint(0,59):02d}</text><rect x="150" y="{y+4}" width="{random.randint(130,230)}" height="5" rx="2" fill="#3b5b77"/><rect x="420" y="{y+4}" width="{random.randint(60,120)}" height="5" rx="2" fill="#2f4a62"/><rect x="560" y="{y+3}" width="34" height="10" rx="3" fill="#1f4a3a"/>')
# 警告一覧
pane(628, 258, 356, 166, "セキュリティ警告一覧")
for i in range(5):
    y = 296 + i * 24
    a(f'<circle cx="646" cy="{y+5}" r="5" fill="{random.choice(("#3b5b77","#3b5b77","#7a6a2c"))}"/><rect x="660" y="{y}" width="{random.randint(170,260)}" height="5" rx="2" fill="#3b5b77"/><rect x="660" y="{y+11}" width="{random.randint(80,160)}" height="4" rx="2" fill="#2a4256"/>')
a('</svg>')
out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "img", "scene-c6.svg")
open(out, "w", encoding="utf-8").write("\n".join(o)); print("作成:", out, round(len("\n".join(o)) / 1024), "KB")
