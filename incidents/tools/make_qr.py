#!/usr/bin/env python3
"""QRコード作成（標準ライブラリのみ・インターネット不要）。
使い方:  python make_qr.py https://example.pages.dev/xxxx  [出力名]  [--ecl L|M|Q|H] [--mask 0-7]
出力:    <出力名>.png（印刷用・大きめ）と <出力名>.svg（拡大しても劣化しない）。既定は誤り訂正 Q。"""
import sys, zlib, struct

ECC = {"L": 1, "M": 0, "Q": 3, "H": 2}; ECC_IDX = {"L": 0, "M": 1, "Q": 2, "H": 3}
ECC_PER_BLOCK = [
 [None,7,10,15,20,26,18,20,24,30,18,20,24,26,30,22,24,28,30,28,28,28,28,30,30,26,28,30,30,30,30,30,30,30,30,30,30,30,30,30,30],
 [None,10,16,26,18,24,16,18,22,22,26,30,22,22,24,24,28,28,26,26,26,26,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28],
 [None,13,22,18,26,18,24,18,22,20,24,28,26,24,20,30,24,28,28,26,30,28,30,30,30,30,28,30,30,30,30,30,30,30,30,30,30,30,30,30,30],
 [None,17,28,22,16,22,28,26,26,24,28,24,28,22,24,24,30,28,28,26,28,30,24,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30]]
NUM_BLOCKS = [
 [None,1,1,1,1,1,2,2,2,2,4,4,4,4,4,6,6,6,6,7,8,8,9,9,10,12,12,12,13,14,15,16,17,18,19,19,20,21,22,24,25],
 [None,1,1,1,2,2,4,4,4,5,5,5,8,9,9,10,10,11,13,14,16,17,17,18,20,21,23,25,26,28,29,31,33,35,37,38,40,43,45,47,49],
 [None,1,1,2,2,4,4,6,6,8,8,8,10,12,16,12,17,16,18,21,20,23,23,25,27,29,34,34,35,38,40,43,45,48,51,53,56,59,62,65,68],
 [None,1,1,2,4,4,4,5,6,8,8,11,11,16,16,18,16,19,21,25,25,25,34,30,32,35,37,40,42,45,48,51,54,57,60,63,66,70,74,77,81]]

def raw_modules(v):
    r = (16 * v + 128) * v + 64
    if v >= 2:
        n = v // 7 + 2; r -= (25 * n - 10) * n - 55
        if v >= 7: r -= 36
    return r
def data_cw(v, e): return raw_modules(v) // 8 - ECC_PER_BLOCK[e][v] * NUM_BLOCKS[e][v]

def rs_divisor(deg):
    res = [0] * (deg - 1) + [1]; root = 1
    for _ in range(deg):
        for j in range(deg):
            res[j] = rs_mul(res[j], root)
            if j + 1 < deg: res[j] ^= res[j + 1]
        root = rs_mul(root, 2)
    return res
def rs_mul(x, y):
    z = 0
    for i in range(7, -1, -1):
        z = (z << 1) ^ ((z >> 7) * 0x11D); z ^= ((y >> i) & 1) * x
    return z
def rs_rem(data, div):
    res = [0] * len(div)
    for b in data:
        f = b ^ res.pop(0); res.append(0)
        for i, c in enumerate(div): res[i] ^= rs_mul(c, f)
    return res

def make(text, ecl="Q", force=None):
    data = text.encode("utf-8"); e = ECC_IDX[ecl]
    for v in range(1, 41):
        cc = 8 if v <= 9 else 16
        if 4 + cc + 8 * len(data) <= data_cw(v, e) * 8: break
    else: raise ValueError("文字列が長すぎます")
    bits = [int(c) for c in format(4, "04b") + format(len(data), "0%db" % cc) + "".join(format(b, "08b") for b in data)]
    cap = data_cw(v, e) * 8; bits += [0] * min(4, cap - len(bits)); bits += [0] * (-len(bits) % 8)
    cws = [int("".join(map(str, bits[i:i + 8])), 2) for i in range(0, len(bits), 8)]
    pad = 0xEC
    while len(cws) < data_cw(v, e): cws.append(pad); pad ^= 0xEC ^ 0x11
    nb, eb, raw = NUM_BLOCKS[e][v], ECC_PER_BLOCK[e][v], raw_modules(v) // 8
    ns = nb - raw % nb; sl = raw // nb; div = rs_divisor(eb); blocks = []; k = 0
    for i in range(nb):
        d = cws[k:k + sl - eb + (0 if i < ns else 1)]; k += len(d)
        ecc = rs_rem(d, div)
        if i < ns: d = d + [None]
        blocks.append(d + ecc)
    out = []
    for i in range(len(blocks[0])):
        for j, b in enumerate(blocks):
            if i != sl - eb or j >= ns: out.append(b[i])
    size = v * 4 + 17
    M = [[False] * size for _ in range(size)]; F = [[False] * size for _ in range(size)]
    def setf(x, y, d): M[y][x] = d; F[y][x] = True
    for i in range(size): setf(6, i, i % 2 == 0); setf(i, 6, i % 2 == 0)
    for cx, cy in ((3, 3), (size - 4, 3), (3, size - 4)):
        for dy in range(-4, 5):
            for dx in range(-4, 5):
                x, y = cx + dx, cy + dy
                if 0 <= x < size and 0 <= y < size: setf(x, y, max(abs(dx), abs(dy)) not in (2, 4))
    if v > 1:
        n = v // 7 + 2; step = 26 if v == 32 else (v * 4 + n * 2 + 1) // (n * 2 - 2) * 2
        pos = [size - 7 - i * step for i in range(n - 1)] + [6]; pos.reverse()
        for i, cy in enumerate(pos):
            for j, cx in enumerate(pos):
                if (i == 0 and j == 0) or (i == 0 and j == n - 1) or (i == n - 1 and j == 0): continue
                for dy in range(-2, 3):
                    for dx in range(-2, 3): setf(cx + dx, cy + dy, max(abs(dx), abs(dy)) != 1)
    def fmt(mask):
        d = ECC[ecl] << 3 | mask; r = d
        for _ in range(10): r = (r << 1) ^ ((r >> 9) * 0x537)
        b = (d << 10 | r) ^ 0x5412; bit = lambda i: (b >> i) & 1 == 1
        for i in range(6): setf(8, i, bit(i))
        setf(8, 7, bit(6)); setf(8, 8, bit(7)); setf(7, 8, bit(8))
        for i in range(9, 15): setf(14 - i, 8, bit(i))
        for i in range(8): setf(size - 1 - i, 8, bit(i))
        for i in range(8, 15): setf(8, size - 15 + i, bit(i))
        setf(8, size - 8, True)
    fmt(0)
    if v >= 7:
        r = v
        for _ in range(12): r = (r << 1) ^ ((r >> 11) * 0x1F25)
        b = v << 12 | r
        for i in range(18):
            c = (b >> i) & 1 == 1; a = size - 11 + i % 3; bb = i // 3; setf(a, bb, c); setf(bb, a, c)
    i = 0; total = len(out) * 8
    right = size - 1
    while right >= 1:                           # forループ内で変数を書き換えると次の列が重複するため、whileで走査する
        if right == 6: right = 5
        for vert in range(size):
            for j in range(2):
                x = right - j; up = ((right + 1) & 2) == 0; y = size - 1 - vert if up else vert
                if not F[y][x] and i < total: M[y][x] = (out[i >> 3] >> (7 - (i & 7))) & 1 == 1; i += 1
        right -= 2
    masks = [lambda x, y: (x + y) % 2 == 0, lambda x, y: y % 2 == 0, lambda x, y: x % 3 == 0, lambda x, y: (x + y) % 3 == 0,
             lambda x, y: (x // 3 + y // 2) % 2 == 0, lambda x, y: x * y % 2 + x * y % 3 == 0,
             lambda x, y: (x * y % 2 + x * y % 3) % 2 == 0, lambda x, y: ((x + y) % 2 + x * y % 3) % 2 == 0]
    def penalty(G):
        p = 0; pat = [1,0,1,1,1,0,1,0,0,0,0]; rpat = pat[::-1]
        for lines in (G, [list(c) for c in zip(*G)]):
            for row in lines:
                run = 1
                for a in range(1, size):
                    if row[a] == row[a - 1]: run += 1
                    else:
                        if run >= 5: p += 3 + run - 5
                        run = 1
                if run >= 5: p += 3 + run - 5
                s = [1 if c else 0 for c in row]
                for a in range(size - 10):
                    if s[a:a + 11] == pat or s[a:a + 11] == rpat: p += 40
        for y in range(size - 1):
            for x in range(size - 1):
                if G[y][x] == G[y][x + 1] == G[y + 1][x] == G[y + 1][x + 1]: p += 3
        dark = sum(c for r in G for c in r); t = size * size
        return p + (-(-abs(dark * 20 - t * 10) // t) - 1) * 10
    best = None
    for m in ([force] if force is not None else range(8)):
        G = [[M[y][x] ^ (not F[y][x] and masks[m](x, y)) for x in range(size)] for y in range(size)]
        pn = penalty(G)
        if best is None or pn < best[0]: best = (pn, m, G)
    _, m, G = best; M = G; fmt(m)  # 書式情報を選んだマスクで書き直す
    return [[bool(c) for c in r] for r in M], v

def to_png(M, scale=20, border=4):
    n = len(M) + 2 * border; W = n * scale; rows = []
    for y in range(n):
        line = bytearray()
        for x in range(n):
            mx, my = x - border, y - border
            dark = 0 <= mx < len(M) and 0 <= my < len(M) and M[my][mx]
            line += (b"\x00" if dark else b"\xff") * scale
        rows += [b"\x00" + bytes(line)] * scale
    def chunk(t, d): c = struct.pack(">I", len(d)) + t + d; return c + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", W, W, 8, 0, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(b"".join(rows), 9)) + chunk(b"IEND", b"")
def to_svg(M, border=4):
    n = len(M) + 2 * border; d = "".join("M%d,%dh1v1h-1z" % (x + border, y + border) for y, r in enumerate(M) for x, c in enumerate(r) if c)
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" shape-rendering="crispEdges"><rect width="100%%" height="100%%" fill="#fff"/><path d="%s" fill="#000"/></svg>' % (n, n, d)

if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]; ecl = "Q"
    if "--ecl" in sys.argv: ecl = sys.argv[sys.argv.index("--ecl") + 1].upper()
    mask = int(sys.argv[sys.argv.index("--mask") + 1]) if "--mask" in sys.argv else None   # 読み取りにくい端末があれば 0〜7 を試す
    if not a: sys.exit(__doc__)
    url, base = a[0], (a[1] if len(a) > 1 else "qr")
    M, v = make(url, ecl, mask)
    open(base + ".png", "wb").write(to_png(M)); open(base + ".svg", "w").write(to_svg(M))
    print("作成しました: %s.png / %s.svg  (バージョン%d, 誤り訂正%s, %d文字)" % (base, base, v, ecl, len(url)))
