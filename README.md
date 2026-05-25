# WuWa Banners

`wuwabanners.net` 的静态 SEO 站点，主要围绕 Wuthering Waves 的这些意图页：

- current banner
- next banner
- banner history
- banner countdown
- rerun watch
- pull advice

## 核心规则

日常卡池更新，先看这份数据：

`data/banner-data.csv`

然后重建：

```bash
cd /Users/zhaobingkun/dev/wuthering-waves-next-banner/wuwabanners.net
python3 scripts/build_banner_snapshot.py
```

大多数情况下，你真正需要改的就是这一个 CSV。

日常维护文档：

- [DAILY-UPDATE-SOP.md](/Users/zhaobingkun/dev/wuthering-waves-next-banner/wuwabanners.net/DAILY-UPDATE-SOP.md)
- [DAILY-CHECKLIST.txt](/Users/zhaobingkun/dev/wuthering-waves-next-banner/wuwabanners.net/DAILY-CHECKLIST.txt)
- [UPDATE-WORKFLOW.md](/Users/zhaobingkun/dev/wuthering-waves-next-banner/wuwabanners.net/UPDATE-WORKFLOW.md)
- [POST-LAUNCH-CONTENT-AUDIT.md](/Users/zhaobingkun/dev/wuthering-waves-next-banner/wuwabanners.net/POST-LAUNCH-CONTENT-AUDIT.md)
- [AI-HANDOFF.md](/Users/zhaobingkun/dev/wuthering-waves-next-banner/wuwabanners.net/AI-HANDOFF.md)

## 构建脚本会更新什么

构建脚本会刷新：

- `data/banner-snapshot.json`
- `assets/img/current-banner-card.svg`
- `assets/img/next-banner-card.svg`
- `assets/img/banner-history-card.svg`
- 这些页面里的动态区块：
  - `index.html`
  - `wuthering-waves-next-banner/index.html`
  - `wuthering-waves-current-banner/index.html`
  - `wuthering-waves-banner-history/index.html`
  - `wuthering-waves-next-rerun/index.html`
  - `wuthering-waves-banner-countdown/index.html`
  - `pull-advice/index.html`
- 自动生成的角色页：
  - `wuthering-waves-should-you-pull-*/index.html`
- 自动生成的角色支撑页：
  - `wuthering-waves-*-materials/`
  - `wuthering-waves-*-build/`
  - `wuthering-waves-*-team-comps/`
- `sitemap.xml`

## 数据源规则

优先使用官方来源：

1. 官网新闻 / patch notes
2. 官方直播 / 官方 YouTube
3. 游戏内 `Convene` 确认

只有在官方信息还不够完整时，才临时用二级媒体交叉核对。

## CSV 里最重要的字段

- `banner_type`
- `version`
- `phase`
- `featured_characters`
- `featured_weapons`
- `start_date`
- `end_date`
- `source_url`
- `status`
- `last_checked`

当前构建脚本会先根据带日期的 `character` 行判断当前卡池和下一个卡池，再按 `version + phase` 去匹配武器行。

## 正常更新流程

1. 运行 `python3 scripts/check_official_banner_updates.py`
2. 看终端输出或 `data/banner-update-report.json`
3. 只有报告显示确实有变化时，才改 `data/banner-data.csv`
4. 运行 `python3 scripts/run_banner_update_cycle.py`
5. 本地预览
6. 检查这些页面：
   - `/wuthering-waves-next-banner/`
   - `/wuthering-waves-current-banner/`
   - `/wuthering-waves-banner-history/`
   - `/wuthering-waves-next-rerun/`
   - `/wuthering-waves-banner-countdown/`
   - `/pull-advice/`
7. 确认新的角色页或变更后的角色页已经重新生成

## 半自动官方检查

在改 CSV 之前，先运行：

```bash
cd /Users/zhaobingkun/dev/wuthering-waves-next-banner/wuwabanners.net
python3 scripts/check_official_banner_updates.py
```

它会做这些事：

- 读取 `data/banner-data.csv`
- 检查哪些数据行太久没更新
- 访问当前 `source_url`
- 检查官网、官方 YouTube、Dear Players 更新页
- 生成 `data/banner-update-report.json`

它不会做这些事：

- 不会改 `data/banner-data.csv`
- 不会重建页面
- 不会自动发布

## 候选 CSV 草稿

如果你想先拿一份安全草稿，再运行：

```bash
cd /Users/zhaobingkun/dev/wuthering-waves-next-banner/wuwabanners.net
python3 scripts/prepare_banner_csv_candidate.py
```

它会生成：

- `data/banner-data.candidate.csv`
- `data/banner-data.diff.txt`

这个脚本只会自动刷新安全的 `last_checked`。
不会自动改 lineup、日期或 `source_url`。

## 本地预览

```bash
cd /Users/zhaobingkun/dev/wuthering-waves-next-banner/wuwabanners.net
python3 -m http.server 4173
```

打开：

- `http://127.0.0.1:4173/`
- `http://127.0.0.1:4173/wuthering-waves-next-banner/`
- `http://127.0.0.1:4173/pull-advice/`

## 什么情况还需要手改 HTML

下面这些情况仍然需要手动改 HTML：

- 新增一种页面类型
- 改布局
- 全站改 FAQ 结构
- 改 hub 策略
- 重做设计

## 一键维护命令

改完 banner 数据之后，直接运行：

```bash
cd /Users/zhaobingkun/dev/wuthering-waves-next-banner/wuwabanners.net
python3 scripts/run_banner_update_cycle.py
```

它会：

- 重建 reference detail pages
- 重建 banner snapshot pages
- 编译检查 Python 脚本
- 检查 `assets/js/site.js` 语法
- 校验核心 hub、页面、重点角色支撑页和 sitemap URL

## 目录说明

- `assets/css/`：站点样式
- `assets/img/`：生成图卡和静态图片
- `data/`：源 CSV 和生成的 JSON 快照
- `scripts/`：构建脚本
- `banners/`：banner hub
- `guides/`：guides hub
- `pull-advice/`：抽卡决策 hub
- `wuthering-waves-should-you-pull-*/`：自动生成的抽卡页
