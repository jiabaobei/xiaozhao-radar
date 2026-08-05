# 校招雷达 · 跨设备恢复说明

## 数据源
- 腾讯文档（智能表格）: https://docs.qq.com/smartsheet/DTkRMUVhoUWJXZEhJ
- padId: NDLQXhQbWdHI
- 子表1: tTNjGc 「27届内推汇总」
- 子表2: tvVDZj 「实习提前批每日更新」

## 字段映射（腾讯文档列 → jobs.json）
- 公司名称 → c
- 招聘岗位 → p
- 工作地点/行业 → l（提取城市）
- 行业 → ind（映射到15行业分类）
- 招聘截止日期 → d
- 投递链接or推文/投递链接 → u
- 批次 → w
- s 固定为"校招信息聚合平台"
- t 固定为"互联网"或"其他"
- e 固定为空

## 同步脚本
- GitHub 仓库: https://github.com/jiabaobei/xiaozhao-radar
- 脚本文件: sync_tencent_docs.py（仓库根目录，纯标准库）
- 详细文档: SYNC.md（仓库根目录）

## 每周五指令
用户说"同步校招"时：
1. 拉取/clone 仓库到本地
2. 运行 python sync_tencent_docs.py --push
3. 检查输出条数与 GitHub Pages 部署状态
4. 汇报：本次X条，较上次±Y条

## 跨设备说明
若在新电脑/手机收到指令：
1. 从 GitHub 下载 sync_tencent_docs.py 和 SYNC.md
2. 确保本地有 Python 与 git
3. 运行 python sync_tencent_docs.py --push

## 已验证链路
- 2026-08-05 实测：拉取1355条 → jobs.json → push → GitHub Pages updated=2026-08-05
