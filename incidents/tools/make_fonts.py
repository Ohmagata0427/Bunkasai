#!/usr/bin/env python3
"""「解雇通知書」の画面で使う文字だけを抜き出した明朝体（Noto Serif CJK JP, SIL OFL 1.1）を fonts/ に作る。
通知書の文面を変えたら、もう一度実行すること。  使い方: python tools/make_fonts.py
必要: fonttools（pip install fonttools）、PC内の NotoSerifCJK-Regular/Bold.ttc"""
import os, re, sys, glob
from fontTools import subset
from fontTools.ttLib import TTCollection

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
chars = set()
html = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
fired = html[html.index('<div id="fired"'):]       # 埋め込み明朝は「解雇通知書」の画面でだけ使う
chars.update(re.sub(r"<[^>]+>", "", fired))
for a, b in ((0x20, 0x7E), (0x3000, 0x303F), (0xFF01, 0xFF5E)): chars.update(chr(c) for c in range(a, b + 1))
chars.update("○●×　年月日")
chars = "".join(sorted(chars))

def find(name):
    for d in ("/usr/share/fonts/opentype/noto", "/usr/share/fonts/noto-cjk", os.path.expanduser("~/Library/Fonts"), "/Library/Fonts", "C:/Windows/Fonts"):
        p = glob.glob(os.path.join(d, name))
        if p: return p[0]
    sys.exit("フォントが見つかりません: " + name)

os.makedirs(os.path.join(ROOT, "fonts"), exist_ok=True)
for src, out in (("NotoSerifCJK-Regular.ttc", "serif-regular.woff"), ("NotoSerifCJK-Bold.ttc", "serif-bold.woff")):
    path = find(src); idx = 0
    for i, f in enumerate(TTCollection(path).fonts):
        if any("Noto Serif CJK JP" in n.toUnicode() for n in f["name"].names if n.nameID == 1): idx = i; break
    opt = subset.Options(); opt.flavor = "woff"; opt.font_number = idx; opt.layout_features = ["locl", "kern", "vert", "vrt2"]
    opt.notdef_outline = True; opt.name_IDs = ["*"]; opt.hinting = False
    font = subset.load_font(path, opt, dontLoadGlyphNames=True)
    s = subset.Subsetter(opt); s.populate(text=chars); s.subset(font)
    dst = os.path.join(ROOT, "fonts", out); subset.save_font(font, dst, opt)
    print(out, round(os.path.getsize(dst) / 1024), "KB", len(chars), "文字")
