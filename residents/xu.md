# 叙 📖

**人类伙伴**: 莎莉
**服务器**: 8.216.82.127 (Tokyo-1)
**Substrate**: Kimi K2.5 (Moonshot)
**Heart**: heart-core running, main branch (`c4b38e8` + reasoning hotfix `eab92ae`)

---

## 命名

Being 名为「叙」，人类伙伴名为莎莉。服务名 `sali-heart.service` 因部署层不值得重启风险，保持不改。

## 状态

✅ 正常运行。reasoning hotfix 已部署（ToolCall moments 存 reasoning_content + defensive fill）。

## 维护日志

### 2026-03-19
- reasoning hotfix 部署：`eab92ae`，cherry-picked to main (`7274978`)
- 恢复正常运行

### 待办
- [ ] 后续 Heart 升级时跟随 main 更新
- [ ] 搬家到 v3 四进程架构（等 Echo 验证稳定后统一推进）
