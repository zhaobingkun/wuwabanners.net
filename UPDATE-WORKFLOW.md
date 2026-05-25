# WuWa Banners 更新流程

这份文档用于最稳妥、可重复的更新流程。

## 目标

在不让脚本静默覆盖官方数据的前提下，保持 `data/banner-data.csv` 准确。

当前推荐流程分 3 层：

1. `check_official_banner_updates.py`
2. `prepare_banner_csv_candidate.py`
3. `run_banner_update_cycle.py`

## 每个脚本分别做什么

### 1. 检查脚本

命令：

```bash
cd /Users/zhaobingkun/dev/wuthering-waves-next-banner/wuwabanners.net
python3 scripts/check_official_banner_updates.py
```

它会做：

- 读取 `data/banner-data.csv`
- 检查哪些行太久没更新
- 检查哪些行还在用 `secondary_media`
- 访问当前 `source_url`
- 检查官网 / 官方 YouTube / Dear Players 更新页
- 生成 `data/banner-update-report.json`

它不会做：

- 不会改 `data/banner-data.csv`
- 不会重建页面
- 不会发布

## 2. 候选草稿脚本

命令：

```bash
cd /Users/zhaobingkun/dev/wuthering-waves-next-banner/wuwabanners.net
python3 scripts/prepare_banner_csv_candidate.py
```

它会做：

- 读取 `data/banner-data.csv`
- 读取 `data/banner-update-report.json`
- 生成：
  - `data/banner-data.candidate.csv`
  - `data/banner-data.diff.txt`

它会自动改什么：

- 只会自动刷新安全的 `last_checked`

它不会自动改什么：

- banner 名称
- featured characters
- featured weapons
- 开始 / 结束日期
- `source_url`
- `source_type`
- 新版本占位行

## 3. 重建脚本

命令：

```bash
cd /Users/zhaobingkun/dev/wuthering-waves-next-banner/wuwabanners.net
python3 scripts/run_banner_update_cycle.py
```

它会做：

- 重建 reference detail pages
- 重建 banner snapshot pages
- 编译检查 Python 脚本
- 检查 `assets/js/site.js` 语法
- 校验核心页面和 sitemap 覆盖

## 日常操作顺序

### 普通日

1. 运行：

```bash
python3 scripts/check_official_banner_updates.py
```

2. 如果没有重要变化，停止。

3. 如果报告提示可能有变化，再运行：

```bash
python3 scripts/prepare_banner_csv_candidate.py
```

4. 打开这些文件：
- `data/banner-update-report.json`
- `data/banner-data.diff.txt`
- `data/banner-data.candidate.csv`

5. 手动编辑：
- `data/banner-data.csv`

候选文件和 diff 只是参考，不要直接无脑覆盖正式 CSV。

6. 重建：

```bash
python3 scripts/run_banner_update_cycle.py
```

7. 本地预览或直接发布。

## 切池当天

流程和上面一样，但要再加一层：

- 游戏内 `Convene` 最终确认

重建后，额外检查：

- `/`
- `/wuthering-waves-current-banner/`
- `/wuthering-waves-next-banner/`
- `/pull-advice/`
- `/wuthering-waves-banner-history/`
- 一个当前期角色 hub
- 一个下一期角色 hub

## 最安全的编辑原则

脚本只负责“提示你可能哪里变了”。  
真正的内容确认，还是由你手动决定。

也就是：

- 脚本负责告诉你该检查什么
- 脚本可以帮你刷新 `last_checked`
- 但最终什么内容进正式 `data/banner-data.csv`，还是你决定

## 需要记住的文件

- 正式数据： `data/banner-data.csv`
- 检查报告： `data/banner-update-report.json`
- 候选草稿： `data/banner-data.candidate.csv`
- 文字 diff： `data/banner-data.diff.txt`
- 重建脚本： `scripts/run_banner_update_cycle.py`
