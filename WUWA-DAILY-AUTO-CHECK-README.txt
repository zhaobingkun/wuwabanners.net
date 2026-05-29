WuWa Banners Daily Auto Check

这套任务的目标不是“自动更新网站内容”，而是：
- 每天自动检查官方来源
- 每天自动生成检查报告和候选草稿
- 由你人工决定是否修改正式数据和是否重建站点

这样做的原因很简单：
- Pixel Flow / Clues by Sam 是结构化内容，适合自动同步
- WuWa banner 数据是高风险业务数据
- 如果脚本自动改错 phase、日期、lineup 或 source_url，会直接把错误内容同步到全站

所以这套任务只做 report-only 自动化。

当前自动执行时间
- 每天 11:00 执行一次

自动任务做什么
1. 进入项目目录：
   /Users/zhaobingkun/dev/wuthering-waves-next-banner/wuwabanners.net
2. 运行：
   /Library/Frameworks/Python.framework/Versions/3.13/bin/python3 scripts/check_official_banner_updates.py
3. 再运行：
   /Library/Frameworks/Python.framework/Versions/3.13/bin/python3 scripts/prepare_banner_csv_candidate.py
4. 生成或刷新这些文件：
   data/banner-update-report.json
   data/banner-data.candidate.csv
   data/banner-data.diff.txt
   data/banner-check-record.txt
   data/banner-check-history.log

自动任务不会做什么
- 不会修改 data/banner-data.csv
- 不会自动重建站点
- 不会自动发布

你每天需要做什么
1. 看报告文件
   先看：
   data/banner-check-record.txt

2. 如果你想看更细节
   再看：
   data/banner-update-report.json
   data/banner-data.diff.txt

3. 只回答一个问题
   当前 banner、next banner、featured characters、featured weapons、开始/结束日期、source_url 有没有官方层面的变化？

4. 如果没有变化
   什么都不用做。
   当天到这里结束。

5. 如果有变化
   打开：
   data/banner-data.candidate.csv
   data/banner-data.diff.txt
   data/banner-data.csv

6. 手动编辑正式数据
   只改 data/banner-data.csv
   不要直接拿 candidate 覆盖 live CSV。

7. 数据确认后，手动重建站点
   cd /Users/zhaobingkun/dev/wuthering-waves-next-banner/wuwabanners.net
   python3 scripts/run_banner_update_cycle.py

8. 抽查页面
   /
   /wuthering-waves-current-banner/
   /wuthering-waves-next-banner/
   /pull-advice/
   /wuthering-waves-banner-history/

9. 如果今天是切池日
   再额外确认：
   /wuthering-waves-next-banner-date/
   /wuthering-waves-current-banner-end-date/
   一个当前期角色页
   一个下一期角色页
   游戏内 Convene

每天最常见的结论
- 大多数日子里，不需要改 CSV
- 只有官方信息真的变了，才需要手动更新
- 只有 CSV 真改了，才需要跑 run_banner_update_cycle.py

最常用文件
- 你每天优先看的记录文件：
  data/banner-check-record.txt
- 历史记录：
  data/banner-check-history.log
- 比对状态底稿：
  data/banner-check-state.json
- 正式数据：
  data/banner-data.csv
- 自动检查报告：
  data/banner-update-report.json
- 自动候选草稿：
  data/banner-data.candidate.csv
- 自动 diff：
  data/banner-data.diff.txt
- 重建脚本：
  scripts/run_banner_update_cycle.py

自动任务相关文件
- wrapper：
  scripts/run_daily_official_check.sh
- launchd plist：
  /Users/zhaobingkun/Library/LaunchAgents/com.zhaobingkun.wuwabanners.daily-check.plist
- stdout 日志：
  /Users/zhaobingkun/Library/Logs/wuwabanners-daily-check.log
- stderr 日志：
  /Users/zhaobingkun/Library/Logs/wuwabanners-daily-check.err.log

怎么手动执行一次自动检查
方法 1：直接跑 wrapper
cd /Users/zhaobingkun/dev/wuthering-waves-next-banner/wuwabanners.net
./scripts/run_daily_official_check.sh

方法 2：分两步跑
cd /Users/zhaobingkun/dev/wuthering-waves-next-banner/wuwabanners.net
python3 scripts/check_official_banner_updates.py
python3 scripts/prepare_banner_csv_candidate.py

如果自动执行没有成功，手动怎么做
1. 先看日志
   /Users/zhaobingkun/Library/Logs/wuwabanners-daily-check.log
   /Users/zhaobingkun/Library/Logs/wuwabanners-daily-check.err.log

2. 手动执行 wrapper
   cd /Users/zhaobingkun/dev/wuthering-waves-next-banner/wuwabanners.net
   ./scripts/run_daily_official_check.sh

3. 如果 wrapper 失败，分开执行
   python3 scripts/check_official_banner_updates.py
   python3 scripts/prepare_banner_csv_candidate.py

4. 如果报告正常生成
   再看：
   data/banner-check-record.txt
   然后继续按“你每天需要做什么”里的流程处理。

5. 如果脚本本身报错
   先不要改正式 CSV。
   先根据日志修脚本或联系我继续处理。

如何确认计划任务是否已加载
命令：
launchctl print gui/$(id -u)/com.zhaobingkun.wuwabanners.daily-check

如果要立刻触发一次计划任务
命令：
launchctl kickstart -k gui/$(id -u)/com.zhaobingkun.wuwabanners.daily-check

如果以后想改执行时间
编辑：
  /Users/zhaobingkun/Library/LaunchAgents/com.zhaobingkun.wuwabanners.daily-check.plist

当前配置是：
- Hour = 11
- Minute = 0

改完后重新加载：
launchctl bootout gui/$(id -u) /Users/zhaobingkun/Library/LaunchAgents/com.zhaobingkun.wuwabanners.daily-check.plist
launchctl bootstrap gui/$(id -u) /Users/zhaobingkun/Library/LaunchAgents/com.zhaobingkun.wuwabanners.daily-check.plist

相关参考文档
- DAILY-UPDATE-SOP.md
- DAILY-CHECKLIST.txt
- UPDATE-WORKFLOW.md

一句话总结
- 自动任务每天帮你“检查、比对并产出记录文件”
- 你每天主要只需要“看 data/banner-check-record.txt，判断有没有变化”
- 真的有变化时，再手动改 data/banner-data.csv 并手动重建站点
