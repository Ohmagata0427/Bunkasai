/* スマホ用デバッグパネル。 #debug を付けて開く、または画面左上の隅を素早く5回タップで表示/非表示。 */
(() => {
  "use strict";
  const logs = [], MAX = 300;
  const fmt = a => a.map(x => { try { return typeof x === "string" ? x : (x instanceof Error ? x.stack || x.message : JSON.stringify(x)); } catch (e) { return String(x); } }).join(" ");
  let view = null;
  const push = (lv, a) => { const t = new Date().toTimeString().slice(0, 8); logs.push("[" + t + "] " + lv + " " + fmt(a)); if (logs.length > MAX) logs.shift(); if (view) { view.textContent = logs.join("\n"); view.scrollTop = view.scrollHeight; } };
  window.__log = (...a) => push("G", a);
  ["log", "info", "warn", "error"].forEach(k => { const o = console[k]; console[k] = (...a) => { push(k === "error" ? "E" : k === "warn" ? "W" : "L", a); o.apply(console, a); }; });
  window.addEventListener("error", e => push("E", [e.message + " @" + (e.filename || "").split("/").pop() + ":" + e.lineno]));
  window.addEventListener("unhandledrejection", e => push("E", ["Promise: " + (e.reason && e.reason.message || e.reason)]));

  let panel = null, reveal = false, ptype = "-", maxTouch = 0;
  const $ = id => document.getElementById(id);
  document.addEventListener("pointerdown", e => { ptype = e.pointerType; if (e.pointerType === "touch") document.documentElement.classList.add("touch"); }, true);
  if (navigator.maxTouchPoints > 0) document.documentElement.classList.add("touch");
  document.addEventListener("touchstart", e => { maxTouch = Math.max(maxTouch, e.touches.length); }, true);

  function info() {
    const g = window.__game || {};
    return ["state=" + g.state, "case=" + (g.ci + 1) + "/" + (g.cases || "?"), "発見=" + (g.found || []).length + " 誤報告=" + g.W,
      "viewport=" + innerWidth + "x" + innerHeight + " dpr=" + devicePixelRatio, "pointer=" + ptype + " maxTouch=" + maxTouch + " coarse=" + matchMedia("(pointer: coarse)").matches,
      "reducedMotion=" + matchMedia("(prefers-reduced-motion: reduce)").matches, "UA=" + navigator.userAgent.slice(0, 90)].join("\n");
  }
  function applyReveal() {
    document.querySelectorAll(".line").forEach(l => { const g = window.__game; l.classList.toggle("dbg-answer", !!(reveal && g && g.answers().includes(l.dataset.id))); });
  }
  setInterval(() => { if (reveal) applyReveal(); }, 300);

  function build() {
    panel = document.createElement("div"); panel.id = "dbg";
    const head = document.createElement("div"); head.className = "dbg-head";
    const infoEl = document.createElement("pre"); infoEl.className = "dbg-info";
    view = document.createElement("pre"); view.className = "dbg-log"; view.textContent = logs.join("\n");
    const row = document.createElement("div"); row.className = "dbg-btns";
    const btn = (t, f) => { const b = document.createElement("button"); b.type = "button"; b.textContent = t; b.addEventListener("click", () => { try { f(b); } catch (e) { push("E", [e]); } refresh(); }); row.appendChild(b); return b; };
    const g = () => window.__game;
    (window.CASES || []).forEach((c, i) => btn("事件" + (i + 1), () => g().goCase(i)));
    btn("正解を表示", b => { reveal = !reveal; b.textContent = reveal ? "正解を隠す" : "正解を表示"; applyReveal(); });
    btn("ハード切替", b => { b.textContent = g().toggleHard() ? "ハード中" : "ハード切替"; });
    btn("並べ替えへ", () => g().rank());
    btn("誤報告+1", () => g().wrong());
    btn("失敗演出", () => g().fail());
    btn("トラップ発動", () => g().trap());
    btn("結果へ", () => g().result());
    btn("ログ消去", () => { logs.length = 0; view.textContent = ""; });
    btn("コピー", b => { const t = info() + "\n---\n" + logs.join("\n"); (navigator.clipboard ? navigator.clipboard.writeText(t) : Promise.reject()).then(() => { b.textContent = "コピー済"; }, () => { const r = document.createRange(); r.selectNodeContents(view); const s = getSelection(); s.removeAllRanges(); s.addRange(r); b.textContent = "ログを選択"; }); });
    btn("閉じる", () => toggle(false));
    head.textContent = "DEBUG"; panel.append(head, row, infoEl, view); document.body.appendChild(panel);
    panel._info = infoEl;
  }
  function refresh() { if (panel && !panel.hidden) panel._info.textContent = info(); }
  function toggle(on) {
    if (!panel) build();
    panel.hidden = on === undefined ? !panel.hidden : !on;
    if (!panel.hidden) { refresh(); view.scrollTop = view.scrollHeight; }
    document.body.classList.toggle("dbg-on", !panel.hidden);
  }
  setInterval(refresh, 1000);
  const hashOn = () => { if (/^#debug/.test(location.hash)) toggle(true); };
  window.addEventListener("hashchange", hashOn);
  document.addEventListener("DOMContentLoaded", hashOn);
  // 左上の隅（56px四方）を2秒以内に5回タップ
  let taps = [];
  document.addEventListener("pointerdown", e => {
    if (window.INCIDENTS_CONFIG && INCIDENTS_CONFIG.debugTap === false) return; // 公開版では角タップを無効化（#debug だけ有効）
    if (e.clientX > 56 || e.clientY > 56) return;
    const n = Date.now(); taps = taps.filter(t => n - t < 2000); taps.push(n);
    if (taps.length >= 5) { taps = []; toggle(); }
  }, true);
  window.__debugToggle = toggle;
})();
