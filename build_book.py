#!/usr/bin/env python3
"""Build the book:
  - book/index.html  : shell + JS (no chapter content embedded)
  - book/chapters/   : one .md file per chapter (fetched on demand)

Run:  python build_book.py
"""

import os
import json
import shutil

BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "marked.min.js"), "r", encoding="utf-8") as f:
    MARKED_JS = f.read()

CHAPTERS_DIR = os.path.join(BASE, "Chapters")
OUT_DIR      = os.path.join(BASE, "book")

CHAPTERS = [
    ("preface", "_preface.md",                "Preface: Why This Matters"),
    ("ch01",    "ch01_bitcoin.md",            "Chapter 1: A Comprehensive Introduction to Bitcoin"),
    ("ch02",    "ch02_ethereum.md",           "Chapter 2: The Ethereum Ecosystem"),
    ("ch03",    "ch03_solana.md",             "Chapter 3: The Solana Ecosystem"),
    ("ch04",    "ch04_l1_blockchains.md",     "Chapter 4: L1 Blockchains"),
    ("ch05",    "ch05_custody.md",            "Chapter 5: Custody Fundamentals"),
    ("ch06",    "ch06_market_structure.md",   "Chapter 6: Crypto Market Structure & Trading"),
    ("ch07",    "ch07_defi.md",               "Chapter 7: DeFi"),
    ("ch08",    "ch08_mev.md",                "Chapter 8: MEV"),
    ("ch09",    "ch09_stablecoins_rwas.md",   "Chapter 9: Stablecoins and RWAs"),
    ("ch10",    "ch10_hyperliquid.md",        "Chapter 10: Hyperliquid"),
    ("ch11",    "ch11_nfts.md",               "Chapter 11: Non-Fungible Tokens (NFTs)"),
    ("ch12",    "ch12_governance.md",         "Chapter 12: Governance & Token Economics"),
    ("ch13",    "ch13_depin.md",              "Chapter 13: DePIN"),
    ("ch14",    "ch14_quantum_resistance.md", "Chapter 14: Quantum Resistance"),
    ("ch15",    "ch15_prediction_markets.md", "Chapter 15: Prediction Markets"),
]

# ── Output directories ────────────────────────────────────────────────────────
chapters_out = os.path.join(OUT_DIR, "chapters")
os.makedirs(chapters_out, exist_ok=True)

# ── Copy chapter markdown files ───────────────────────────────────────────────
for slug, filename, _title in CHAPTERS:
    src = os.path.join(CHAPTERS_DIR, filename)
    dst = os.path.join(chapters_out, slug + ".md")
    shutil.copy2(src, dst)

# ── TOC metadata (no content!) ────────────────────────────────────────────────
toc_json = json.dumps(
    [{"slug": slug, "title": title} for slug, _f, title in CHAPTERS],
    ensure_ascii=False,
)

# ── HTML shell ────────────────────────────────────────────────────────────────
HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>How Crypto Actually Works</title>
<script>{MARKED_JS}</script>
<style>
  :root {{
    --bg: #f9f6f1;
    --sidebar-bg: #1a1a2e;
    --sidebar-text: #c8c8d4;
    --sidebar-hover: #e94560;
    --sidebar-active: #e94560;
    --text: #2c2c2c;
    --heading: #1a1a2e;
    --accent: #e94560;
    --link: #0a3d8f;
    --border: #ddd6cb;
    --code-bg: #f0ede8;
    --blockquote-border: #e94560;
    --shadow: rgba(0,0,0,0.08);
    --sidebar-width: 300px;
  }}
  [data-theme="dark"] {{
    --bg: #12121e;
    --sidebar-bg: #0d0d1a;
    --sidebar-text: #a0a0b8;
    --text: #d4d4e0;
    --heading: #e8e8f0;
    --accent: #e94560;
    --link: #6aa3e8;
    --border: #2a2a3e;
    --code-bg: #1e1e30;
    --blockquote-border: #e94560;
    --shadow: rgba(0,0,0,0.3);
  }}

  * {{ box-sizing: border-box; margin: 0; padding: 0; }}

  body {{
    font-family: 'Georgia', serif;
    background: var(--bg);
    color: var(--text);
    display: flex;
    min-height: 100vh;
    transition: background 0.2s, color 0.2s;
  }}

  /* ── Sidebar ── */
  #sidebar {{
    width: var(--sidebar-width);
    background: var(--sidebar-bg);
    display: flex;
    flex-direction: column;
    position: fixed;
    top: 0; left: 0; bottom: 0;
    overflow-y: auto;
    z-index: 100;
    transition: transform 0.3s;
  }}
  #sidebar-header {{
    padding: 28px 20px 20px;
    border-bottom: 1px solid rgba(255,255,255,0.07);
  }}
  #sidebar-header .book-title {{
    font-size: 14px;
    font-weight: 700;
    color: #fff;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    line-height: 1.4;
    margin-bottom: 4px;
  }}
  #sidebar-header .book-subtitle {{
    font-size: 11px;
    color: rgba(255,255,255,0.4);
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }}
  #toc {{
    padding: 12px 0;
    flex: 1;
  }}
  .toc-item {{
    display: block;
    padding: 8px 20px;
    color: var(--sidebar-text);
    cursor: pointer;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    font-size: 13px;
    line-height: 1.4;
    border-left: 3px solid transparent;
    transition: all 0.15s;
    text-decoration: none;
  }}
  .toc-item:hover {{ color: #fff; background: rgba(255,255,255,0.05); }}
  .toc-item.active {{ color: #fff; border-left-color: var(--accent); background: rgba(233,69,96,0.1); }}
  .toc-item.preface {{ font-style: italic; }}
  #sidebar-footer {{
    padding: 16px 20px;
    border-top: 1px solid rgba(255,255,255,0.07);
    font-size: 11px;
    color: rgba(255,255,255,0.3);
    line-height: 1.6;
  }}

  /* ── Main ── */
  #main {{
    margin-left: var(--sidebar-width);
    flex: 1;
    display: flex;
    flex-direction: column;
    min-height: 100vh;
  }}
  #topbar {{
    position: sticky;
    top: 0;
    background: var(--bg);
    border-bottom: 1px solid var(--border);
    padding: 10px 48px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    z-index: 50;
    box-shadow: 0 1px 4px var(--shadow);
  }}
  #chapter-title-bar {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    font-size: 13px;
    color: var(--accent);
    font-weight: 600;
    letter-spacing: 0.03em;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 600px;
  }}
  #controls {{
    display: flex;
    gap: 8px;
    align-items: center;
    flex-shrink: 0;
  }}
  .btn {{
    background: none;
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 5px 12px;
    font-size: 12px;
    cursor: pointer;
    color: var(--text);
    font-family: -apple-system, sans-serif;
    transition: all 0.15s;
  }}
  .btn:hover {{ background: var(--border); }}
  #font-size-display {{
    font-size: 12px;
    color: var(--text);
    font-family: -apple-system, sans-serif;
    min-width: 30px;
    text-align: center;
  }}

  /* ── Loading indicator ── */
  #loading {{
    display: none;
    text-align: center;
    padding: 80px 48px;
    color: var(--accent);
    font-family: -apple-system, sans-serif;
    font-size: 14px;
    letter-spacing: 0.05em;
  }}
  #loading.visible {{ display: block; }}

  /* ── Content ── */
  #content {{
    max-width: 760px;
    margin: 0 auto;
    padding: 56px 48px 80px;
    width: 100%;
    overflow-wrap: break-word;
    word-break: break-word;
  }}
  #content h1 {{
    font-size: 2em;
    color: var(--heading);
    margin-bottom: 0.3em;
    line-height: 1.2;
    font-weight: 700;
  }}
  #content h2 {{
    font-size: 1.35em;
    color: var(--heading);
    margin-top: 2em;
    margin-bottom: 0.6em;
    padding-bottom: 0.3em;
    border-bottom: 1px solid var(--border);
    font-weight: 700;
  }}
  #content h3 {{
    font-size: 1.1em;
    color: var(--heading);
    margin-top: 1.5em;
    margin-bottom: 0.4em;
    font-weight: 700;
  }}
  #content h4 {{
    font-size: 0.85em;
    color: var(--heading);
    margin-top: 1.2em;
    margin-bottom: 0.3em;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.04em;
  }}
  #content p {{
    line-height: 1.8;
    margin-bottom: 1.1em;
    font-size: 1em;
  }}
  #content ul, #content ol {{
    margin: 0.8em 0 1em 1.4em;
    line-height: 1.8;
  }}
  #content li {{ margin-bottom: 0.3em; }}
  #content li p {{ margin-bottom: 0.2em; }}
  #content a {{ color: var(--link); text-decoration: none; }}
  #content a:hover {{ text-decoration: underline; }}
  #content strong {{ color: var(--heading); font-weight: 700; }}
  #content em {{ font-style: italic; }}
  #content code {{
    background: var(--code-bg);
    padding: 0.1em 0.4em;
    border-radius: 4px;
    font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
    font-size: 0.85em;
  }}
  #content pre {{
    background: var(--code-bg);
    padding: 1.2em;
    border-radius: 8px;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    white-space: pre;
    margin: 1.2em 0;
    border: 1px solid var(--border);
  }}
  #content pre code {{ background: none; padding: 0; font-size: 0.88em; }}
  #content blockquote {{
    border-left: 4px solid var(--blockquote-border);
    padding: 0.6em 1.2em;
    margin: 1.2em 0;
    background: var(--code-bg);
    border-radius: 0 6px 6px 0;
    font-style: italic;
    color: #666;
  }}
  [data-theme="dark"] #content blockquote {{ color: #999; }}
  #content table {{
    display: block;
    width: 100%;
    border-collapse: collapse;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    white-space: nowrap;
    margin: 1.2em 0;
    font-size: 0.92em;
    font-family: -apple-system, sans-serif;
  }}
  #content th {{
    background: var(--heading);
    color: var(--bg);
    padding: 8px 12px;
    text-align: left;
    font-size: 0.82em;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    white-space: normal;
    min-width: 80px;
  }}
  #content td {{
    padding: 8px 12px;
    border-bottom: 1px solid var(--border);
    white-space: normal;
    min-width: 80px;
  }}
  #content tr:hover td {{ background: var(--code-bg); }}
  #content hr {{
    border: none;
    border-top: 1px solid var(--border);
    margin: 2em 0;
  }}

  /* ── Navigation footer ── */
  #nav-footer {{
    display: flex;
    justify-content: space-between;
    padding: 24px 48px 40px;
    max-width: 760px;
    margin: 0 auto;
    width: 100%;
    gap: 16px;
  }}
  .nav-btn {{
    background: none;
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 12px 20px;
    font-size: 13px;
    cursor: pointer;
    color: var(--text);
    font-family: -apple-system, sans-serif;
    transition: all 0.15s;
    text-align: left;
    max-width: 45%;
    line-height: 1.4;
  }}
  .nav-btn:hover {{ background: var(--code-bg); border-color: var(--accent); }}
  .nav-btn .direction {{ font-size: 11px; color: var(--accent); text-transform: uppercase; letter-spacing: 0.08em; display: block; margin-bottom: 4px; }}
  .nav-btn.next {{ text-align: right; margin-left: auto; }}
  .nav-btn:disabled {{ opacity: 0.3; cursor: default; }}
  .nav-btn:disabled:hover {{ background: none; border-color: var(--border); }}

  /* ── License banner ── */
  #license-banner {{
    background: var(--sidebar-bg);
    color: rgba(255,255,255,0.6);
    text-align: center;
    padding: 16px 24px;
    font-size: 12px;
    font-family: -apple-system, sans-serif;
    line-height: 1.6;
  }}
  #license-banner a {{ color: var(--accent); text-decoration: none; }}

  /* ── Mobile ── */
  #hamburger {{
    display: none;
    background: none;
    border: none;
    font-size: 26px;
    cursor: pointer;
    color: var(--text);
    padding: 8px;
    min-width: 44px;
    min-height: 44px;
    line-height: 1;
  }}
  #overlay {{
    display: none;
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.5);
    z-index: 90;
  }}

  @media (max-width: 768px) {{
    #sidebar {{ transform: translateX(-100%); min-width: unset; }}
    #sidebar.open {{ transform: translateX(0); }}
    #overlay.open {{ display: block; }}
    #main {{ margin-left: 0; }}

    #topbar {{
      padding: 6px 12px;
      gap: 8px;
      flex-wrap: nowrap;
    }}
    #chapter-title-bar {{
      font-size: 12px;
      max-width: 140px;
    }}
    #controls {{ gap: 4px; }}
    .btn {{
      padding: 6px 8px;
      font-size: 13px;
      min-width: 36px;
      min-height: 36px;
    }}
    #font-size-display {{ min-width: 20px; font-size: 13px; }}

    #content {{ padding: 24px 16px 60px; }}
    #content h1 {{ font-size: 1.5em; }}
    #content h2 {{ font-size: 1.2em; }}
    #content p {{ font-size: 1em; line-height: 1.75; }}

    #nav-footer {{
      padding: 12px 16px 32px;
      gap: 10px;
    }}
    .nav-btn {{
      max-width: 48%;
      padding: 10px 12px;
      font-size: 12px;
    }}

    #hamburger {{ display: flex; align-items: center; justify-content: center; }}
  }}
</style>
</head>
<body>

<div id="overlay" onclick="closeSidebar()"></div>

<nav id="sidebar">
  <div id="sidebar-header">
    <div class="book-title">How Crypto Actually Works</div>
    <div class="book-subtitle">The Missing Manual</div>
  </div>
  <div id="toc"></div>
  <div id="sidebar-footer">
    By Larry Cermak &amp; co-authors<br>
    CC BY-NC-ND 4.0 &mdash; Free to read &amp; share
  </div>
</nav>

<div id="main">
  <div id="topbar">
    <button id="hamburger" onclick="toggleSidebar()">&#9776;</button>
    <div id="chapter-title-bar"></div>
    <div id="controls">
      <button class="btn" onclick="changeFont(-1)">A&#8722;</button>
      <span id="font-size-display">18</span>
      <button class="btn" onclick="changeFont(1)">A+</button>
      <button class="btn" id="theme-btn" onclick="toggleTheme()">Dark</button>
    </div>
  </div>

  <div id="loading">Loading&hellip;</div>
  <div id="content"></div>

  <div id="nav-footer">
    <button class="nav-btn prev" id="btn-prev" onclick="navigate(-1)">
      <span class="direction">&#8592; Previous</span>
      <span id="prev-title"></span>
    </button>
    <button class="nav-btn next" id="btn-next" onclick="navigate(1)">
      <span class="direction">Next &#8594;</span>
      <span id="next-title"></span>
    </button>
  </div>

  <div id="license-banner">
    <strong>How Crypto Actually Works</strong> by Larry Cermak, Igor Igamberdiev &amp; Bohdan Pavlov &mdash;
    Licensed under <a href="https://creativecommons.org/licenses/by-nc-nd/4.0/" target="_blank">CC BY-NC-ND 4.0</a>.
    Free to read and share with attribution. Not for commercial use. No derivatives.
  </div>
</div>

<script>
const chapters = {toc_json};

let currentIndex = 0;
let fontSize = 18;
const cache = {{}};

// Build TOC
const toc = document.getElementById('toc');
chapters.forEach((ch, i) => {{
  const a = document.createElement('div');
  a.className = 'toc-item' + (i === 0 ? ' preface' : '');
  a.textContent = ch.title;
  a.onclick = () => {{ loadChapter(i); closeSidebar(); }};
  a.id = 'toc-' + i;
  toc.appendChild(a);
}});

async function loadChapter(index) {{
  currentIndex = index;
  const ch = chapters[index];

  // Show loading, hide content
  document.getElementById('loading').classList.add('visible');
  document.getElementById('content').innerHTML = '';

  // Fetch markdown (use cache to avoid re-fetching)
  if (!cache[ch.slug]) {{
    try {{
      const res = await fetch('chapters/' + ch.slug + '.md');
      if (!res.ok) throw new Error('HTTP ' + res.status);
      cache[ch.slug] = await res.text();
    }} catch (e) {{
      document.getElementById('loading').classList.remove('visible');
      document.getElementById('content').innerHTML =
        '<p style="color:var(--accent);padding:2em 0">Failed to load chapter. Please refresh.</p>';
      return;
    }}
  }}

  document.getElementById('loading').classList.remove('visible');
  document.getElementById('content').innerHTML = marked.parse(cache[ch.slug]);
  document.getElementById('chapter-title-bar').textContent = ch.title;

  window.scrollTo({{ top: 0 }});

  document.querySelectorAll('.toc-item').forEach((el, i) => {{
    el.classList.toggle('active', i === index);
  }});

  const prev = document.getElementById('btn-prev');
  const next = document.getElementById('btn-next');
  if (index > 0) {{
    prev.disabled = false;
    document.getElementById('prev-title').textContent = chapters[index - 1].title;
  }} else {{
    prev.disabled = true;
    document.getElementById('prev-title').textContent = '';
  }}
  if (index < chapters.length - 1) {{
    next.disabled = false;
    document.getElementById('next-title').textContent = chapters[index + 1].title;
  }} else {{
    next.disabled = true;
    document.getElementById('next-title').textContent = '';
  }}

  history.replaceState(null, '', '#' + ch.slug);
  document.title = ch.title + ' \u2014 How Crypto Actually Works';
}}

function navigate(dir) {{
  const next = currentIndex + dir;
  if (next >= 0 && next < chapters.length) loadChapter(next);
}}

function changeFont(delta) {{
  fontSize = Math.max(14, Math.min(24, fontSize + delta));
  document.getElementById('content').style.fontSize = fontSize + 'px';
  document.getElementById('font-size-display').textContent = fontSize;
}}

function toggleTheme() {{
  const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
  document.documentElement.setAttribute('data-theme', isDark ? '' : 'dark');
  document.getElementById('theme-btn').textContent = isDark ? 'Dark' : 'Light';
  localStorage.setItem('theme', isDark ? '' : 'dark');
}}

function toggleSidebar() {{
  document.getElementById('sidebar').classList.toggle('open');
  document.getElementById('overlay').classList.toggle('open');
}}
function closeSidebar() {{
  document.getElementById('sidebar').classList.remove('open');
  document.getElementById('overlay').classList.remove('open');
}}

// Restore theme
const savedTheme = localStorage.getItem('theme') || '';
if (savedTheme) {{
  document.documentElement.setAttribute('data-theme', savedTheme);
  document.getElementById('theme-btn').textContent = 'Light';
}}

// Load chapter from hash or default
const hash = location.hash.slice(1);
const startIndex = hash ? Math.max(0, chapters.findIndex(c => c.slug === hash)) : 0;
loadChapter(startIndex);
</script>
</body>
</html>
"""

out_html = os.path.join(OUT_DIR, "index.html")
with open(out_html, "w", encoding="utf-8") as f:
    f.write(HTML)

print(f"Built: {out_html}")
print(f"       {out_html.replace('index.html', 'chapters/')}  ({len(CHAPTERS)} .md files)")
