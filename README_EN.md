# xiaozhao-radar

**AI-driven campus recruitment aggregator.**  
Crawls 100+ company career pages (top internet firms + state-owned enterprises) and presents them in a searchable, filterable dashboard. No backend required — runs entirely in the browser.

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()

---

## Why this exists

Campus recruitment information is scattered across 100+ company career pages. Fresh graduates spend hours checking each site manually.  
**xiaozhao-radar** automates the crawl and presents everything in one searchable table with category filters, pagination, and batch import.

## Quick start

### Option A: Firecrawl (no login required)

1. Get a free API key from [Firecrawl](https://www.firecrawl.dev/app/api-keys)
2. Open `xiaozhao-radar.html` in your browser
3. Paste your Firecrawl API key → click **🕷 Crawl**
4. First 20 sites load instantly; remaining sites load in the background

### Option B: BrowserAct CLI (for anti-bot / captcha sites)

```bash
npm install -g browser-act
browser-act login
browser-act stealth-extract "https://join.qq.com/" --out ba_result.json
```

Then click **📤 Import** in the radar page and select `ba_result.json`.

### Option C: OpenCLI xiaozhao adapter (for 51job full database)

```bash
npm install -g @jackwener/opencli
opencli xiaozhao search "2027 校招" -f json > xiaozhao.json
```

Then click **📤 Import** in the radar page and select `xiaozhao.json`.

## Data sources (987 sites)

| Category | Count | Examples |
|----------|-------|----------|
| Corporate career pages | 126 | Tencent, Alibaba, ByteDance, Meituan, Baidu, JD, Huawei, Xiaomi, State Grid, Sinopec, CNPC, China Mobile... |
| Official WeChat accounts | 16 | Huadian, Sinopec Longyuan, SAIC, CSCEC, ByteDance, Tencent IEG, PDD official recruiting accounts |
| New public campus-recruitment nodes (v2.3.0) | 845 | Internet tech (228), banking & finance (81), energy & power (37), heavy equipment (26), FMCG (23), automotive (21), pharma & medical (18), telecom (6), construction (5), petrochemicals (5), logistics (2), agriculture (2), aerospace & defense (2) |
| Job boards | 3 | 51job, Yingjiesheng, GuoPin |

## Features

- **987 pre-configured career sites** — no manual URL entry
- **Batch crawl with Firecrawl** — first 20 sites load immediately, rest in background
- **Pagination** — 20 / 50 / 100 items per page
- **Category filter** — filter by Internet / SOE / Job board
- **Company name display** — shows real company names (Tencent, State Grid), not source domains
- **JSON/CSV import** — bring your own data from any CLI tool
- **Zero backend** — single HTML file, open and use

## Tech stack

- Pure HTML + vanilla JS (no build step)
- Firecrawl API for cloud crawling
- BrowserAct / OpenCLI adapters for protected sites
- LocalStorage for API key persistence

## Roadmap

- [ ] Auto-refresh / scheduled crawl
- [ ] Keyword alert (notify when new positions match)
- [ ] Export to Excel
- [ ] Chrome extension version

## License

Apache 2.0

## Star history

If this tool saves you time, a star is the best support.  
GitHub: https://github.com/jiabaobei/xiaozhao-radar
