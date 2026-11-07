#!/usr/bin/env python3
"""公開用フォルダ deploy/ を作る（HTTPS配信向け：オフライン動作＝PWA、検索除外、角タップのデバッグ無効）。
使い方: python tools/build_deploy.py   →  deploy/ をそのままホスティングにアップロードする。"""
import os, io, re, json, shutil, hashlib
from PIL import Image, ImageDraw
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = os.path.join(ROOT, "deploy")
rd = lambda f: open(os.path.join(ROOT, f), encoding="utf-8").read()
shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT + "/img"); os.makedirs(OUT + "/fonts")

# 画像（導入画面用）は小さく軽くする
for n in ("office", "report", "result"):
    im = Image.open(f"{ROOT}/img/{n}.png").convert("RGB"); im.thumbnail((720, 720))
    im.convert("P", palette=Image.ADAPTIVE, colors=96).save(f"{OUT}/img/{n}.png", optimize=True)
for f in sorted(os.listdir(f"{ROOT}/img")):
    if f.endswith(".svg"): shutil.copy(f"{ROOT}/img/{f}", f"{OUT}/img/{f}")   # 事件ごとの背景（SVG）
for f in ("serif-regular.woff", "serif-bold.woff"): shutil.copy(f"{ROOT}/fonts/{f}", f"{OUT}/fonts/{f}")
os.makedirs(OUT + "/sounds", exist_ok=True)
for f in sorted(os.listdir(f"{ROOT}/sounds")):
    if f.endswith(".mp3"): shutil.copy(f"{ROOT}/sounds/{f}", f"{OUT}/sounds/{f}")   # 効果音
for f in ("style.css", "app.js", "cases.js", "debug.js"): shutil.copy(f"{ROOT}/{f}", f"{OUT}/{f}")
open(OUT + "/config.js", "w").write("window.INCIDENTS_CONFIG={debugTap:false};\n")
open(OUT + "/pwa.js", "w").write('if("serviceWorker" in navigator&&(location.protocol==="https:"||location.hostname==="localhost"||location.hostname==="127.0.0.1")){window.addEventListener("load",function(){navigator.serviceWorker.register("sw.js").catch(function(e){console.warn("sw",e)})})}\n')

# アイコン（フラットな虫眼鏡）
def icon(size, pad=0.0):
    im = Image.new("RGB", (size, size), "#161715"); d = ImageDraw.Draw(im); u = size * (1 - 2 * pad) / 100; o = size * pad
    P = lambda v: o + v * u
    d.ellipse([P(18), P(14), P(68), P(64)], outline="#e8e3d3", width=max(2, int(9 * u)))
    d.line([P(60), P(58), P(84), P(86)], fill="#e8e3d3", width=max(2, int(11 * u)))
    d.rectangle([P(36), P(32), P(50), P(46)], fill="#b3261e"); return im
icon(192).save(OUT + "/icon-192.png"); icon(512).save(OUT + "/icon-512.png"); icon(512, 0.14).save(OUT + "/icon-maskable.png"); icon(180).save(OUT + "/apple-touch-icon.png")
json.dump({"name": "INCIDENTS", "short_name": "INCIDENTS", "lang": "ja", "start_url": "./", "scope": "./", "display": "standalone",
           "background_color": "#161715", "theme_color": "#0e0f0e",
           "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"},
                     {"src": "icon-maskable.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}]},
          open(OUT + "/manifest.webmanifest", "w"), ensure_ascii=False, indent=1)

h = rd("index.html")
h = h.replace('<meta name="theme-color" content="#0a0d0f">', '<meta name="theme-color" content="#0e0f0e">\n<meta name="robots" content="noindex,nofollow,noarchive">\n<link rel="manifest" href="manifest.webmanifest">\n<link rel="apple-touch-icon" href="apple-touch-icon.png">\n<meta name="apple-mobile-web-app-capable" content="yes">\n<meta name="mobile-web-app-capable" content="yes">\n<meta name="apple-mobile-web-app-title" content="INCIDENTS">')
assert 'rel="manifest"' in h
h = h.replace('<script src="debug.js"></script>', '<script src="config.js"></script>\n<script src="debug.js"></script>', 1)
h = h.replace("</body>", '<script src="pwa.js"></script>\n</body>', 1)
open(OUT + "/index.html", "w", encoding="utf-8").write(h)
open(OUT + "/robots.txt", "w").write("User-agent: *\nDisallow: /\n")
open(OUT + "/_headers", "w").write("/*\n  X-Robots-Tag: noindex, nofollow, noarchive\n  Referrer-Policy: no-referrer\n  X-Content-Type-Options: nosniff\n/sw.js\n  Cache-Control: no-cache\n/index.html\n  Cache-Control: no-cache\n")

assets = sorted(os.path.relpath(os.path.join(dp, f), OUT).replace("\\", "/") for dp, _, fs in os.walk(OUT) for f in fs if f not in ("sw.js", "_headers", "robots.txt"))
ver = hashlib.sha1(b"".join(open(os.path.join(OUT, a), "rb").read() for a in assets)).hexdigest()[:10]
sw = '''const CACHE="incidents-%s";
const ASSETS=%s;
self.addEventListener("install",e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(ASSETS)).then(()=>self.skipWaiting()))});
self.addEventListener("activate",e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(n=>n!==CACHE).map(n=>caches.delete(n)))).then(()=>self.clients.claim()))});
self.addEventListener("fetch",e=>{
  if(e.request.method!=="GET")return;
  const u=new URL(e.request.url); if(u.origin!==location.origin)return;
  e.respondWith(caches.match(e.request,{ignoreSearch:true}).then(r=>r||fetch(e.request).catch(()=>e.request.mode==="navigate"?caches.match("index.html"):Response.error())));
});
''' % (ver, json.dumps(["./"] + assets))
open(OUT + "/sw.js", "w").write(sw)
tot = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(OUT) for f in fs)
print("deploy/ を作成:", len(assets), "ファイル / 合計", round(tot / 1024), "KB / キャッシュ版", ver)
