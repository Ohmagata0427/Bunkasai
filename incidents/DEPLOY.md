# GitHub Pages で公開する（推奨・無料）

push するだけで、公開とQRコード作成まで自動で行われる（`.github/workflows/pages.yml`）。

## 手順（初回のみ）
1. GitHub で新しいリポジトリを作る。**Public** にする（無料プランの GitHub Pages は公開リポジトリが条件）。名前は推測されにくくする（例：`incidents-k7m2q9x4`）。
2. このフォルダの中身を、そのままリポジトリに push する（`deploy/` は自動生成なので含めない。`.gitignore` 済み）。
   ```
   git init -b main
   git add .
   git commit -m "INCIDENTS"
   git remote add origin https://github.com/＜ユーザー名＞/＜リポジトリ名＞.git
   git push -u origin main
   ```
3. リポジトリの **Settings → Pages → Build and deployment → Source** を **GitHub Actions** にする。
4. **Actions** タブで「Deploy to GitHub Pages」が緑になるのを待つ（1〜2分）。公開URLは `https://＜ユーザー名＞.github.io/＜リポジトリ名＞/`。
5. 同じ実行結果のページの **Artifacts → qr-code** をダウンロードする。公開URL入りの `qr_incidents.png`（印刷用）と `.svg` が入っている。
   - 一度作ればURLは変わらない。以後は文言を直して push するだけで、公開版が更新される（QRの作り直しは不要）。

## 注意
- 公開リポジトリなので、`cases.js` の正解を含め、ソースは誰でも読める。展示用の簡易ゲームという位置づけで、秘密にしたい情報は入れないこと。
- `robots.txt` と `_headers` は GitHub Pages では効かない。検索に出にくくする設定は `index.html` の noindex だけになる。URLを知っている人は誰でも開ける。
- **効果音（`sounds/`）は第三者の素材**。公開（再配布）してよい条件かを、各配布元の利用規約で確認し、`sounds/README.txt` に出典を記録すること。問題があれば、差し替えるか `sounds/` を外す（音なしでも動く）。
- 開催後に取り下げるときは、Settings → Pages で公開を止めるか、リポジトリを削除する。
- 実機（iPhone / Android）で、印刷したQRを読み取って確認すること（下の「本番前チェックリスト」）。

---

# 他のホスティングを使う場合（Cloudflare Pages / Netlify など）

# スマホ公開（案A）：QRコード → 来場者のスマホ内で完結

## 仕組み
- QRコードにはURLだけを入れる。来場者のスマホが、自分の回線で最初に1回だけゲーム一式（約0.4MB）を読み込む。
- 以後のゲーム処理はすべてスマホ内で完結する。成績・回答などは、どこにも送信されない（サーバーへの通信は一切ない）。
- 一度開いたあとは、Service Worker（PWA）がスマホに保存するので、電波が弱い教室でも・機内モードでも遊べる。
- 会場でWi-Fiに接続させる必要はない。

## 1. 公開用フォルダを作る
`python tools/build_deploy.py`  →  `deploy/` ができる（このフォルダの中身だけをアップロードする）。
- 検索エンジンに載らない設定（noindex、robots.txt、`_headers`）入り。
- 公開版では、角タップのデバッグは無効。URL末尾に `#debug` を付けたときだけ開く。
- ゲームの内容（cases.js など）や文言を変えたら、`python tools/make_fonts.py` → `python tools/build_deploy.py` の順に再実行し、再アップロードする。

## 2. HTTPSの静的ホスティングにアップロードする
無料の静的ホスティング（例：Cloudflare Pages、Netlify、GitHub Pages）のいずれかでよい。必要なのは「HTTPSで静的ファイルを配信できること」だけ。
- Service Worker（オフライン動作）はHTTPSでのみ有効。
- URLは推測されにくくする（プロジェクト名に英数字のランダム文字列を含める。例：`incidents-k7m2q9x4`）。
- 検索に出ないだけで、URLを知っている人は誰でも開ける。個人情報は扱っていないので問題ないが、開催後に取り下げる（プロジェクトの削除）。
- ホスティング側にはアクセスログ（IPアドレスなど）が残る場合がある。サービスの規約を確認すること。
- 各サービスの操作画面は変わることがあるので、アップロード手順は各サービスの最新の案内に従う（このPCからは動作確認していない）。

## 3. QRコードを作る
`python tools/make_qr.py https://（公開されたURL） qr_incidents`  →  `qr_incidents.png`（印刷用）と `.svg`
- 既定は誤り訂正Q（汚れや折れに強い）。印刷は一辺3cm以上、周囲の白い余白（4マス分）を切らない。
- 必ず、複数の機種（iPhone、Android）で、印刷したものを読み取って確認する。読み取りにくい機種があれば `--mask 3` のようにマスク番号（0〜7）を変えて作り直す。

## 4. 本番前チェックリスト
1. スマホのWi-Fiをオフにし、モバイル回線だけでQRを読んで開く。
2. 最後まで遊び（事件、失敗演出、現場調査）、誤報告4回の「解雇」も確認する。
3. 機内モードにして、ブラウザを再読み込みしても遊べることを確認する（初回読み込み後）。
4. 修正して再アップロードした場合、来場者のスマホは次にネットにつないで開いたときに新しい版へ更新される。
