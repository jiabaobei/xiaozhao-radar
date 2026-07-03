# 校招雷达 - Xiaozhao Radar

> **🔍 AI驱动的校招信息聚合平台 —— 突破传统招聘网站，直达央国企&互联网大厂微信公众号招聘内容，免费交付大学生使用。**

[![Version](https://img.shields.io/badge/version-1.0.0-blue)]()
[![License](https://img.shields.io/badge/license-Apache%202.0-green)]()

## 🎬 功能亮点

- **实时爬取**：集成 Firecrawl MCP 工具，从真实招聘网站获取最新职位数据
- **多源覆盖**：实习僧、BOSS直聘、智联招聘、国聘网、应届生求职网等
- **一键操作**：点击"一键爬虫"自动抓取，无需后端服务器
- **智能管理**：搜索、筛选、排序、编辑、导出 CSV
- **开源免费**：MIT 许可证，可自由使用和修改

## 📋 快速开始

### 1. 获取 Firecrawl API Key

1. 访问 https://www.firecrawl.dev/app/api-keys 注册并获取免费 API Key
2. 复制你的 API Key（格式：`fc-xxxxxxxxxxxx`）

### 2. 运行

直接双击 `校招雷达.html` 文件即可在浏览器中使用，无需安装任何依赖。

## 🔧 使用方法

### 基本操作

1. **启动**：双击 `校招雷达.html` 打开页面
2. **爬取数据**：
   - 方式一：点击左上角 **"🕷 一键爬虫(Firecrawl)"** 按钮
   - 方式二（推荐）：在 WorkBuddy 对话框输入"帮我爬取校招职位"，自动调用 Firecrawl MCP 工具
3. **编辑数据**：双击任意单元格进行编辑
4. **导出备份**：点击右上角 **"📥 导出"** 按钮保存为 CSV 文件

### 数据管理

| 功能 | 操作方式 |
|------|----------|
| 搜索 | 顶部搜索框输入关键词 |
| 筛选 | 按来源、学历下拉筛选 |
| 排序 | 点击"按公司"或"按截止"按钮 |
| 添加 | 点击 **"➕ 添加"** 按钮 |
| 删除 | 点击每行末尾的 **"x"** 按钮 |
| 清空 | 点击 **"🗑 清空"** 按钮 |

## 🎯 数据来源

通过 Firecrawl MCP 工具实时抓取：
- **实习僧** (shixiseng.com)
- **BOSS直聘** (zhipin.com)
- **智联招聘** (zhaopin.com)
- **国聘网** (guopin.com)
- **牛客网** (nowcoder.com)
- **应届生求职网** (yingjiesheng.com)
- **腾讯招聘** (join.qq.com)
- **字节跳动** (jobs.bytedance.com)
- **美团招聘** (zhaopin.meituman.com)
- **国有企业微信公众号**（国家电网、中国石化、中国烟草等）
- **互联网大厂微信公众号**（腾讯、阿里、字节等）
- **银行/券商微信公众号**（四大行、中信证券等）

## ⚙️ 技术特性

- **零后端**：纯 HTML + CSS + JavaScript，无需服务器
- **Firecrawl 集成**：通过 MCP 工具调用 Firecrawl API
- **智能解析**：自动提取公司、职位、地点、福利等结构化数据
- **数据持久化**：使用 localStorage 自动保存数据
- **响应式设计**：适配桌面和移动端

## 📁 文件结构

```
xiaozhao-radar/
├── xiaozhao-radar.html    # 主程序（单文件即可运行）
└── README.md              # 说明文档
```

## ❓ 常见问题

### Q: 需要安装什么软件吗？
A: 不需要！只需要一个现代浏览器（Chrome/Edge/Firefox），双击 HTML 文件即可运行。

### Q: 为什么要设置 API Key？
A: Firecrawl 需要 API Key 才能调用其抓取服务。注册即可获取免费额度。

### Q: 数据存在哪里？
A: 数据保存在浏览器本地（localStorage），关闭页面不会丢失。建议定期导出 CSV 备份。

### Q: 可以部署到自己的网站上吗？
A: 可以！这是一个纯前端项目，可以部署到任何静态网站托管服务（GitHub Pages、Vercel 等）。

## 📄 许可证

MIT License

## 🙏 致谢

- [Firecrawl](https://firecrawl.dev) - 提供强大的网页抓取 API
- [Agnes AI](https://agnes-ai.com) - 提供免费 AI 服务

## 📋 更新日志

### v2.0.0
- 集成 Firecrawl MCP 工具实现真实数据爬取
- 支持从 9+ 招聘网站实时获取数据
- 新增数据持久化（localStorage）
- 优化用户界面和交互体验
- 完善文档和使用说明

### v1.0.0
- 初始版本，37条示例数据
