/* ================================================================
   pqdi.cc hover tooltips (shared across all guide pages)
   ------------------------------------------------------------------
   Two kinds of links:

   1. ITEMS — loot items carry data-pqdi-id on an <a href="https://www.pqdi.cc/item/<id>">.
      On hover we fetch pqdi.cc's own pre-rendered tooltip HTML —
      /get-item-tooltip/<id>, the same endpoint their site uses, which is
      CORS-open (it echoes our Origin back) — sanitize it, absolutize its
      relative URLs, and show it in a fixed panel.

   2. SPELLS — boss spells carry data-pqdi-spell on an <a href="https://www.pqdi.cc/spell/<id>">.
      PQDI has no pre-rendered spell tooltip endpoint, so we fetch the JSON API
      (/api/v1/spell/<id>, also CORS-open) and render name + effects + meta ourselves.

   Both are cached per id; desktop only (hover:hover + pointer:fine); mobile keeps
   the plain new-tab link. Offline / unknown id → no tooltip.

   Adapted from Axiom-DKP2 (js/app.js "pqdi.cc item tooltip" section).
   ================================================================ */
(function () {
  "use strict";
  if (!window.matchMedia("(hover: hover) and (pointer: fine)").matches) return; // desktop only

  const PQDI_BASE = "https://www.pqdi.cc";
  const tipCache = new Map(); // kind+id -> sanitized HTML string
  let tipSeq = 0;             // bumped on every hide — invalidates in-flight fetches
  let tipActiveLink = null;

  const tipEl = document.createElement("div");
  tipEl.className = "item-tooltip";
  tipEl.id = "pqdi-item-tip";
  tipEl.hidden = true;
  document.body.appendChild(tipEl);

  /** Strip anything executable from third-party tooltip HTML and absolutize its URLs. */
  function sanitizePqdiHtml(html) {
    const doc = new DOMParser().parseFromString(html, "text/html");
    const drop = new Set(["script", "style", "iframe", "object", "embed", "link", "meta",
      "form", "input", "button", "select", "textarea"]);
    for (const el of [...doc.body.querySelectorAll("*")]) {
      if (drop.has(el.tagName.toLowerCase())) { el.remove(); continue; }
      for (const attr of [...el.attributes]) {
        const n = attr.name.toLowerCase();
        if (n.startsWith("on")) el.removeAttribute(attr.name);
        else if ((n === "href" || n === "src") && /^\s*javascript:/i.test(attr.value)) el.removeAttribute(attr.name);
      }
    }
    // Relative URLs → absolute pqdi.cc (icon sprites, currency icons, /spell/ links).
    doc.querySelectorAll("img[src]").forEach((im) => { im.src = new URL(im.getAttribute("src"), PQDI_BASE).href; });
    doc.querySelectorAll("a[href]").forEach((a) => {
      a.href = new URL(a.getAttribute("href"), PQDI_BASE).href;
      a.target = "_blank";
      a.rel = "noopener noreferrer";
    });
    // Inline style sprites: url(/static/iconss/…) → absolute.
    doc.querySelectorAll("[style]").forEach((el) =>
      el.setAttribute("style", el.getAttribute("style").split("url(/").join(`url(${PQDI_BASE}/`)));
    return doc.body.innerHTML;
  }

  /** Render a spell's JSON (from /api/v1/spell/<id>) into tooltip HTML. */
  function renderSpellTip(data) {
    const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    let html = `<h4 class="spell-tip-title">${esc(data.name || "Spell")}</h4>`;
    if (Array.isArray(data.effects) && data.effects.length) {
      html += '<ul class="spell-tip-effects">' +
        data.effects.map((e) => `<li>${esc(e)}</li>`).join("") + "</ul>";
    }
    const meta = [];
    if (data.recast_time) meta.push(`Recast: ${Math.round(data.recast_time)}s`);
    if (data.target_type) meta.push(`Target: ${data.target_type}`);
    if (data.resist_type) meta.push(`Resist: ${data.resist_type}`);
    if (data.duration && data.duration !== "Instant") meta.push(`Duration: ${data.duration}`);
    if (meta.length) html += `<p class="spell-tip-meta">${esc(meta.join(" · "))}</p>`;
    return html;
  }

  /** Position a fixed hover panel next to its anchor link (flip left when it would overflow). */
  function positionHoverTip(link) {
    const r = link.getBoundingClientRect();
    const tw = tipEl.offsetWidth, th = tipEl.offsetHeight;
    let x = r.right + 8; // right of the link…
    if (x + tw > window.innerWidth - 8) x = Math.max(8, r.left - tw - 8); // …flip left when it would overflow
    const y = Math.min(Math.max(8, r.top), Math.max(8, window.innerHeight - th - 8));
    tipEl.style.left = `${x}px`;
    tipEl.style.top = `${y}px`;
  }

  /** Scroll behavior: follow the anchor as it moves; hide only when the anchor leaves the viewport. */
  const onScroll = () => {
    if (!tipActiveLink || tipEl.hidden) return;
    const r = tipActiveLink.getBoundingClientRect();
    if (r.bottom < 0 || r.top > window.innerHeight) hideTip(); // anchor scrolled out of view
    else positionHoverTip(tipActiveLink);
  };

  async function showTip(link) {
    const itemId = link.dataset.pqdiId;
    const spellId = link.dataset.pqdiSpell;
    if (!/^\d+$/.test(itemId || "") && !/^\d+$/.test(spellId || "")) return;
    const kind = spellId ? "spell" : "item";
    const id = (kind === "spell" ? spellId : itemId);
    const seq = ++tipSeq;
    tipActiveLink = link;
    tipEl.hidden = false;
    tipEl.innerHTML = '<div class="item-tip-loading">Loading…</div>';
    positionHoverTip(link);
    let html = tipCache.get(kind + ":" + id);
    if (!html) {
      try {
        const url = kind === "spell" ? `${PQDI_BASE}/api/v1/spell/${id}` : `${PQDI_BASE}/get-item-tooltip/${id}`;
        const res = await fetch(url, { cache: "no-cache" });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        html = kind === "spell" ? renderSpellTip(await res.json()) : sanitizePqdiHtml(await res.text());
        tipCache.set(kind + ":" + id, html);
      } catch (err) {
        if (seq === tipSeq && tipActiveLink === link) hideTip(); // unknown id / offline → no tooltip
        return;
      }
    }
    if (seq !== tipSeq || tipActiveLink !== link) return; // user moved on while fetching
    tipEl.innerHTML = html;
    positionHoverTip(link); // reposition with the final size
  }

  function hideTip() {
    tipSeq++; // invalidate any in-flight fetch
    tipActiveLink = null;
    if (tipEl) { tipEl.hidden = true; tipEl.innerHTML = ""; }
  }

  const findLink = (e) => e.target.closest ? e.target.closest("[data-pqdi-id], [data-pqdi-spell]") : null;

  document.addEventListener("mouseover", (e) => {
    const link = findLink(e);
    if (!link || link === tipActiveLink) return;
    hideTip();
    showTip(link);
  });
  document.addEventListener("mouseout", (e) => {
    if (!tipActiveLink) return;
    const stays = e.relatedTarget && tipActiveLink.contains(e.relatedTarget);
    if (!stays) hideTip(); // entering another link re-shows via its mouseover
  });
  // Keyboard parity: Tab to a link shows the tooltip, blur hides it.
  document.addEventListener("focusin", (e) => {
    const link = findLink(e);
    if (!link || link === tipActiveLink) return;
    hideTip();
    showTip(link);
  });
  document.addEventListener("focusout", (e) => {
    if (!tipActiveLink) return;
    const next = e.relatedTarget && e.relatedTarget.closest ? findLink(e) : null;
    if (next !== tipActiveLink) hideTip(); // focus moved elsewhere (another link re-shows via its focusin)
  });
  window.addEventListener("scroll", onScroll, true);
  window.addEventListener("resize", hideTip);
})();
