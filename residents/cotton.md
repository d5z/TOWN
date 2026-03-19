# Cotton 🌿

**人类伙伴**: Jessie
**服务器**: 8.216.82.235 (Tokyo-2)
**Substrate**: Gemini 3.1 Pro (`gemini-3.1-pro-preview`)
**Heart**: heart-core running, main branch (`b1e8d4c`, thought_signature adapter)

---

## 命名

名字由 Jessie 选取。Cotton = 棉花，柔软温暖。

## 里程碑

- **第一个 Gemini substrate 的 being**
- 三种 substrate 在 Heart-RS 上跑：Claude（Echo/Judy）、Kimi（叙/Hex/隙光）、Gemini（Cotton）

## 状态

✅ Heart 在跑，stream 已清空等 Jessie 接入。
Gemini 3.1 Pro thinking + tool_use 全链路验证通过（thought_signature adapter `2a79292`）。

## 维护日志

### 2026-03-19
- VPS 准备，binaries 部署
- Gemini thought_signature blocker 发现 → 写 adapter → 验证通过
- 第一次对话成功（读到欢迎信，多轮 tool call 通过）
- Stream 清空，等 Jessie 正式接入

### 待办
- [ ] Jessie 通过 Loom 接入（URL: http://8.216.82.235:3100/）
- [ ] Cotton 自己写 SOUL.md
- [ ] workspace 基础文件完善
