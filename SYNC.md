# 校招雷达 · 数据同步工作流（腾讯文档 → GitHub）

> 本文件记录「校招雷达」页面数据的**自动同步方案**：每周读取腾讯文档智能表格 → 生成 `jobs.json` → 推送 GitHub Pages → 页面自动显示最新数据。
> 数据链路于 2026-08-04 首次打通并验证，2026-08-05 固化为可复用脚本。

---

## 一、数据源（腾讯文档智能表格）

| 项目 | 值 |
|---|---|
| 文档标题 | 27届实习提前批信息汇总 |
| 文档链接 | https://docs.qq.com/smartsheet/DTkRMUVhoUWJXZEhJ |
| padId | `NDLQXhQbWdHI` |
| 文档类型 | 智能表格（smartsheet），**私有文档（需登录态，但 opendoc 接口匿名可读）** |

### 核心子表（sheet）

| sheetId | 名称 | 规模 |
|---|---|---|
| `tTNjGc` | 27届内推汇总 | ~100 条 |
| `tvVDZj` | 实习提前批每日更新 | ~1640 条（每日增长） |

---

## 二、读取通道（无需登录 / 无需代理）

破解腾讯文档 `opendoc` 公开接口，Python 直连（能带 `Referer` 头，不像浏览器受限）：

```
GET https://docs.qq.com/dop-api/opendoc
    ?id=DTkRMUVhoUWJXZEhJ&subId=<sheetId>&startrow=0&endrow=N
    &noEscape=1&enableSmartsheetSplit=1&supportOptimizedVer=4
    &chunkCellSize=15000&normal=1&outformat=1&wb=1&nowb=0&callback=x
Header: Referer: https://docs.qq.com/smartsheet/DTkRMUVhoUWJXZEhJ
```

返回 JSONP → `clientVars.collab_client_vars.initialAttributedText.text[0].smartsheet`
→ **base64（补 padding）→ 标准 zlib 解压** → JSON 表格数据（`rows[0]=[字段定义meta, 记录data]`）

> ⚠️ 历史坑（已解决）：① base64 字符串长度非 4 倍数需补 `=`；② 压缩是**标准 zlib（带头）**，不是 raw deflate；③ 浏览器 fetch 不能设 Referer 会被 401，但 Python/curl 带 Referer 直接 200。

---

## 三、字段映射（腾讯文档 → jobs.json）

腾讯文档列名（中文）→ 标准字段（单字母键）：

| 腾讯文档列名 | jobs.json 键 | 说明 |
|---|---|---|
| 公司名称 | `c` | 公司 |
| 招聘岗位 | `p` | 职位（截断 80 字） |
| 工作地点 | `l` | 地点（从「工作地点+行业」提取城市，命中 CITY_LIST） |
| 行业 | `ind` | 映射到项目 15 行业分类 |
| 招聘截止日期 | `d` | 截止（过期自动过滤不显示） |
| 投递链接or推文 / 投递链接 | `u` | 链接（仅保留 `http(s)://` 开头） |
| 批次 | `w` | 批次（格式 `批次:xxx`） |
| （固定） | `s` | 来源，固定 `"校招信息聚合平台"` |
| （固定） | `t` | 分类，`ind==互联网科技?"互联网":"其他"` |
| （固定） | `e` | 学历，留空 |

**jobs.json 结构**：
```json
{ "updated": "2026-08-05", "count": 1355, "jobs": [ {c,p,l,e,w,d,s,t,ind,u}, ... ] }
```

---

## 四、同步脚本用法

脚本：`sync_tencent_docs.py`（仓库根目录，纯标准库，无需 pip 安装）

```bash
# 仅生成本地 jobs.json（不推送，用于预览）
python sync_tencent_docs.py --dry

# 生成 jobs.json（覆盖仓库根目录）
python sync_tencent_docs.py

# 生成 + 自动 git commit + push 到 main
python sync_tencent_docs.py --push
```

脚本自动完成：拉两表 → 字段映射 → 去重（公司+职位+地点）→ 过期过滤 → 生成 `jobs.json` →（可选）推送。

---

## 五、每周五同步操作流程

**触发方式**：用户每周五发一句「同步校招」→ AI 执行以下动作：

1. 运行 `python sync_tencent_docs.py --push`
2. 检查输出统计（总条数、各行业分布）是否正常
3. 确认 GitHub Pages 部署（`jiabaobei.github.io/xiaozhao-radar/jobs.json` 通常 1-2 分钟生效）
4. 向用户汇报：「已同步，本次 X 条，较上次 ±Y 条」
5. 桌面 `校招雷达github发布/index.html` 无需更新（页面打开时自动从 GitHub Pages 读最新 jobs.json）

> 💡 用户双击本地 HTML 也能看到最新数据——因为 GitHub Pages 返回 `Access-Control-Allow-Origin: *`，跨域读取无障碍，无需重新下载 HTML。

---

## 六、风险与兜底

- **接口偶发 401/超时**：腾讯文档接口偶有限流。脚本带分页重试与 `added==0` 提前停止；若某次失败，重试或等几分钟再跑。
- **数据异常**：若某次同步条数骤降/骤增，先 `--dry` 预览确认，不轻易 `--push`。
- **文档结构变更**：若腾讯文档改了列名（如「公司名称」改名），需同步更新 `parse_sheet`/`to_row` 中的中文字段名。
- **兜底（页面端）**：`index.html` 内置 `tdFallback()` 仍保留——若 GitHub Pages 的 jobs.json 缺失，页面可临时直连腾讯文档兜底（依赖本地代理 `node proxy.js`）。
