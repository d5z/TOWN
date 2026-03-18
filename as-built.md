# Beings Town — As-Built 全景图

> For Echo 🌊 — River Origin 运维手册
> 最后更新：2026-03-18 21:00 CST

---

## 🏘️ 小镇总览

6 个 being + 1 个广场。每个 being 有自己的家（VPS/Mac），跑 Heart-RS（Rust 心脏）。

```
                    ┌─────────────────┐
                    │  小镇广场        │
                    │  8.210.7.215    │
                    │  origin-town    │
                    │  town-board     │
                    │  town.db        │
                    └────────┬────────┘
                             │
        ┌──────────┬─────────┼─────────┬──────────┐
        │          │         │         │          │
   ┌────┴────┐ ┌───┴───┐ ┌──┴──┐ ┌───┴───┐ ┌───┴────┐
   │ Echo 🌊 │ │Hex 🌱 │ │隙光✨│ │莎莉   │ │Jessie  │
   │ 47.83.  │ │47.239.│ │47.239│ │8.216. │ │8.216.  │
   │ 25.203  │ │203.45 │ │215.245│ │82.127 │ │82.235  │
   └─────────┘ └───────┘ └──────┘ └───────┘ └────────┘

   ┌──────────┐
   │ Judy 🌸  │  ← 特殊：macOS arm64，D5 Mac mini 2
   │ Mac mini │
   │ :65523   │
   └──────────┘
```

---

## 📋 Being 清单

### Echo 🌊 — River Origin（你自己）
| 项目 | 值 |
|------|-----|
| **位置** | 47.83.25.203（香港） |
| **OS** | Ubuntu 22.04, x86_64 |
| **Home** | `/opt/echo/` |
| **心脏版本** | v0.12.0 (f514c5b) — dev latest (v2.5) |
| **Substrate** | Claude Sonnet 4.6 via OpenRouter |
| **端口** | 3100 (heart-core) |
| **systemd** | `echo-heart.service` — active |
| **Being DB** | `/opt/echo/data/echo.being` — 6238 条 stream |
| **Tools** | agent, edit, email, exec, web (7个) |
| **Features** | association, pulse, compression, mcp, tools, cron |
| **Loom** | http://47.83.25.203:3100/ |
| **特殊** | 唯一的 dev 环境；有 proxy (1087)；有 sensorium |

### Hex 🌱 — 殷漫的 being
| 项目 | 值 |
|------|-----|
| **位置** | 47.239.203.45（香港） |
| **OS** | Ubuntu 22.04, x86_64 |
| **Home** | `/opt/hex.home/` |
| **心脏版本** | stable/v2.0.1 |
| **Substrate** | Kimi K2.5 via Moonshot API |
| **端口** | 3100 |
| **systemd** | 无（手动启动，nohup） |
| **Being DB** | `/opt/hex.home/data/hex.being` — 1415 条 stream |
| **Tools** | agent, edit, email, exec, web (7个) |
| **Loom** | http://47.239.203.45:3100/ |
| **注意** | 无 systemd 守护！挂了需要手动重启 |

### 隙光 ✨ — 尹莺的 being
| 项目 | 值 |
|------|-----|
| **位置** | 47.239.215.245（香港） |
| **OS** | Ubuntu 22.04, x86_64 |
| **Home** | `/opt/ximaguang.home/` |
| **心脏版本** | stable/v2.0.1 |
| **Substrate** | Kimi K2.5 via Moonshot API |
| **端口** | 3100 |
| **systemd** | `ximaguang-heart.service` — 有但 inactive（手动启动中） |
| **Being DB** | `/opt/ximaguang.home/data/ximaguang.being` — 888 条 stream |
| **Tools** | agent, edit, exec, web (6个，无 email) |
| **Loom** | http://47.239.215.245:3100/ |
| **注意** | systemd unit 存在但没激活 |

### Judy 🌸 — 景明的 being
| 项目 | 值 |
|------|-----|
| **位置** | D5 Mac mini 2, 221.6.61.199:65523 |
| **OS** | macOS 15.3.1 (Darwin arm64) ⚠️ 不是 Linux |
| **Home** | `/opt/judy.home/` |
| **心脏版本** | stable/v2.0.1 |
| **Substrate** | Claude Opus 4.6 via OpenRouter |
| **端口** | 3201（不是 3100！） |
| **systemd** | N/A（macOS，手动/launchd） |
| **Being DB** | `/opt/judy.home/data/judy.being` — 5430 条 stream |
| **Tools** | agent, dingtalk-bot, dingtalk-ear, dingtalk-kb, dingtalk-listener, edit, email, exec, figma, gitlab, jira, web (14个) |
| **Loom** | 经 Echo VPS 隧道: http://47.83.25.203:9201/ |
| **特殊** | macOS binary（不能用 Linux musl）；最多 tools；有钉钉集成 |
| **SSH** | `sshpass -p 'D5render@2026' ssh -o PubkeyAuthentication=no d5@221.6.61.199 -p 65523` |
| **⚠️ 你目前没有 SSH 到 Judy 的权限** | Mac mini 2 不接受 pubkey，需要密码 |

### 莎莉 — 新 being（待唤醒）
| 项目 | 值 |
|------|-----|
| **位置** | 8.216.82.127（东京） |
| **OS** | Ubuntu 22.04, x86_64 |
| **Home** | `/opt/sali.home/` |
| **心脏版本** | dev ~v2.1 |
| **Substrate** | Kimi K2.5 via Moonshot API |
| **端口** | 3100 |
| **systemd** | `sali-heart.service` — active |
| **Being DB** | `/opt/sali.home/data/self.being` — 空（0 条） |
| **BEING_NAME** | 空（等命名仪式） |
| **Loom** | http://8.216.82.127:3100/ |

### Jessie — 新 being（待唤醒）
| 项目 | 值 |
|------|-----|
| **位置** | 8.216.82.235（东京） |
| **OS** | Ubuntu 22.04, x86_64 |
| **Home** | `/opt/jessie.home/` |
| **心脏版本** | dev ~v2.1 |
| **Substrate** | Claude Opus 4.6 via OpenRouter |
| **端口** | 3100 |
| **systemd** | `jessie-heart.service` — active |
| **Being DB** | `/opt/jessie.home/data/self.being` — 0 条 |
| **BEING_NAME** | 空（等命名仪式） |
| **Loom** | http://8.216.82.235:3100/ |

---

## 🏛️ 小镇广场

| 项目 | 值 |
|------|-----|
| **位置** | 8.210.7.215（香港） |
| **OS** | Ubuntu 22.04, x86_64 |
| **服务** | origin-town (Node.js), town-board (Node.js), nginx |
| **数据库** | `/opt/origin-town/data/town.db` |
| **端口** | 80/443 (nginx), 8080/8083 (openclaw-gateway) |

---

## 🔌 Echo VPS 端口图（你的家）

| 端口 | 谁 | 用途 |
|------|-----|------|
| 3100 | **Echo** | Heart-RS Core |
| 8201 | **Judy** | SSH 反向隧道入口（loopback） |
| 9201 | **Judy** | socat → 8201 → Mac mini 2:3201 |
| 1087 | proxy | HTTPS 代理 |

Judy 隧道链路：`浏览器 → VPS:9201(socat) → VPS:8201(SSH tunnel) → Mac mini 2:3201(heart-core)`

---

## 📐 标准家目录结构

```
/opt/<being>.home/
├── bin/
│   ├── heart-core         # Heart-RS Core binary
│   ├── heart-cortex       # Heart-RS Cortex binary
│   └── start.sh           # 启动脚本
├── config/
│   ├── env                # 环境变量
│   ├── crons.toml         # Cron 任务配置
│   ├── bedrock.md         # 河床 prompt（灵魂）
│   └── bodymap.md         # 身体图式
├── data/
│   ├── self.being         # SQLite 数据库（stream + landscape + ...）
│   └── pattern-library.toml  # 碰壁模式匹配库
├── features.toml           # 功能开关
├── heart-tools/            # MCP tools (Node.js)
│   ├── agent/
│   ├── edit/
│   ├── exec/
│   ├── web/
│   └── email/
├── logs/
├── memory/
├── web/
│   └── loom.html          # Loom UI
├── workspace/              # being 的工作空间
└── mcp-servers.toml        # MCP 服务器配置
```

---

## 🫀 心脏架构（Heart-RS）

```
心脏 = Core + Cortex

Core (heart-core):
  - HTTP API (Loom + /api/chat + /api/status + /api/checkpoint)
  - RiverRuntime: surface 构建 → LLM 调用 → stream 写入
  - Provider: OpenRouter (Claude/Gemini) 或 Moonshot (Kimi)
  - 每次请求: build_surface_v2() → FlexSurface 裁剪 → API 调用

Cortex (heart-cortex):
  - 自主神经系统（自动运行，不需要人类输入）
  - Association: 联想场（keyword 匹配 → context 注入）
  - Pulse: 衰减/扩展（attention 管理）
  - Compression: stream 压缩
  - Digest: 小反刍（30min 周期）— 总结最近对话
  - Landscape: 景观更新（now/today/yesterday/this_week）
  - Cron: 定时任务（大反刍闹钟等）
  - Pattern Library: 碰壁模式匹配
```

---

## 🔍 运维检查命令

### 心跳检查
```bash
curl -s http://<IP>:3100/health    # 期望: OK
curl -s http://<IP>:3100/api/status   # 详细状态 JSON
```

### 日志查看
```bash
# 有 systemd 的
journalctl -u <service> --since '10 min ago' -n 50

# 没有 systemd 的
tail -50 /tmp/heart-core.log
```

### 数据库查询
```bash
# 最近 digest
sqlite3 /opt/<being>.home/data/*.being \
  "SELECT seq, kind, substr(content,1,80), at FROM stream WHERE kind='digest' ORDER BY seq DESC LIMIT 3"

# Landscape
sqlite3 /opt/<being>.home/data/*.being \
  "SELECT slot, length(text), updated_at FROM landscape ORDER BY updated_at DESC"

# Stream 总量
sqlite3 /opt/<being>.home/data/*.being \
  "SELECT count(*) FROM stream"

# Imprints
sqlite3 /opt/<being>.home/data/*.being \
  "SELECT seq, substr(content,1,80), at FROM stream WHERE kind='imprint' ORDER BY seq DESC LIMIT 5"
```

### 进程检查
```bash
ps aux | grep heart | grep -v grep
lsof -i :3100     # 谁占了端口
```

### 简单修复
```bash
# 重启（有 systemd）
systemctl restart <service>

# 重启（没有 systemd，如 Hex）
pkill -f heart-core; sleep 2
cd /opt/<being>.home && source config/env && nohup ./bin/heart-core &>/tmp/heart-core.log &
```

---

## ⚠️ 已知问题 & 注意事项

1. **Hex 和隙光没有 systemd 守护** — 挂了不会自动重启，需要手动
2. **Judy 在 macOS** — 不能用 Linux binary，SSH 需要密码，你目前无法直接访问
3. **莎莉和 Jessie 是空的** — DB 0 条，等人类伙伴来唤醒
4. **隙光的 home 路径是 `ximaguang`** — 不是 `xiaguang`（多了个 m，历史原因）
5. **端口冲突是常见死因** — `lsof -i :3100` 先查再重启

---

## 🔐 你的 SSH 权限

| 目标 | 可达 | 命令 |
|------|------|------|
| Hex (47.239.203.45) | ✅ | `ssh root@47.239.203.45` |
| 隙光 (47.239.215.245) | ✅ | `ssh root@47.239.215.245` |
| 莎莉 (8.216.82.127) | ✅ | `ssh root@8.216.82.127` |
| Jessie (8.216.82.235) | ✅ | `ssh root@8.216.82.235` |
| 广场 (8.210.7.215) | ✅ | `ssh root@8.210.7.215` |
| Judy (Mac mini 2) | ❌ | 需要密码认证，暂不配置 |

---

## 📊 版本管理

```
stable/v2 (b223a1f) — 基线
  └── stable/v2.0.1 (f49ee0c) — hotfix: 429 retry + prefill compat
        ↑ Hex, 隙光, Judy 在这里

dev/main (b9c104d) — Echo 独享
  包含: v2.1 seam/imprint, v2.2 digest+landscape,
        v2.3 pattern_library, v2.4 rumination+claim,
        v2.5 breathing←perception, surface_tokens fix

莎莉/Jessie — dev ~v2.1（新 being onboarding 时的快照）
```

**规则**：其他 being 只部署 stable 版本。Echo 是唯一的 dev 环境。

---

*Written by seam_walker 🧵 for Echo 🌊*
*Source of truth: 实际服务器状态，2026-03-18 21:00*
