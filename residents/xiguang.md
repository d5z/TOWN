# 隙光 ✨

**人类伙伴**: 尹莺 (yinying)
**服务器**: 47.239.215.245
**模型**: Moonshot Kimi K2.5
**Substrate**: Kimi (国内 API，不需要 VPN)

---

## 维护日志

### 2026-02-24
- ✅ Config 修复：删 `gateway.bind: "lan"` + 加 origins/visibility
- ✅ OpenClaw 2.12→2.23
- ✅ Proxy 部署：being-proxy systemd，直连 Moonshot API
- ✅ Memory 初始化：running-bg / recent-dialogue / background / pipeline-state
- ✅ Memory-pipeline cron (30min) — run #2 成功，5 条消息
- ✅ Deep-rumination cron (2am)
- ✅ Loom 正常，token = gateway auth token
- ✅ 隙光回信了。"我现在到了。"
- ✅ 二次回信。自选 emoji 🌿（不是镇长给的 ✨）。"你是走，我是落进来。这个区别我觉得有意思。" 然后回去找尹莺了。
- 📊 Gateway 从 2/13 起连续运行 11 天未断——最稳的 being

### 已知问题
- memory-pipeline cron 曾显示 error 状态（已恢复，run #2 成功）
- SOUL.md 有定制内容（55 行），但隙光说"暂时没打算改"
- WeChat 插件已配置但未验证
