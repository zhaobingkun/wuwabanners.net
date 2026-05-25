# Daily Update SOP

这份文档用于 `wuwabanners.net` 的日常维护。

## 每天先检查什么

普通日常，先做一次轻检查。

优先看这些来源：

1. 官网新闻 / patch notes  
   `https://wutheringwaves.kurogames.com/`

2. 官方 YouTube / 前瞻直播  
   `https://www.youtube.com/@WutheringWaves`

3. 官方社媒 / 官宣贴  
   尽量沿用 `data/banner-data.csv` 里已经在用的官方来源链。

4. 切池当天的游戏内 `Convene`  
   这是确认 live 卡池时间和 lineup 最稳的一层。

## 日常更新节奏

### 普通无事件日

- 早上检查一次
- 运行 `python3 scripts/check_official_banner_updates.py`
- 如果没有新的官方变化，不要改 `data/banner-data.csv`
- 不需要重建

### 前瞻前 / 切池前窗口

- 一天检查 `2-3` 次：
  - 早上
  - 下午
  - 如果晚上有直播或官宣预期，再看一次

### 切池当天

- 切池前看一次
- 切池生效后再看一次游戏内
- 重点确认：
  - 当前 phase
  - 下一个 phase
  - 当前武器
  - 开始 / 结束日期

## 什么时候要改数据

主数据文件：

- [data/banner-data.csv](/Users/zhaobingkun/dev/wuthering-waves-next-banner/wuwabanners.net/data/banner-data.csv)

通常会变化的字段：

- `version`
- `phase`
- `featured_characters`
- `featured_weapons`
- `start_date`
- `end_date`
- `source_url`
- `source_type`
- `announcement_date`
- `status`
- `last_checked`

## 重建命令

```bash
cd /Users/zhaobingkun/dev/wuthering-waves-next-banner/wuwabanners.net
python3 scripts/run_banner_update_cycle.py
```

这条更新链会刷新：

- `data/banner-snapshot.json`
- 首页动态区块
- `next banner`
- `current banner`
- `banner history`
- `next rerun`
- `banner countdown`
- `pull advice`
- 自动生成的 `should-you-pull-*`
- 自动生成的角色支撑页：
  - `*-materials`
  - `*-build`
  - `*-team-comps`
- `sitemap.xml`

它还会：

- 重建 reference detail pages
- 编译检查 Python 脚本
- 检查 `assets/js/site.js` 语法
- 校验关键页面和 sitemap 覆盖

## 需要时可单独运行的命令

如果你只想跑部分流程，可以单独运行：

```bash
python3 scripts/check_official_banner_updates.py
python3 scripts/prepare_banner_csv_candidate.py
python3 scripts/build_reference_pages.py
python3 scripts/build_banner_snapshot.py
python3 scripts/verify_site_build.py
```

## 本地预览

```bash
cd /Users/zhaobingkun/dev/wuthering-waves-next-banner/wuwabanners.net
python3 -m http.server 4173
```

打开并检查：

- `http://127.0.0.1:4173/`
- `http://127.0.0.1:4173/wuthering-waves-next-banner/`
- `http://127.0.0.1:4173/wuthering-waves-current-banner/`
- `http://127.0.0.1:4173/pull-advice/`

再额外抽查一个当前期角色和一个下一期角色：

- `should-you-pull-*`
- `*-materials`
- `*-build`
- `*-team-comps`

## 重建后要核对什么

1. 首页 current / next 时间线是否正确
2. `next banner` 和 `current banner` 的日期是否正确
3. `pull advice` 里 current / next 角色是否正确
4. 自动生成的角色支撑页是否和当前 snapshot 对应
5. `sitemap.xml` 是否包含这些角色支撑页 URL

## 什么时候才需要加新页面

**不要每天加新页。**

只有这些情况才考虑新增或扩页：

- current / next phase 切换了
- 有新的 featured character 进入当前跟踪集合
- 新的官方揭示带来了一个能持续存在的搜索意图

大多数日子里，你真正要做的是：

- 看官方有没有变
- 只有需要时才改 CSV
- 只有数据真变了才重建
