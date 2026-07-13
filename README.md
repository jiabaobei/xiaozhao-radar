# 校招雷达 - Xiaozhao Radar

> **🔍 AI驱动的校招信息聚合平台 —— 100家央企&互联网大厂校招公告实时抓取，分批加载+分页浏览。**

[![Version](https://img.shields.io/badge/version-2.0.1-blue)]()
[![License](https://img.shields.io/badge/license-Apache%202.0-green)]()

## 🎬 v2.0.1 核心亮点

- **100家招聘官网**：50家互联网大厂（腾讯/阿里/字节/美团/百度/京东/华为/小米...）+ 50家央企国企（国家电网/中石化/中石油/中国移动/航天科工...）+ 3家综合招聘网站（51job/应届生/国聘）排最后
- **分批加载**：先爬前20个站（互联网大厂优先）立即展示，后台继续加载剩余83个站，每10个站更新一次表格
- **分页浏览**：支持 20/50/100 条/页切换，上一页/下一页按钮，页码实时显示
- **公司名正确显示**：公司列直接显示"腾讯/美团/国家电网"等真实公司名，不再是来源网站名
- **分类筛选**：来源下拉支持按"互联网大厂/央企国企/综合招聘"分类过滤
- **双源互补**：Firecrawl（云端）管公开页 + OpenCLI xiaozhao 适配器（本地登录态）管需登录站

## 📋 快速开始

### 方式一：Firecrawl 公开页（免登录）

1. 访问 https://www.firecrawl.dev/app/api-keys 注册获取免费 API Key（格式：`fc-...`）
2. 双击 `xiaozhao-radar.html` 打开页面
3. 在 `Firecrawl API Key` 框填 Key → 点 **🕷 一键爬虫**
4. 前20个站爬完立即出数据，后台继续加载剩余站点

### 方式二：OpenCLI xiaozhao 适配器（完整职位库，需登录态）

```bash
# 安装 OpenCLI
npm install -g @jackwener/opencli

# 爬校招数据（复用 Chrome 登录态）
opencli xiaozhao search "2027 校招" -f json > xiaozhao.json

# 校招雷达点「📤 导入」选 xiaozhao.json
```

可选参数：`--city 成都` `--degree 本科` `--limit 30`

## 🎯 数据源（103条）

| 分类 | 数量 | 覆盖 |
|------|------|------|
| 互联网大厂 | 50 | 腾讯/阿里/字节/美团/百度/京东/华为/小米/网易/拼多多/快手/滴滴/B站/携程... |
| 央企国企 | 50 | 国家电网/中石化/中石油/中国移动/中国电信/华能/大唐/中核/航天科工/中航工业... |
| 综合招聘 | 3 | 51job校招/应届生求职网/国聘 |

## 📁 文件结构

```
xiaozhao-radar/
├── xiaozhao-radar.html          # 主程序（单文件即可运行）
├── index.html                   # GitHub Pages 入口（与主程序同步）
├── README.md                    # 说明文档
├── LICENSE                      # Apache 2.0
├── manifest.json                # 项目元数据
└── clis/xiaozhao/               # OpenCLI 校招专用适配器
    ├── search.js                # `opencli xiaozhao search` 命令实现
    └── utils.js                 # Playwright 页面交互 + 字段映射
```

## ❓ 常见问题

### Q: 一键爬虫返回空数据？
A: 103个站每个都调Firecrawl API，免费层有速率限制。前20个站加载完会立即展示，后续站点后台陆续加载。

### Q: 页面显示旧版？
A: 浏览器缓存问题，按 **Ctrl+Shift+R** 强制刷新。

### Q: 导入 JSON 字段对不上？
A: 导入函数已兼容多种字段命名（title/position、company、city/district、degree、salary/tags/issueDate/url），直接导即可。

## 📄 许可证

Apache 2.0 License

## 📋 更新日志

### v2.0.1
- CRAWL_SITES 扩展至 103 条：50家互联网大厂 + 50家央企国企 + 3家综合招聘网站（排最后）
- 公司列直接显示真实公司名（腾讯/美团/国家电网等），不再显示来源网站名
- 新增分批加载：先爬前20个站立即展示，后台继续加载剩余83个站
- 新增分页功能：支持 20/50/100 条/页切换，上一页/下一页按钮
- 来源下拉改为分类筛选：互联网大厂/央企国企/综合招聘
- 域名过滤放宽：支持 hr./talent/career/join/recruit/hotjob 等招聘域名
- SAMPLE_DATA 增加 type 字段，演示数据支持分类筛选

### v2.0.0
- Firecrawl 改走 v1/scrape 抓取预置校招官网官方公告页
- 新增 OpenCLI xiaozhao 校招专用适配器
- 新增「📤 导入」按钮，支持 JSON/CSV
- 公司列改为纯公司名，来源列移至末尾
- 表格卡片化，标题超长省略

### v1.1.0
- 接入 Firecrawl REST API 真实联网搜索
- API Key 改为页面输入框 + 浏览器本地存储

### v1.0.0
- 初始版本
