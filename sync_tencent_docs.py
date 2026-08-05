# -*- coding: utf-8 -*-
"""
校招雷达 · 腾讯文档智能表格 → jobs.json 同步脚本
=================================================
数据链路（已验证，2026-08-04 完成对接）：
  腾讯文档智能表格「27届实习提前批信息汇总」
    https://docs.qq.com/smartsheet/DTkRMUVhoUWJXZEhJ
    └─ 核心两个子表(sheet)：
        tTNjGc 「27届内推汇总」      (~100 条)
        tvVDZj 「实习提前批每日更新」 (~1600 条)

读取通道（破解 opendoc 接口，无需登录/无需代理）：
  GET https://docs.qq.com/dop-api/opendoc?id=DTkRMUVhoUWJXZEhJ&subId=<sheetId>&startrow=0&endrow=N
  └─ 返回 JSONP → clientVars.collab_client_vars.initialAttributedText.text[0].smartsheet
        └─ base64 → zlib raw deflate 解压 → JSON（rows[0]=[meta,data]）
              └─ meta.c.k3.k3 字段定义 / data.c.k2.k1 记录值

输出：仓库根目录 jobs.json  ——  GitHub Pages(jiabaobei.github.io/xiaozhao-radar/jobs.json)
      以 Access-Control-Allow-Origin:* 提供，页面(含本地双击 HTML)自动跨域读取最新数据。

用法：
  python sync_tencent_docs.py            # 仅生成本地 jobs.json（不推送）
  python sync_tencent_docs.py --push     # 生成并提交 + push 到 GitHub main
  python sync_tencent_docs.py --dry      # 仅打印统计，不写文件
"""

import sys, os, re, json, base64, zlib, urllib.request, urllib.parse, subprocess, datetime

# ============ 配置 ============
TD_PAD_ID = "DTkRMUVhoUWJXZEhJ"
TD_REF    = "https://docs.qq.com/smartsheet/DTkRMUVhoUWJXZEhJ"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"

# (子表ID, 名称, 拉取条数上限)
SHEETS = [
    ("tTNjGc", "27届内推汇总", 200),
    ("tvVDZj", "实习提前批每日更新", 2000),
]
PAGE_SIZE = 300

CITY_LIST = ["北京","上海","广州","深圳","成都","杭州","武汉","南京","重庆","西安","苏州","天津",
             "长沙","郑州","青岛","东莞","佛山","宁波","无锡","厦门","福州","济南","合肥","昆明",
             "大连","哈尔滨","沈阳","长春","石家庄","太原","南昌","贵阳","南宁","海口","兰州",
             "银川","西宁","呼和浩特","乌鲁木齐","拉萨"]

# ============ 网络 ============
def fetch_sheet_raw(sheet_id, rows):
    """请求 opendoc 接口，返回解压后的 JSON 字符串（腾讯文档表格数据）。"""
    params = {
        "u":"", "noEscape":"1", "enableSmartsheetSplit":"1", "supportOptimizedVer":"4",
        "chunkCellSize":"15000", "normal":"1", "outformat":"1", "wb":"1", "nowb":"0",
        "callback":"x", "xsrf":"", "id":TD_PAD_ID, "subId":sheet_id,
        "startrow":"0", "endrow":str(rows),
    }
    url = "https://docs.qq.com/dop-api/opendoc?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={
        "User-Agent": UA, "Referer": TD_REF, "Accept": "*/*",
    })
    with urllib.request.urlopen(req, timeout=40) as resp:
        text = resp.read().decode("utf-8", "ignore")
    # 去 JSONP 包装：clientVarsCallback({...})
    m = re.match(r"^[^(]*\((.*)\)\s*;?\s*$", text, re.S)
    if not m:
        raise RuntimeError("JSONP 解析失败")
    data = json.loads(m.group(1))
    ccv = data.get("clientVars", {}).get("collab_client_vars", {})
    iat = ccv.get("initialAttributedText", {})
    t = (iat.get("text") or [None])[0]
    if not t or not t.get("smartsheet"):
        raise RuntimeError("无数据字段(smartsheet)")
    b64 = t["smartsheet"].replace("\n", "").replace("\r", "").replace(" ", "")
    raw = base64.b64decode(b64 + "=" * (-len(b64) % 4))  # 补 padding
    inflated = zlib.decompress(raw)  # 标准 zlib（带 zlib 头）
    return inflated.decode("utf-8", "ignore")

# ============ 解析 ============
def field_value(fv, meta):
    """复现前端 tdFieldValue：按字段类型提取可读文本。"""
    if not isinstance(fv, dict):
        return ""
    try:
        t = meta.get("type")
        if t == 1:  # 文本
            arr = fv.get("k1") or []
            if isinstance(arr, list):
                return "".join((x.get("k2") or x.get("k1") or "") for x in arr)
            return str(arr)
        if t == 4:  # 日期时间戳(毫秒)
            k4 = fv.get("k4")
            if k4 is not None:
                try:
                    ts = int(k4)
                    dt = datetime.datetime.fromtimestamp(ts/1000) if ts > 1e11 else datetime.datetime.fromtimestamp(ts)
                    return dt.strftime("%Y-%m-%d")
                except Exception:
                    pass
            return ""
        if t == 8:  # URL
            arr = fv.get("k8") or fv.get("k1")
            if isinstance(arr, str):
                return arr
            if isinstance(arr, list):
                return " ".join(x.get("k2") for x in arr if isinstance(x, dict) and x.get("k2"))
            return ""
        if t in (9, 17):  # 多选 / 单选
            ids = fv.get("k9") or fv.get("k17") or []
            if isinstance(ids, list):
                return "/".join(meta.get("options", {}).get(i, i) for i in ids)
            return str(ids)
        # 兜底：遍历找文本数组
        for k, v in fv.items():
            if isinstance(v, list) and v:
                texts = [x.get("k2") if isinstance(x, dict) else str(x) for x in v if x]
                if texts:
                    return "/".join(filter(None, texts))
    except Exception:
        pass
    return ""

def parse_sheet(json_str):
    """复现前端 tdParseSheet：返回 [{中文字段名: 值}, ...]。"""
    rows = json.loads(json_str)
    if not rows or not isinstance(rows[0], list) or len(rows[0]) < 2:
        return []
    h0, h1 = rows[0][0], rows[0][1]
    field_defs = ((h0.get("c", {}).get("k3", {}).get("k3")) or {})
    field_meta = {}
    for fid, def_ in field_defs.items():
        if not isinstance(def_, dict):
            continue
        opts = {}
        opt_def = def_.get("k17") or def_.get("k9") or {}
        opt_arr = opt_def.get("k3") if isinstance(opt_def, dict) else None
        if isinstance(opt_arr, list):
            for o in opt_arr:
                if isinstance(o, dict) and o.get("k1") and o.get("k2"):
                    opts[o["k1"]] = o["k2"]
        field_meta[fid] = {"name": def_.get("k30") or fid, "type": def_.get("k31"), "options": opts}
    records = ((h1.get("c", {}).get("k2", {}).get("k1")) or {})
    out = []
    for rid, rec_node in records.items():
        fields = rec_node.get("k1") if isinstance(rec_node, dict) else rec_node
        if not isinstance(fields, dict):
            continue
        rec = {}
        for fid, fv in fields.items():
            meta = field_meta.get(fid)
            if not meta:
                continue
            rec[meta["name"]] = field_value(fv, meta)
        out.append(rec)
    return out

# ============ 映射（复现前端 tdToRow / mapTDIndustry / extractLocation / isExpiredDeadline）============
def map_industry(td_ind):
    if not td_ind:
        return "综合"
    rules = [
        (r"互联网|软件|游戏|AI|大模型|电商|科技", "互联网科技"),
        (r"银行|金融|证券|基金|保险|信托", "银行金融"),
        (r"能源|电力|燃气|核能", "能源电力"),
        (r"通信|5G|电信", "通信运营商"),
        (r"汽车|驾驶", "汽车制造"),
        (r"医药|医疗|生物|制药", "医药医疗"),
        (r"快消|零售|食品|饮料|家电", "快消零售"),
        (r"装备|机械|制造|机器人|半导体|芯片|硬件", "装备重工"),
        (r"建筑|地产|市政|工程", "建筑地产"),
        (r"石油|石化|化工", "石油化工"),
        (r"航天|航空|军工|国防", "航天军工"),
        (r"物流|运输|交通|邮政", "交通物流"),
        (r"农业|农林|畜牧|食品", "农业食品"),
    ]
    for pat, name in rules:
        if re.search(pat, td_ind):
            return name
    return "综合"

def extract_location(text):
    if not text:
        return ""
    if re.search(r"多地|全国|不限地点|工作地不限", text):
        return "多地"
    found = [c for c in CITY_LIST if c in text]
    return "/".join(found[:4])

def is_expired(deadline):
    if not deadline:
        return False
    d = re.sub(r"\s+", " ", str(deadline)).strip()
    if re.search(r"招满即止|招聘中|长期|不限|持续", d):
        return False
    if re.search(r"已结束|已截止|过期|截止$", d):
        return True
    m = re.search(r"(\d{4})[年\/\-.\s]\s*(\d{1,2})[月\/\-.\s]\s*(\d{1,2})日?", d)
    if m:
        try:
            end = datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
            return end < datetime.date.today()
        except Exception:
            pass
    m2 = re.search(r"(\d{1,2})月(\d{1,2})日", d) or re.search(r"^(\d{1,2})[\/\-.](\d{1,2})$", d)
    if m2:
        try:
            now = datetime.date.today()
            end2 = datetime.date(now.year, int(m2.group(1)), int(m2.group(2)))
            return end2 < now
        except Exception:
            pass
    return False

def to_row(r):
    c = (r.get("公司名称") or "").strip()
    p = (r.get("招聘岗位") or "").strip()[:80]
    if not c and not p:
        return None
    deadline = (r.get("招聘截止日期") or "").strip()
    if is_expired(deadline):
        return None
    loc_text = (r.get("工作地点") or "") + " " + (r.get("行业") or "")
    loc = extract_location(loc_text) or extract_location(r.get("工作地点") or "")
    url = (r.get("投递链接or推文") or r.get("投递链接") or "").strip()
    clean_url = url.split()[0] if (url and re.match(r"^https?://", url)) else ""
    ind = map_industry(r.get("行业") or "")
    batch = (r.get("批次") or "").strip()
    title = p if p else (batch or "校招信息")
    return {
        "c": c, "p": title, "l": loc, "e": "",
        "w": ("批次:" + batch) if batch else "",
        "d": deadline, "s": "校招信息聚合平台",
        "t": ("互联网" if ind == "互联网科技" else "其他"),
        "ind": ind, "u": clean_url,
    }

# ============ 主流程 ============
def run(push=False, dry=False):
    all_rows = []
    seen = set()
    for sheet_id, name, limit in SHEETS:
        print(f"[拉取] {name} ({sheet_id}) ...", end=" ", flush=True)
        for off in range(0, limit, PAGE_SIZE):
            try:
                js = fetch_sheet_raw(sheet_id, off + PAGE_SIZE)
                page = parse_sheet(js)
            except Exception as e:
                print(f"页 {off} 失败: {e}")
                break
            if not page:
                break
            added = 0
            for r in page:
                row = to_row(r)
                if not row:
                    continue
                key = row["c"] + "|" + row["p"] + "|" + row["l"]
                if key in seen:
                    continue
                seen.add(key)
                all_rows.append(row)
                added += 1
            print(f"页{off}:{len(page)}条→净增{added}", end="  ", flush=True)
            if added == 0:  # opendoc 每次从 0 返回，无新增即到底
                break
        print()  # 换行
    print(f"\n[汇总] 两表合并后共 {len(all_rows)} 条有效招聘信息")
    # 行业分布
    from collections import Counter
    dist = Counter(x["ind"] for x in all_rows)
    for k, v in dist.most_common():
        print(f"   {k}: {v}")
    if dry:
        return
    out = {
        "updated": datetime.date.today().isoformat(),
        "count": len(all_rows),
        "jobs": all_rows,
    }
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "jobs.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    print(f"\n[jobs.json] 已写入 {path} ({os.path.getsize(path)//1024} KB)")
    if push:
        try:
            subprocess.run(["git", "add", "jobs.json"], cwd=here, check=True)
            msg = f"data: sync jobs.json from Tencent Docs ({len(all_rows)} jobs, {out['updated']})"
            subprocess.run(["git", "commit", "-m", msg], cwd=here, check=True)
            subprocess.run(["git", "push", "origin", "main"], cwd=here, check=True)
            print("[git] 已 commit + push 到 main")
        except subprocess.CalledProcessError as e:
            print(f"[git] 推送失败: {e}")

if __name__ == "__main__":
    push = "--push" in sys.argv
    dry = "--dry" in sys.argv
    run(push=push, dry=dry)
