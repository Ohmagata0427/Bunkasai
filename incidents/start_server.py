#!/usr/bin/env python3
"""INCIDENTS をローカルネットワーク内だけで配信する簡易サーバー（標準ライブラリのみ・インターネット不要）。
使い方: このフォルダで  python start_server.py   （Windowsは start_server.bat をダブルクリック）
スマホをPCと同じWi-Fi（またはPCのモバイルホットスポット）につなぎ、表示されたURLを開く。 止めるときは Ctrl+C。"""
import http.server, socket, os, sys, functools

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
ROOT = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):                      # 修正がすぐ反映されるよう、キャッシュさせない
        self.send_header("Cache-Control", "no-store")
        super().end_headers()
    def log_message(self, fmt, *a):
        sys.stderr.write("  %s  %s\n" % (self.client_address[0], fmt % a))

def lan_ips():
    ips = set()
    try:                                        # 実際には通信せず、使われる経路のIPだけを調べる
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); s.connect(("10.255.255.255", 1)); ips.add(s.getsockname()[0]); s.close()
    except OSError:
        pass
    try:
        ips.update(socket.gethostbyname_ex(socket.gethostname())[2])
    except OSError:
        pass
    return sorted(i for i in ips if not i.startswith("127."))

if __name__ == "__main__":
    handler = functools.partial(Handler, directory=ROOT)
    with http.server.ThreadingHTTPServer(("0.0.0.0", PORT), handler) as srv:
        print("\nINCIDENTS ローカルサーバー起動（このフォルダだけを同じネットワーク内に公開します）")
        print("  PC   : http://localhost:%d/" % PORT)
        for ip in lan_ips():
            print("  スマホ: http://%s:%d/        デバッグ付き: http://%s:%d/#debug" % (ip, PORT, ip, PORT))
        print("\n※ 信頼できるWi-Fi（自宅・会場の専用回線）でのみ使ってください。止める: Ctrl+C\n")
        try:
            srv.serve_forever()
        except KeyboardInterrupt:
            print("\n停止しました。")
