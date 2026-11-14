# GitHub 免费算力 — 开箱即用包

一套直接能跑的东西，拿去把 GitHub 给的免费机器用起来。
不用装任何工具，全部在网页上点几下就能跑。

---

## 一、先搞清楚能拿到什么

| 玩法 | 拿到的东西 | 能干嘛 | 一次能撑多久 |
|---|---|---|---|
| **临时 SSH 机器** | Ubuntu，2 核 / 7G 内存 / 40G 盘 | 当一台真电脑用，随便装随便玩，能 ssh 进去 | 最长约 6 小时 |
| **跑任务** | 同样的机器，跑完自动收产出 | 爬数据、批量处理、跑脚本、算东西 | 最长约 6 小时 |
| **三平台编译** | Linux + Windows + macOS 三份产物 | 编译自己的程序，本地一个工具链都不用装 | 按需 |
| **临时公网地址** | https 网址，指向你机器上的服务 | 临时演示 / 自己手机访问 | 跟着机器走 |
| **Codespaces** | 真正的开发机，浏览器里就是完整的 VS Code | 长期写代码、调试，有终端有端口转发 | 每月 120 核时（2 核机约 60 小时） |

公开仓库的机器**完全免费、不限时长**（单次任务仍受 6 小时上限约束）。
私有仓库走 Free 计划每月 $12 的额度，也够个人用很久。

---

## 二、怎么放上去（网页操作，两分钟）

1. 打开 github.com，右上角 **+** → **New repository**
2. 名字随便起，比如 `my-box`，选 **Public**（公开仓库才免费不限量），点 **Create repository**
3. 在新仓库页面点 **uploading an existing file**
4. 把这个文件夹里的东西**全选拖进去**（`.github` 这个文件夹一定要拖，它是隐藏的，别漏）
5. 底下点 **Commit changes**

拖完仓库里应该是这个结构：

```
.github/workflows/     ← 五个现成的流程，别漏这个
scripts/hello.py       ← 示例任务，换成你自己的活
scripts/requirements.txt
README.md
```

---

## 三、开一台临时机器（最接近"白嫖一台电脑"）

1. 仓库页面点顶上的 **Actions**
2. 左边选 **开一台临时交互式机器（SSH）**
3. 右边点 **Run workflow** → 再点绿色的 **Run workflow**
4. 等十几秒，刷新页面，点进正在跑的那条任务
5. 展开 **开 SSH 会话** 这一步，里面会打印几行 `ssh xxx@nyc1.tmate.io` 这样的连接串
6. 复制到你自己的终端里粘上，回车 —— 就进去了

进去之后你面对的就是一台干净的 Ubuntu：
2 核 CPU、7G 内存、40G 盘，`sudo` 能用，随便 `apt install`。
想装什么装什么，跑完到时间机器自动销毁，什么都不留。

> 连接串是公开可连的（配置里没锁人），别往外贴。
> 想只让自己连，把 `tmate-shell.yml` 里的 `limit-access-to-actor: false` 改成 `true`。

**单个任务最长 350 分钟**（约 5.8 小时），到点自动回收。要续就再点一次 Run workflow。

---

## 四、跑自己的任务

改 `scripts/hello.py` 里的 `some_work()`，换成你要干的事，其他都不用动。

三种触发方式，任选：

- **手动跑**：Actions → **手动跑命令** → Run workflow，在输入框里填命令，比如
  `python scripts/hello.py` 或 `ffmpeg -i in.mp4 out.mp4`
- **定时跑**：已经配好每 6 小时一次（`cron-task.yml` 里的 `cron: '0 */6 * * *'`，UTC 时间，想改直接改这行）
- **推代码就跑**：往仓库 push 就触发，看 `build-matrix.yml` 的配置

跑完的结果去哪看：

- 任务页面底下的 **Artifacts** 里有 `output-*` 压缩包，下载就是产出
- 定时任务还会把 `output/` 和 `data/` 自动 commit 回仓库，攒的历史数据直接在仓库里看

依赖写在 `scripts/requirements.txt`，workflow 会自动 `pip install`。

---

## 五、编译三平台版本

Actions → **三平台编译** → Run workflow。

会同时起三台机器，各自编译，最后给你三个包：

- `bin-linux-x64`
- `bin-windows-x64`
- `bin-macos-arm64`

示例用的是 PyInstaller 把 Python 脚本打成单文件程序。跑 C/C++、Go、Rust 也一样，
把编译那一步换成对应的命令就行（`gcc`、`go build`、`cargo build` 这些机器上都现成有）。

---

## 六、注意事项（说实话的部分）

- **不是一台常驻服务器**。跑完就销毁，没有固定公网 IP，不能从外面长期连进去。
  要长期常驻的，去看 Oracle Cloud 的永久免费 ARM 机器（4 核 24G），那个才是真 VPS。
- **别拿它挖矿或长期跑无关任务**。GitHub 会识别，账号会封。
  拿来跑自己的正经活、编译、爬数据、算东西都没问题。
- **公开仓库的代码谁都能看**。别往里放密码、API key、私钥。
  要用密钥就存到仓库的 Settings → Secrets and variables → Actions 里，代码里用 `${{ secrets.XXX }}` 取。
- **定时任务不准点**。GitHub 的 cron 在高峰期会延迟几分钟到几十分钟，要求精确定时的话别指望它。
- **私有仓库要花额度**。Free 计划每月 $12 的算力额度，Linux 2 核差不多 2000 分钟，用超了要等下个月或者开公开仓库。

---

## 七、Codespaces（想要一台长期在的开发机）

仓库页面上点绿色的 **Code** 按钮 → **Codespaces** 标签 → **Create codespace on main**。

浏览器里直接开出完整的 VS Code，带终端，能装东西、能跑服务、能转发端口。
Free 账号每月 120 核时的额度，开 2 核的机器就是约 60 小时。

**省额度的关键**：用完立刻在 codespaces 页面点 **Stop**，别让它挂着空跑。
闲置超时也可以在设置里调短（默认 30 分钟）。

---

## 八、Windows 免费机（浏览器里直接开桌面）

工作流：`.github/workflows/windows-box.yml`，名字是 **Windows 免费机**。

跑起来是一台 **Windows Server 2022**：4 核 / 16G 内存 / 14G 盘，
公仓免费不限分钟，单次最长约 5 小时 50 分，到点整机销毁。

点 **Actions → Windows 免费机 → Run workflow**：
- `minutes` 填存活分钟数（最大 350）
- `password` 留空就自动生成一个

1~2 分钟后，**Summary** 里和**Issues**（标题 `WINBOX` 开头）里都会贴出入口：

1. **浏览器桌面**：`https://xxxx.trycloudflare.com/vnc.html?...`，手机电脑都能开，不装东西
2. **远程桌面**：`mstsc` 里填 `bore.pub:xxxxx`，账号 `runneradmin`

两条别同时用，远程桌面一登会把本地会话顶掉。

它是服务器版系统：exe、常规软件、编译、脚本都能跑；
WSL2 / Docker / 商店 App 用不了（虚拟机里没有嵌套虚拟化）。
