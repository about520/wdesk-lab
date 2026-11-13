#!/usr/bin/env python3
"""示例任务：跑起来会采集这台机器的信息 + 做点实际计算，结果写进 output/。

换成你自己的活很简单：把 main() 里的内容替换掉就行，
其他流程（装依赖、收产出、提交回仓库）都不用改。
"""

import json
import os
import platform
import shutil
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output"


def machine_info() -> dict:
    """这台免费机器到底什么配置，打出来心里有数。"""
    total, used, free = shutil.disk_usage("/")
    return {
        "主机名": platform.node(),
        "系统": f"{platform.system()} {platform.release()}",
        "架构": platform.machine(),
        "Python": platform.python_version(),
        "CPU 核心": os.cpu_count(),
        "磁盘总容量GB": round(total / 1024**3, 1),
        "磁盘可用GB": round(free / 1024**3, 1),
        "工作目录": os.getcwd(),
        "在GitHub上跑": os.getenv("GITHUB_ACTIONS") == "true",
        "仓库": os.getenv("GITHUB_REPOSITORY", "-"),
        "运行编号": os.getenv("GITHUB_RUN_NUMBER", "-"),
        "触发方式": os.getenv("GITHUB_EVENT_NAME", "-"),
    }


def some_work() -> dict:
    """一段能看出机器确实在为你干活的示例计算。

    换成你自己的真实任务即可 —— 爬数据、跑模型、批量转码、算报表都行。
    """
    started = time.time()

    # 示例：算前 20 万个整数里的素数个数（纯 CPU 活，用来量吞吐）
    limit = 200_000
    sieve = bytearray([1]) * limit
    sieve[0:2] = b"\x00\x00"
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            sieve[i * i :: i] = bytearray(len(sieve[i * i :: i]))
    primes = sum(sieve)

    return {
        "示例任务": f"统计 {limit} 以内素数个数",
        "结果": primes,
        "耗时秒": round(time.time() - started, 3),
    }


def main() -> None:
    OUT.mkdir(exist_ok=True)

    report = {
        "生成时间UTC": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        "机器信息": machine_info(),
        "任务结果": some_work(),
    }

    # 1) 给人看的报告
    lines = ["# 运行报告", ""]
    lines.append(f"- 生成时间(UTC)：{report['生成时间UTC']}")
    for k, v in report["机器信息"].items():
        lines.append(f"- {k}：{v}")
    lines.append("")
    lines.append("## 任务结果")
    for k, v in report["任务结果"].items():
        lines.append(f"- {k}：{v}")
    (OUT / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # 2) 给程序读的 JSON
    (OUT / "result.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # 3) 每次运行追加一行，攒历史用（定时任务跑起来就能看出效果）
    with (ROOT / "data" / "history.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(report, ensure_ascii=False) + "\n")

    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"\n产出已写入 {OUT}")


if __name__ == "__main__":
    main()
