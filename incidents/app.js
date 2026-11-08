(() => {
  "use strict";
  let hard = false;                       // ハードモード（開始画面で選ぶ）
  const MAX_W_NORMAL = 4, MAX_W_HARD = 3; // この回数目の誤報告で任務失敗
  const maxW = () => hard ? MAX_W_HARD : MAX_W_NORMAL;
  const HARD_MULT = 1.5, RANK_PENALTY = 10; // ハード：スコア倍率／並べ替えを間違えるたびの減点
  const REDUCED = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  const $ = id => document.getElementById(id);
  const C = window.CASES;
  let ci = 0, found = new Set(), rejected = new Set(), done = false, W = 0, t0 = 0, tick = null;
  let rankMiss = 0, rankOrder = [];
  let state = "start", curDoc = null, total = { B: 0, A: 0, S: 0, T: 0 }, toastT = null;

  function show(n) {
    state = n;
    ["start", "intro", "office", "doc", "arg", "rank", "result"].forEach(s => $(s).hidden = s !== n);
    $("fired").hidden = n !== "fired";
    $("trap").hidden = true; $("trap").textContent = ""; hideCutIn();
    if (n !== "fired") { stopSound(peeSnd, 0); peeSnd = null; }
    $("tbTitle").textContent = "INCIDENTS — 調査端末";
    $("bar").hidden = !(n === "office" || n === "doc");
    $("backBtn").hidden = n !== "doc";
    if (n === "start") drawBoard($("startBoard"), { mode: "normal", clear: true });
    window.scrollTo(0, 0);
  }
  const elapsed = () => Math.floor((Date.now() - t0) / 1000);
  function hud() {
    $("time").textContent = elapsed();
    $("count").textContent = found.size;
    $("total").textContent = (C[ci] && C[ci].answer) ? C[ci].answer.length : 0;
    $("wrong").textContent = W + " / " + maxW();
  }
  function say(msg, ok) {
    const t = $("toast"); t.textContent = msg; t.className = ok === "info" ? "info" : ok ? "ok" : ""; t.hidden = false;
    clearTimeout(toastT); toastT = setTimeout(() => t.hidden = true, 4500);
  }

  function startCase() {
    const c = C[ci];
    if (c.type === "arg") return startArg(c);
    found = new Set(); rejected = new Set(); done = false; W = 0; rankMiss = 0; t0 = Date.now();
    $("caseTitle").textContent = (hard ? "【HARD】" : "") + c.title;
    buildRoom(c);
    clearInterval(tick); tick = setInterval(hud, 500);
    hud(); show("office");
  }

  let roomT = [];
  function buildRoom(c) {
    roomT.forEach(clearTimeout); roomT = [];
    const room = $("room"); room.className = c.scene || "office"; room.dataset.theme = c.theme || c.scene || "office"; room.textContent = "";
    $("hint1").textContent = c.hint || "";
    (c.spots || []).forEach(sp => {
      const b = document.createElement("button");
      b.type = "button"; b.className = "spot s-" + sp.doc; b.dataset.title = sp.title || sp.label; b.style.cssText = sp.pos;
      const sm = document.createElement("small"); sm.textContent = sp.sub;
      const lb = document.createElement("span"); lb.className = "lbl"; lb.textContent = sp.label;
      b.append(lb, document.createElement("br"), sm);
      b.addEventListener("click", () => { b.classList.remove("pulse"); openDoc(sp.doc); });
      if (sp.delay) { // 時間差で現れる調査対象（操作は妨げない）
        b.hidden = true;
        roomT.push(setTimeout(() => { b.hidden = false; b.classList.add("pulse"); say("通知が届きました。"); }, sp.delay * 1000));
      }
      room.appendChild(b);
    });
  }

  function openDoc(key) {
    const d = C[ci].docs[key]; curDoc = key;
    $("docTitle").textContent = d.title;
    $("docMeta").textContent = d.meta;
    const body = $("docBody"); body.textContent = "";
    body.classList.toggle("ref", !!d.ref); $("doc").classList.toggle("is-ref", !!d.ref);
    $("docHint").hidden = false;
    $("docHint").textContent = d.ref ? "参照資料です。報告の対象ではありません。他の資料と見比べる基準として読んでください。" : "";
    if (!d.ref) { $("docHint").textContent = ""; $("docHint").append("問題だと思う行を長押し"); const kb = document.createElement("span"); kb.className = "hint-kb"; kb.textContent = "（キーボードはEnter長押し）"; $("docHint").append(kb, "すると報告します。"); }
    if (d.ref) { // 手順書などの参照資料：報告はできない（長押しの処理を付けない）
      d.lines.forEach(l => { const r = document.createElement("div"); r.className = "refline"; r.dataset.id = l.id; r.textContent = l.t; r.addEventListener("pointerdown", () => say("参照資料です。報告の対象ではありません。", "info")); body.appendChild(r); });
    } else d.lines.forEach(l => {
      const b = document.createElement("button");
      b.type = "button"; b.dataset.id = l.id;
      b.className = "line" + (d.type === "log" ? " log" : "") + (found.has(l.id) ? " found" : "") + (rejected.has(l.id) ? " rejected" : "");
      b.textContent = l.t;
      attachHold(b, l.id);
      body.appendChild(b);
    });
    if (d.trap) { // 罠：通知の「確認する」を開いてしまうと、ブラクラ風ポップアップが暴走して任務失敗
      const row = document.createElement("div"); row.className = "trapRow";
      const tb = document.createElement("button"); tb.type = "button"; tb.className = "trapBtn"; tb.textContent = d.trap;
      tb.addEventListener("click", trapPopups); row.appendChild(tb); body.appendChild(row);
    }
    show("doc");
  }

  // ---- 効果音（sounds/ のmp3。file://でも動くようHTMLAudioで再生）----
  const SND_FILES = { noise: "sounds/sfx-noise.mp3", hold: "sounds/sfx-hold.mp3", pee: "sounds/sfx-pee.mp3", open: "sounds/sfx-open.mp3", ok: "sounds/sfx-ok.mp3", ng: "sounds/sfx-ng.mp3" };
  const SND = {}; let soundOn = true, unlocked = false, noiseSnd = null, peeSnd = null;
  Object.keys(SND_FILES).forEach(k => { const a = new Audio(SND_FILES[k]); a.preload = "auto"; SND[k] = a; });
  function unlockAudio() { // 最初の操作で一度だけ、無音で再生→停止して再生許可を得る（iOS対策）
    if (unlocked) return; unlocked = true;
    Object.values(SND).forEach(a => { a.muted = true; const p = a.play(); const done = () => { a.pause(); a.currentTime = 0; a.muted = false; }; if (p && p.then) p.then(done, () => { a.muted = false; unlocked = false; }); else done(); });
  }
  ["pointerdown", "keydown", "touchstart"].forEach(ev => document.addEventListener(ev, unlockAudio, { capture: true, passive: true }));
  function play(name, opt) {
    if (!soundOn || !SND[name]) return null; opt = opt || {};
    const a = opt.clone ? SND[name].cloneNode(true) : SND[name];
    a.volume = opt.vol == null ? 1 : opt.vol; try { a.currentTime = 0; } catch (e) {}
    const p = a.play(); if (p && p.catch) p.catch(() => {}); window.__log && __log("sound " + name); return a;
  }
  function stopSound(a, ms) {
    if (!a) return; if (!ms) { a.pause(); try { a.currentTime = 0; } catch (e) {} return; }
    let v = a.volume; const step = v / 5, iv = setInterval(() => { v -= step; if (v <= 0.02) { clearInterval(iv); a.pause(); try { a.currentTime = 0; } catch (e) {} a.volume = 1; } else a.volume = v; }, ms / 5);
  }
  $("soundBtn").addEventListener("click", () => {
    soundOn = !soundOn; $("soundBtn").textContent = "音：" + (soundOn ? "ON" : "OFF"); $("soundBtn").setAttribute("aria-pressed", String(soundOn));
    if (!soundOn) Object.values(SND).forEach(a => a.pause());
  });

  // ---- 報告の演出（点→円が広がり一周→警告アイコン）----
  const FX = (() => {
    const box = $("fx"), ring = box.querySelector(".fx-ring"); let t = null; const R0 = 24, R1 = 44;
    return {
      start(x, y) { clearTimeout(t); box.style.left = x + "px"; box.style.top = y + "px"; box.className = "on"; this.set(0); },
      set(p) { ring.style.strokeDasharray = (p * 100).toFixed(1) + " 100"; }, // 円の大きさは変えず、一周する弧だけが伸びる
      cancel() { box.className = ""; },
      done() { box.className = "on done"; clearTimeout(t); t = setTimeout(() => { box.className = ""; }, 1400); }
    };
  })();

  // ---- 誤報告が上限に達したときの失敗演出 ----
  // 画面の歪み → 侵入ログ（情報送出）→ 砂嵐 → 画面が消える → 解雇通知書
  const LITE = /iPhone|iPad|iPod/.test(navigator.userAgent) || (navigator.maxTouchPoints > 1 && /Mac/.test(navigator.platform));
  function glitch(ms) {
    if (REDUCED) return;
    const disp = $("glDisp"), turb = $("glTurb"), els = [$("bar"), document.querySelector("main")], t0 = performance.now();
    els.forEach(e => { e.classList.add("glitching"); if (LITE) e.classList.add("lite"); });
    (function f() {
      const k = (performance.now() - t0) / ms;
      if (k >= 1) { els.forEach(e => e.classList.remove("glitching", "lite")); disp.setAttribute("scale", "0"); return; }
      disp.setAttribute("scale", (Math.random() < 0.65 ? Math.random() * 80 * (0.4 + k) : 0).toFixed(1));
      turb.setAttribute("baseFrequency", "0 " + (0.02 + Math.random() * 0.12).toFixed(3));
      setTimeout(f, 55);
    })();
  }
  const VLOG = [
    ["[03:41:07] 未登録プロセス svc_update.exe を検知"], ["[03:41:07] 権限昇格 ............ 成功"], ["[03:41:08] 監査ログの停止 ...... 成功"],
    ["[03:41:09] 203.0.113.58:443 へ接続"], ["[03:41:10] 保管データを外部へ送信中", 1], ["[03:41:12] 送信完了。情報漏洩を確認", 1]
  ];
  function runTerminal(ms) {
    const term = $("vterm"), log = $("vlog"), bar = $("vbar"), pct = $("vpct"), t0 = performance.now();
    log.textContent = ""; bar.style.transition = "none"; bar.style.width = "0"; pct.textContent = "0%"; term.hidden = false;
    requestAnimationFrame(() => requestAnimationFrame(() => { bar.style.transition = "width " + ms + "ms cubic-bezier(.4,0,.6,1)"; bar.style.width = "100%"; }));
    VLOG.forEach((l, i) => setTimeout(() => { const sp = document.createElement("span"); if (l[1]) sp.className = "bad"; sp.textContent = l[0] + "\n"; log.appendChild(sp); }, 250 + i * (ms * 0.72) / VLOG.length));
    const iv = setInterval(() => { const k = Math.min(1, (performance.now() - t0) / ms); pct.textContent = Math.round(k * 100) + "%"; if (k >= 1) clearInterval(iv); }, 60);
  }
  function runNoise(ms, cb) {
    const cv = $("noise"), ctx = cv.getContext("2d");
    const w = cv.width = Math.ceil(innerWidth / 3), h = cv.height = Math.ceil(innerHeight / 3);
    const img = ctx.createImageData(w, h), d = img.data;
    const draw = () => { for (let i = 0; i < d.length; i += 4) { const v = 25 + Math.random() * 150; d[i] = d[i + 1] = d[i + 2] = v; d[i + 3] = 255; } ctx.putImageData(img, 0, 0); };
    cv.hidden = false;
    if (REDUCED) { draw(); setTimeout(cb, ms); return; } // 動きを減らす設定：静止ノイズ
    let last = 0; const t0 = performance.now();
    const loop = t => { if (t - last > 70) { draw(); last = t; } if (t - t0 < ms) requestAnimationFrame(loop); else cb(); };
    requestAnimationFrame(loop);
  }
  function showFired() {
    const n = new Date(), ds = n.getFullYear() + "年" + (n.getMonth() + 1) + "月" + n.getDate() + "日";
    $("firedDate").textContent = ds; $("firedDay").textContent = ds;
    show("fired"); peeSnd = play("pee"); // 解雇通知書が出たとき、3秒の「ピー」を流す
    $("firedBtns").hidden = true; setTimeout(() => { $("firedBtns").hidden = false; }, 3900);
  }
  // ---- 通知トラップ：ブラクラ風ポップアップ12連発 → 解雇通知書へ直行 ----
  const TRAP_MSG = [["警告", "お使いのPCはウイルスに感染しています"], ["システムエラー", "不審なプログラムを検知しました (0x80070057)"], ["セキュリティ警告", "個人情報が外部に送信されています"],
    ["重要", "今すぐ対処してください"], ["ウイルスに感染しました", "3つの脅威が見つかりました"], ["システム", "このPCは保護されていません"], ["警告", "アカウント情報が流出しました"],
    ["確認", "本当に閉じますか？"], ["エラー", "応答がありません"], ["警告", "ファイルが暗号化されています"], ["セキュリティ", "不正アクセスを検知しました"], ["ウイルス警告", "今すぐ削除してください"]];
  function trapPopups() {
    if (done) return;
    done = true; clearInterval(tick); state = "virus"; $("toast").hidden = true; $("tbTitle").textContent = "INCIDENTS — 応答なし";
    const layer = $("trap"); layer.textContent = ""; layer.hidden = false; window.__log && __log("TRAP fired");
    const add = i => {
      play("open", { clone: true, vol: 0.85 });
      const w = document.createElement("div"); w.className = "trap-win";
      const bar = document.createElement("div"); bar.className = "tw-bar"; bar.append(TRAP_MSG[i][0], Object.assign(document.createElement("span"), { textContent: "×" }));
      const body = document.createElement("div"); body.className = "tw-body"; body.textContent = TRAP_MSG[i][1];
      const ok = document.createElement("button"); ok.type = "button"; ok.className = "tw-ok"; ok.textContent = "OK"; body.appendChild(ok);
      w.append(bar, body); w.style.left = (Math.random() * Math.max(10, innerWidth - 300)) + "px"; w.style.top = (40 + Math.random() * Math.max(10, innerHeight - 190)) + "px";
      layer.appendChild(w);
    };
    if (REDUCED) { TRAP_MSG.forEach((_, i) => add(i)); setTimeout(showFired, 1800); return; }
    let i = 0; const iv = setInterval(() => { add(i++); if (i >= TRAP_MSG.length) { clearInterval(iv); setTimeout(showFired, 800); } }, 190);
  }

  function failMission() {
    done = true; clearInterval(tick); state = "virus"; $("toast").hidden = true;
    const v = $("virus");
    setTimeout(() => { $("tbTitle").textContent = "INCIDENTS — 応答なし"; v.hidden = false; v.className = ""; requestAnimationFrame(() => v.classList.add("on")); glitch(900); }, 700);
    setTimeout(() => { play("open"); runTerminal(2300); }, 1600);
    setTimeout(() => {
      $("vterm").hidden = true; v.classList.add("noisy"); noiseSnd = play("noise");
      runNoise(2000, () => {
        v.classList.add("collapse");
        setTimeout(() => { v.hidden = true; v.className = ""; $("noise").hidden = true; stopSound(noiseSnd, 0); showFired(); }, REDUCED ? 50 : 600);
      });
    }, 4000);
  }

  // ---- 長押しで報告 ----
  const HOLD_MS = 900;
  function attachHold(b, id) {
    let timer = null, raf = 0, t1 = 0, holdSnd = null;
    const reset = (cancelFx = true) => { clearTimeout(timer); cancelAnimationFrame(raf); if (timer && cancelFx) { FX.cancel(); stopSound(holdSnd, 70); } timer = null; b.classList.remove("holding"); };
    const begin = (x, y) => {
      if (timer || done || b.classList.contains("found") || b.classList.contains("rejected")) return;
      t1 = performance.now(); b.classList.add("holding"); FX.start(x, y); holdSnd = play("hold");
      const step = () => { FX.set(Math.min(1, (performance.now() - t1) / HOLD_MS)); raf = requestAnimationFrame(step); };
      raf = requestAnimationFrame(step);
      timer = setTimeout(() => { reset(false); FX.done(); report(id, b); }, HOLD_MS);
    };
    b.addEventListener("pointerdown", e => { if (e.button === 0 || e.pointerType !== "mouse") begin(e.clientX, e.clientY); });
    ["pointerup", "pointercancel", "pointerleave", "blur"].forEach(ev => b.addEventListener(ev, () => reset()));
    b.addEventListener("contextmenu", e => e.preventDefault());
    b.addEventListener("keydown", e => { if ((e.key === "Enter" || e.key === " ") && !e.repeat) { e.preventDefault(); e.stopPropagation(); const r = b.getBoundingClientRect(); begin(r.left + Math.min(r.width / 2, 200), r.top + r.height / 2); } });
    b.addEventListener("keyup", e => { if (e.key === "Enter" || e.key === " ") reset(); });
  }
  // 報告成功のカットイン（画面中央に SUCCESS。操作の邪魔にならないよう、クリックは素通しする）
  let cutT = null;
  function cutIn() {
    const e = $("cutin"); clearTimeout(cutT); e.hidden = false; e.classList.remove("go"); void e.offsetWidth; e.classList.add("go");
    cutT = setTimeout(hideCutIn, 1050);
  }
  function hideCutIn() { const e = $("cutin"); clearTimeout(cutT); e.hidden = true; e.classList.remove("go"); }
  function report(id, b) {
    if (done) return;
    const c = C[ci];
    if (c.answer.includes(id)) {
      found.add(id); b.classList.add("found"); hud(); play("ok"); cutIn(); window.__log && __log("report OK " + id);
      if (found.size === c.answer.length) {
        done = true;
        if (hard && rankable(c)) { say("すべての問題点を報告しました。最後に優先度を判定してください。", true); setTimeout(() => startRank(c), 1100); }
        else { say("すべての問題点を報告しました。調査を終了します。", true); setTimeout(() => success(c), 1100); }
      }
      else say("報告を受理しました。（" + found.size + " / " + c.answer.length + "）調査を続けてください。", true);
    } else {
      if (!rejected.has(id)) { rejected.add(id); W++; }
      b.classList.add("rejected"); hud(); play("ng"); window.__log && __log("report NG " + id + " W=" + W);
      if (W >= maxW()) return failMission();
      say("この記録だけでは、問題と判断できません。（誤報告 " + W + " / " + maxW() + "）" + (W === maxW() - 1 ? " あと1回の誤報告で任務失敗です。" : ""));
    }
  }

  function shuffled(a) { const r = a.slice(); for (let i = r.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [r[i], r[j]] = [r[j], r[i]]; } return r; }
  const el = (tag, cls, text) => { const e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; };
  const KIND = { "兆候": "k-sign", "脆弱性": "k-vuln", "不備": "k-flaw" };
  const LEGEND = [["兆候", "実際に起きた可能性を示す記録（侵害の証明ではありません）"], ["脆弱性", "悪用され得る弱点"], ["不備", "ルールや運用の不備"]];
  function lineText(c, id) { let t = ""; Object.values(c.docs).forEach(d => d.lines.forEach(l => { if (l.id === id) t = l.t; })); return t; }
  function renderFindings(parent, c) {
    const sec = el("div", "findings"), head = el("div", "fhead");
    head.appendChild(el("h3", null, "特定した問題点（" + c.answer.length + "件・深刻度の高い順）"));
    const all = el("button", "ghost", "すべて開く"); all.type = "button"; head.appendChild(all); sec.appendChild(head);
    const setters = [];
    const ORDER = { "兆候": 0, "脆弱性": 1, "不備": 2 };
    const ids = c.answer.slice().sort((x, y) => (ORDER[c.kinds[x]] ?? 9) - (ORDER[c.kinds[y]] ?? 9));
    ids.forEach((id, i) => {
      const kind = c.kinds[id] || "", box = el("div", "finding " + (KIND[kind] || "")), row = el("div", "frow");
      row.appendChild(el("span", "badge " + (KIND[kind] || ""), kind));
      row.appendChild(el("span", "ftext", lineText(c, id)));
      const btn = el("button", "toggle", "解説を開く"); btn.type = "button"; btn.setAttribute("aria-expanded", "false");
      const panel = el("div", "fdetail", c.detail[id] || ""); panel.id = "fd-" + ci + "-" + i; panel.hidden = true; btn.setAttribute("aria-controls", panel.id);
      const set = o => { panel.hidden = !o; btn.setAttribute("aria-expanded", String(o)); btn.textContent = o ? "解説を閉じる" : "解説を開く"; };
      btn.addEventListener("click", () => set(panel.hidden));
      row.appendChild(btn); box.appendChild(row); box.appendChild(panel); sec.appendChild(box); setters.push(set);
    });
    let open = false;
    all.addEventListener("click", () => { open = !open; setters.forEach(f => f(open)); all.textContent = open ? "すべて閉じる" : "すべて開く"; });
    const lg = el("div", "legend");
    LEGEND.forEach(([k, d]) => { const p = el("p", "lg"); p.appendChild(el("span", "badge " + KIND[k], k)); p.appendChild(document.createTextNode(d)); lg.appendChild(p); });
    sec.appendChild(lg); parent.appendChild(sec);
    if (c.caution && c.caution.length) { const cw = el("div", "caution"); cw.appendChild(el("h3", null, "断定できないこと")); c.caution.forEach(t => cw.appendChild(el("p", null, t))); parent.appendChild(cw); }
    parent.appendChild(el("p", "small", "出典・注記：" + c.source));
  }


  // ---- ハードモード：優先度の並べ替え（深刻度＝兆候→脆弱性→不備。同じ種類どうしの順序は問わない）----
  const SEV = { "兆候": 0, "脆弱性": 1, "不備": 2 };
  const sev = (c, id) => SEV[c.kinds[id]] ?? 9;
  const rankable = c => !!c.kinds && new Set(c.answer.map(id => sev(c, id))).size > 1;
  const rankValid = (c, order) => order.every((id, i) => i === 0 || sev(c, order[i - 1]) <= sev(c, id));
  function startRank(c) {
    clearInterval(tick);
    let o = shuffled(c.answer), n = 0;
    while (rankValid(c, o) && n++ < 30) o = shuffled(c.answer); // 最初から正しい並びにはしない
    rankOrder = o; $("rankMsg").textContent = ""; drawRank(c); show("rank");
  }
  function drawRank(c) {
    const ol = $("rankList"); ol.textContent = "";
    rankOrder.forEach((id, i) => {
      const li = el("li", "rank-item"); li.append(el("span", "rank-no", String(i + 1)), el("span", "rank-text", lineText(c, id)));
      const bt = el("span", "rank-btns");
      [["▲", -1, "上へ"], ["▼", 1, "下へ"]].forEach(([ch, d, lb]) => {
        const b = el("button", null, ch); b.type = "button"; b.setAttribute("aria-label", (i + 1) + "番目を" + lb); b.disabled = i + d < 0 || i + d >= rankOrder.length;
        b.addEventListener("click", () => { [rankOrder[i], rankOrder[i + d]] = [rankOrder[i + d], rankOrder[i]]; $("rankMsg").textContent = ""; drawRank(c); });
        bt.appendChild(b);
      });
      li.appendChild(bt); ol.appendChild(li);
    });
  }
  function submitRank() {
    const c = C[ci];
    if (state !== "rank") return;
    if (rankValid(c, rankOrder)) { $("rankMsg").textContent = ""; say("優先度の判定が完了しました。調査を終了します。", true); success(c); return; }
    rankMiss++; window.__log && __log("rank NG " + rankMiss);
    $("rankMsg").textContent = "順序が正しくありません。実際に起きた可能性を示す記録ほど、上に置いてください。（誤り " + rankMiss + " 回・1回につき " + RANK_PENALTY + " 点減点）";
  }

  function success(c) {
    clearInterval(tick);
    const T = elapsed(), perfect = W === 0;
    const base = Math.max(0, 100 + (perfect ? 50 : 0) - 2 * T - 20 * W); // 暫定式
    const S = hard ? Math.max(0, Math.round(base * HARD_MULT) - RANK_PENALTY * rankMiss) : base;
    total.B++; total.A += perfect ? 1 : 0; total.S += S; total.T += T;
    $("resTitle").textContent = "";
    const r = $("resBody"); r.textContent = "";
    const h = document.createElement("div"); h.className = "break"; h.textContent = "特定（IDENTIFIED）"; r.appendChild(h);
    r.appendChild(stats((hard ? [["モード", "HARD"]] : []).concat([["経過", T + "秒"], ["誤報告", W + "件"]], hard ? [["並べ替えの誤り", rankMiss + "回"]] : [], [["今回のスコア", S], ["累計", total.S]])));
    if (c.kinds && c.detail) renderFindings(r, c);
    else {
      const card = document.createElement("div"); card.className = "card";
      const h3 = document.createElement("h3"); h3.textContent = c.kinds ? "特定した問題点" : "解説"; card.appendChild(h3);
      if (c.kinds) {
        c.answer.forEach(id => { let t = ""; Object.values(c.docs).forEach(d => d.lines.forEach(l => { if (l.id === id) t = l.t; }));
          const p = document.createElement("p"); const k = document.createElement("b"); k.textContent = "【" + (c.kinds[id] || "") + "】"; p.appendChild(k); p.appendChild(document.createTextNode(t)); card.appendChild(p); });
        const g = document.createElement("p"); g.className = "small"; g.textContent = "脆弱性＝悪用され得る弱点／不備＝ルールや運用の不備／兆候＝実際に起きた可能性を示す記録（侵害の証明ではありません）"; card.appendChild(g);
        const h4 = document.createElement("h3"); h4.textContent = "解説"; card.appendChild(h4); }
      c.explain.forEach(t => { const p = document.createElement("p"); p.textContent = t; card.appendChild(p); });
      const s = document.createElement("p"); s.className = "small"; s.textContent = "出典・注記：" + c.source; card.appendChild(s);
      r.appendChild(card);
    }
    const last = ci === C.length - 1;
    $("nextBtn").textContent = last ? "最終結果へ" : "次の事件へ";
    show("result");
  }

  // ---- 現場調査（ARG）ステージ ----
  let skipAsk = false, skipT = null;
  function startArg(c) {
    clearInterval(tick); roomT.forEach(clearTimeout); skipAsk = false;
    $("argIntro").textContent = c.intro;
    $("skipBtn").textContent = "スキップ（Webだけで進める）";
    show("arg"); showArgFinal();   // 確認コードは廃止。開始と同時に最終問題（穴埋め）へ
  }
  // 穴埋め：空欄（スロット）をタップ→選択肢（チップ）をタップで入れる。入れたものは再タップで戻せる。
  const BLANK = "＿＿＿＿＿＿＿＿";
  let clozeActive = null;
  function setActive(b) { if (clozeActive) clozeActive.classList.remove("active"); clozeActive = b; if (b) b.classList.add("active"); }
  function clearSlot(b) { if (b._chip) { b._chip.disabled = false; b._chip = null; } b.dataset.val = ""; b.textContent = BLANK; b.classList.remove("filled"); }
  function fillSlot(b, chip) { b.dataset.val = chip.dataset.val; b.textContent = chip.dataset.val; b.classList.add("filled"); chip._slot = b; b._chip = chip; chip.disabled = true; }
  function touchRow(b) { const r = b.closest(".arg-question"); if (r) r.classList.remove("ok", "ng"); $("argFinalMsg").textContent = ""; }
  function makeSlot(type, label) {
    const b = el("button", "cloze-slot", BLANK); b.type = "button"; b.dataset.type = type; b.dataset.val = ""; b.setAttribute("aria-label", label + "の空欄");
    b.addEventListener("click", () => { touchRow(b); if (b.classList.contains("filled")) { clearSlot(b); setActive(b); } else setActive(clozeActive === b ? null : b); });
    return b;
  }
  function makeChip(type, text) {
    const b = el("button", "chip", text); b.type = "button"; b.dataset.type = type; b.dataset.val = text;
    b.addEventListener("click", () => {
      const slots = [...$("argQuestions").querySelectorAll(".cloze-slot")];
      const t = (clozeActive && clozeActive.dataset.type === type && !clozeActive.classList.contains("filled")) ? clozeActive : slots.find(x => x.dataset.type === type && !x.classList.contains("filled"));
      if (!t) return; touchRow(t); fillSlot(t, b); setActive(null);
    });
    return b;
  }
  function showArgFinal() {
    const c = C[ci], rows = c.final.rows, dc = (hard && c.final.decoys) || c.decoys || {};
    setActive(null);
    const host = $("argQuestions"); host.textContent = "";
    rows.forEach((r, i) => {
      const row = el("div", "arg-question"), p1 = el("p", "arg-question-prompt"), p2 = el("p", "arg-risk-line");
      p1.append(r.place + "「", makeSlot("incident", "発見した事象 " + (i + 1)), "」");
      p2.append("危険性：「", makeSlot("risk", "危険性 " + (i + 1)), "」");
      row.append(p1, p2); host.appendChild(row);
    });
    const bank = $("argBank"); bank.textContent = "";
    const groups = [["incident", "選択肢（発見した事象）", rows.map(r => r.incident).concat(hard ? (dc.incident || []) : [])],
                    ["risk", "選択肢（危険性）", rows.map(r => r.risk).concat(hard ? (dc.risk || []) : [])]];
    groups.forEach(([type, title, list]) => {
      const g = el("div", "chip-group"), row = el("div", "chip-row");
      shuffled(list).forEach(v => row.appendChild(makeChip(type, v)));
      g.append(el("h3", null, title), row); bank.appendChild(g);
    });
    $("argFinalMsg").textContent = "";
    window.scrollTo(0, 0);
  }
  function submitArgFinal() {
    const c = C[ci], host = $("argQuestions"), rows = [...host.querySelectorAll(".arg-question")];
    if (!rows.length || [...host.querySelectorAll(".cloze-slot")].some(x => !x.dataset.val)) { $("argFinalMsg").textContent = "すべての空欄を埋めてください。"; return; }
    let ok = 0;
    rows.forEach((row, i) => {
      const [a, b] = row.querySelectorAll(".cloze-slot"), good = a.dataset.val === c.final.rows[i].incident && b.dataset.val === c.final.rows[i].risk;
      if (good) ok++;
      if (!hard) { row.classList.toggle("ok", good); row.classList.toggle("ng", !good); } // ハードは行ごとの正誤を見せない
    });
    if (ok < rows.length) {
      $("argFinalMsg").textContent = hard ? "対応が正しくありません。教室で確認した事象と、その危険性を見直してください。"
        : ok + " / " + rows.length + " 組が正しい対応です。色が赤い行を見直してください。";
      return;
    }
    $("argFinalMsg").textContent = "正解です。現場調査を完了しました。";
    argDone(c, false);
  }
  function skipCase() {
    if (!skipAsk) {
      skipAsk = true; $("skipBtn").textContent = "本当にスキップしますか？ もう一度押すと確定";
      clearTimeout(skipT); skipT = setTimeout(() => { skipAsk = false; $("skipBtn").textContent = "スキップ（Webだけで進める）"; }, 4000);
      return;
    }
    argDone(C[ci], true);
  }
  function argDone(c, skipped) {
    total.arg = skipped ? "SKIP" : "CLEAR";
    const S = skipped ? 0 : Math.round(c.final.rows.length * 50 * (hard ? HARD_MULT : 1)); total.S += S;
    const r = $("resBody"); r.textContent = "";
    const h = document.createElement("div"); h.className = "break"; h.textContent = skipped ? "SKIP" : "FIELD CLEAR"; r.appendChild(h);
    const card = document.createElement("div"); card.className = "card";
    if (skipped) {
      const p = document.createElement("p"); p.textContent = "現場調査はスキップされました。得点はありません。"; card.appendChild(p);
    } else {
      r.appendChild(stats((hard ? [["モード", "HARD"]] : []).concat([["正解", c.final.rows.length + "組"], ["今回のスコア", S], ["累計", total.S]])));
      const p = document.createElement("p"); p.textContent = c.notice; card.appendChild(p);
    }
    r.appendChild(card);
    $("nextBtn").textContent = ci === C.length - 1 ? "最終結果へ" : "次の事件へ";
    show("result");
  }

  function stats(a) {
    const d = document.createElement("div"); d.className = "stat";
    a.forEach(([k, v]) => { const s = document.createElement("span"); s.textContent = k + "："; const b = document.createElement("b"); b.textContent = v; s.appendChild(b); d.appendChild(s); });
    return d;
  }


  // ---- スコアランキング（この端末のブラウザ内にだけ保存。通常／ハードは別の表）----
  const RK_KEY = "incidents.ranking.v1", RK_SHOW = 10, RK_KEEP = 200;
  let rkMem = null; // localStorageが使えない環境では、このページを開いている間だけ保持する
  function rkLoad() {
    try { const a = JSON.parse(localStorage.getItem(RK_KEY) || "[]"); rkMem = Array.isArray(a) ? a : []; }
    catch (e) { rkMem = rkMem || []; }
    return rkMem.filter(x => x && typeof x.score === "number");
  }
  function rkSave(list) {
    rkMem = list.slice(0, RK_KEEP);
    try { localStorage.setItem(RK_KEY, JSON.stringify(rkMem)); return true; } catch (e) { return false; }
  }
  const rkSort = a => a.slice().sort((x, y) => y.score - x.score || x.time - y.time || x.at - y.at);
  const rkMode = (list, mode) => rkSort(list.filter(x => !!x.hard === (mode === "hard")));
  function drawBoard(host, o) {
    o = o || {}; let mode = o.mode || "normal";
    const render = () => {
      host.textContent = "";
      const head = el("div", "bd-head"); head.appendChild(el("h2", null, "スコアランキング"));
      const tabs = el("div", "bd-tabs");
      [["normal", "通常"], ["hard", "ハード"]].forEach(([m, t]) => {
        const b = el("button", "bd-tab" + (m === mode ? " on" : ""), t); b.type = "button"; b.setAttribute("aria-pressed", String(m === mode));
        b.addEventListener("click", () => { mode = m; render(); }); tabs.appendChild(b);
      });
      head.appendChild(tabs); host.appendChild(head);
      const rows = rkMode(rkLoad(), mode), top = rows.slice(0, RK_SHOW);
      const tbl = el("table", "rk"), thead = el("thead"), hr = el("tr");
      ["順位", "名前", "スコア", "時間"].forEach(t => hr.appendChild(el("th", null, t))); thead.appendChild(hr); tbl.appendChild(thead);
      const tb = el("tbody");
      if (!top.length) { const tr = el("tr", "empty"), td = el("td", null, "まだ記録がありません。"); td.colSpan = 4; tr.appendChild(td); tb.appendChild(tr); }
      top.forEach((x, i) => {
        const tr = el("tr", x.at === o.hi && !!x.hard === (mode === "hard") ? "me" : "");
        tr.append(el("td", "no", String(i + 1)), el("td", "nm", x.name || "名無し"), el("td", "sc", String(x.score)), el("td", "tm", x.time + "秒")); tb.appendChild(tr);
      });
      tbl.appendChild(tb);
      const wrap = el("div", "rk-wrap"); wrap.appendChild(tbl); host.appendChild(wrap);
      host.appendChild(el("p", "small bd-note", "この端末のブラウザにだけ保存されます（ほかの人のスマホとは共有されません）。上位" + RK_SHOW + "件を表示。同点は、時間の短い順です。"));
      if (o.clear && rows.length) {
        let ask = false, t = null; const cb = el("button", "ghost bd-clear", "この端末の記録を消去"); cb.type = "button";
        cb.addEventListener("click", () => {
          if (!ask) { ask = true; cb.textContent = "本当に消去しますか？ もう一度押すと確定"; clearTimeout(t); t = setTimeout(() => { ask = false; cb.textContent = "この端末の記録を消去"; }, 4000); return; }
          rkSave([]); render();
        }); host.appendChild(cb);
      }
    };
    render();
    return { redraw(hi, m) { o.hi = hi; if (m) mode = m; render(); } };
  }
  function addRanking(host) {
    const mode = hard ? "hard" : "normal", score = total.S, time = total.T;
    const box = el("div", "rk-form card"), msg = el("p", null, "");
    const before = rkMode(rkLoad(), mode).filter(x => x.score > score || (x.score === score && x.time <= time)).length + 1;
    msg.append("あなたのスコア ", Object.assign(el("b", null, String(score)), {}), " 点は、現在 ", el("b", null, before + "位"), " です。名前を登録するとランキングに載ります。");
    const row = el("div", "rk-row"), inp = el("input"); inp.type = "text"; inp.maxLength = 8; inp.id = "rkName"; inp.placeholder = "ニックネーム（8文字まで）"; inp.autocomplete = "off"; inp.setAttribute("aria-label", "ニックネーム");
    const bt = el("button", "primary", "登録する"); bt.type = "button";
    row.append(inp, bt); box.append(msg, row, el("p", "small", "本名や学校名などは入れず、ニックネームにしてください。"));
    host.appendChild(box);
    const bh = el("div", "board"); host.appendChild(bh);
    const bd = drawBoard(bh, { mode });
    const go = () => {
      if (bt.disabled) return;
      const e = { name: (inp.value.trim() || "名無し").slice(0, 8), score, time, hard, at: Date.now() };
      const ok = rkSave(rkLoad().concat([e])); bt.disabled = true; inp.disabled = true;
      const pos = rkMode(rkLoad(), mode).findIndex(x => x.at === e.at) + 1;
      box.textContent = ""; box.appendChild(el("p", null, "登録しました。" + (pos ? pos + "位です。" : "") + (ok ? "" : "（この環境では保存できないため、このページを閉じると消えます。）")));
      bd.redraw(e.at, mode);
    };
    bt.addEventListener("click", go);
    inp.addEventListener("keydown", e => { if (e.key === "Enter" && !e.isComposing) { e.preventDefault(); go(); } });
  }

  function next() {
    if (state !== "result") return;
    if (ci < C.length - 1) { ci++; startCase(); return; }
    $("resBody").textContent = "";
    const h = document.createElement("div"); h.className = "break"; h.textContent = "REPORT"; $("resBody").appendChild(h);
    $("resBody").appendChild(stats([["モード", hard ? "HARD" : "通常"], ["特定した事件", total.B + "/" + C.filter(x => x.type !== "arg").length], ["誤報告なしで特定", total.A], ["現場調査", total.arg || "-"], ["合計時間", total.T + "秒"], ["総スコア", total.S]]));
    addRanking($("resBody"));
    $("nextBtn").textContent = "最初から";
    ci = C.length; // 最終画面マーク
  }

  $("nextBtn").addEventListener("click", () => {
    if (ci >= C.length) { ci = 0; total = { B: 0, A: 0, S: 0, T: 0 }; show("start"); } else next();
  });
  function begin(h) { hard = h; $("introMaxW").textContent = maxW() + "回目で任務失敗"; ci = 0; total = { B: 0, A: 0, S: 0, T: 0 }; show("intro"); }
  $("startBtn").addEventListener("click", () => begin(false));
  $("startHardBtn").addEventListener("click", () => begin(true));
  $("rankSubmit").addEventListener("click", submitRank);
  $("introBtn").addEventListener("click", startCase);
  $("retryBtn").addEventListener("click", startCase);
  $("homeBtn").addEventListener("click", () => { ci = 0; total = { B: 0, A: 0, S: 0, T: 0 }; show("start"); });
  $("backBtn").addEventListener("click", () => show("office"));
  document.addEventListener("keydown", e => {
    if (e.key !== "Enter" || e.repeat) return;
    if (e.target && /^(INPUT|TEXTAREA|SELECT)$/.test(e.target.tagName)) return;
    if (state === "start") { e.preventDefault(); $("startBtn").click(); }
    else if (state === "intro") { e.preventDefault(); $("introBtn").click(); }
    else if (state === "result") { e.preventDefault(); $("nextBtn").click(); }
  });
  $("argFinalSubmit").addEventListener("click", submitArgFinal);
  $("skipBtn").addEventListener("click", skipCase);
  window.__game = {
    get state() { return state; }, get ci() { return ci; }, get W() { return W; }, get found() { return [...found]; }, get cases() { return C.length; },
    answers: () => (C[ci] && C[ci].answer) || [],
    goCase(i) { clearInterval(tick); ["virus", "fired", "noise"].forEach(id => { $(id).hidden = true; }); $("virus").className = ""; $("toast").hidden = true; done = false; total = { B: 0, A: 0, S: 0, T: 0 }; ci = i; startCase(); },
    get hard() { return hard; }, toggleHard() { hard = !hard; return hard; }, rank() { if (C[ci] && C[ci].answer && !done) { done = true; C[ci].answer.forEach(id => found.add(id)); hud(); rankable(C[ci]) ? startRank(C[ci]) : success(C[ci]); } },
    trap() { if (!done && state === "doc") trapPopups(); },
    wrong() { if (state === "doc" && !done) { W++; hud(); if (W >= maxW()) failMission(); else say("（デバッグ）誤報告 " + W + " / " + maxW()); } },
    fail() { if (!done) failMission(); },
    result() { if (C[ci] && C[ci].answer && !done) { done = true; C[ci].answer.forEach(id => found.add(id)); hud(); success(C[ci]); } }
  };
  show("start");
})();
