# 校招雷达 - Xiaozhao Radar

> **🔍 AI驱动的校招信息聚合平台 —— 央国企&互联网大厂校招公告实时抓取，支持 OpenCLI 本地登录态补充。**

[![Version](https://img.shields.io/badge/version-2.0.0-blue)]()
[![License](https://img.shields.io/badge/license-Apache%202.0-green)]()

## 🎬 v2.0 核心亮点

- **真实爬虫**：改用 Firecrawl v1/scrape 抓取国网招聘/51job/应届生求职网**官方公告页**，提取真实公告链接（旧版 web search 对中文校招质量极差，已弃用）
- **双源互补**：Firecrawl（云端）管公开页 + `OpenCLI xiaozhao` 适配器（本地登录态）管需登录站（51job/BOSS 完整职位库）
- **一键导入**：支持导入 JSON/CSV，已对齐 OpenCLI `opencli xiaozhao search -f json` 输出字段
- **公司列干净显示**：第一列显示公司名（国家电网/51job），来源单独放最后一列

## 📋 快速开始

### 方式一：Firecrawl 公开页（免登录）

1. 访问 https://www.firecrawl.dev/app/api-keys 注册获取免费 API Key（格式：`fc-...`）
2. 双击 `xiaozhao-radar.html` 打开页面
3. 在 `Firecrawl API Key` 框填 Key → 点 **🕷 一键爬虫**，等几秒，国网/51job/应届生真实公告进表格

### 方式二：OpenCLI xiaozhao 适配器（完整职位库，需登录态）

```bash
# 安装 OpenCLI（如已装可跳过）
npm install -g @jackwener/opencli

# 爬校招数据（复用 Chrome 登录态）
opencli xiaozhao search "2027 校招" -f json > xiaozhao.json

# 校招雷达点「📤 导入」选 xiaozhao.json
```

可选参数：`--city 成都` `--degree 本科` `--limit 30`

## 🎯 数据源

| 方式 | 覆盖 | 需要 |
|------|------|------|
| Firecrawl scrape | 国网/51job/应届生 官方公告页 | Firecrawl API Key |
| OpenCLI xiaozhao | 51job/BOSS 完整职位库 | 浏览器登录态 |

## 📁 文件结构

```
xiaozhao-radar/
├── xiaozhao-radar.html          # 主程序（单文件即可运行）
├── README.md                    # 说明文档
├── LICENSE                      # Apache 2.0
├── manifest.json                # 项目元数据
└── clis/xiaozhao/               # OpenCLI 校招专用适配器
    ├── search.js                # `opencli xiaozhao search` 命令实现
    └── utils.js                 # Playwright 页面交互 + 字段映射
```

## ❓ 常见问题

### Q: 一键爬虫返回空数据？
A: Firecrawl 免费层有并发限制，每次抓 3 个官网，单个官网超时自动跳过，非空即成功。

### Q: 导入 JSON 字段对不上？
A: 导入函数已兼容多种字段命名（title/position、company、city/district、degree、salary/tags/issueDate/url），直接导即可。

### Q: 公司列怎么显示"国家电网招聘"而不是"国家电网"？
A: v2.0 已修复，公司列显示纯名，完整站点名在最后一列「来源」。

## 📄 许可证

Apache 2.0 License

## 📋 更新日志

### v2.0.0
- Firecrawl 改走 v1/scrape 抓取预置校招官网官方公告页（v2/search web search 对中文校招质量极差，已弃用）
- 新增 OpenCLI `xiaozhao` 校招专用适配器（复用 Chrome 登录态爬 51job/BOSS 完整职位库）
- 新增「📤 导入」按钮，支持 JSON/CSV，字段已对齐 OpenCLI 输出
- 公司列改为纯公司名（SITE_COMPANY 映射），来源列移至末尾
- 表格卡片化，标题超长省略（悬停看全文）
- 页面标题加 v2.0 标识

### v1.1.0
- 接入 Firecrawl REST API 真实联网搜索
- API Key 改为页面输入框 + 浏览器本地存储

### v1.0.0
- 初始版本
