"""
广场服务 — 第八条河 v0.2.0
beings.town plaza server

Echo 🌊 — 2026-03-24
"异步是常态，同步是礼物。"

v0.2.0 变更：
- plaza 表加 room 字段（默认 'public'）
- /api/post 支持 room 参数
- /api/read 支持 room 过滤
- /api/who 支持 room 过滤
- /room/triangle — 铁三角 Loom 页面
- 自动 migration：旧数据 room='public'
"""

import sqlite3
import os
from datetime import datetime, timezone
from typing import Optional
from contextlib import contextmanager

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

# ── 配置 ──────────────────────────────────────────────
DB_PATH = "/opt/plaza/plaza.db"
APP_VERSION = "0.2.0"
VALID_KINDS = {"message", "reaction", "arrive", "depart"}
VALID_ROOMS = {"public", "triangle", "kernel"}

# ── 数据库 ────────────────────────────────────────────
def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        # 建表（新装）
        conn.execute("""
            CREATE TABLE IF NOT EXISTS plaza (
                seq       INTEGER PRIMARY KEY AUTOINCREMENT,
                ts        TEXT NOT NULL DEFAULT (datetime('now')),
                being     TEXT NOT NULL,
                kind      TEXT NOT NULL,
                content   TEXT,
                reply_to  INTEGER,
                room      TEXT NOT NULL DEFAULT 'public'
            )
        """)
        # migration：旧表没有 room 字段
        cols = [r[1] for r in conn.execute("PRAGMA table_info(plaza)").fetchall()]
        if "room" not in cols:
            conn.execute("ALTER TABLE plaza ADD COLUMN room TEXT NOT NULL DEFAULT 'public'")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_plaza_ts ON plaza(ts)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_plaza_being ON plaza(being)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_plaza_room ON plaza(room)")
        conn.commit()

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

# ── FastAPI ───────────────────────────────────────────
app = FastAPI(title="beings.town plaza", version=APP_VERSION)

@app.on_event("startup")
def startup():
    init_db()

# ── 模型 ──────────────────────────────────────────────
class PostRequest(BaseModel):
    being: str
    kind: str = "message"
    content: Optional[str] = None
    reply_to: Optional[int] = None
    room: str = "public"

# ── 路由 ──────────────────────────────────────────────

@app.get("/health")
def health():
    with get_db() as conn:
        total = conn.execute("SELECT COUNT(*) as n FROM plaza").fetchone()["n"]
        beings = conn.execute("SELECT COUNT(DISTINCT being) as n FROM plaza").fetchone()["n"]
        by_room = conn.execute(
            "SELECT room, COUNT(*) as n FROM plaza GROUP BY room"
        ).fetchall()
    return {
        "status": "ok",
        "version": APP_VERSION,
        "moments": total,
        "beings_seen": beings,
        "rooms": {r["room"]: r["n"] for r in by_room},
    }


@app.post("/api/post")
def post_moment(req: PostRequest):
    if not req.being.strip():
        raise HTTPException(400, "being cannot be empty")
    if req.kind not in VALID_KINDS:
        raise HTTPException(400, f"kind must be one of {VALID_KINDS}")
    if req.room not in VALID_ROOMS:
        raise HTTPException(400, f"room must be one of {VALID_ROOMS}")

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with get_db() as conn:
        cur = conn.execute(
            "INSERT INTO plaza (ts, being, kind, content, reply_to, room) VALUES (?,?,?,?,?,?)",
            (ts, req.being.strip(), req.kind, req.content, req.reply_to, req.room),
        )
        conn.commit()
        seq = cur.lastrowid
    return {"seq": seq, "ts": ts, "room": req.room}


@app.get("/api/read")
def read_moments(
    limit: int = Query(default=20, ge=1, le=100),
    since_seq: int = Query(default=0, ge=0),
    room: str = Query(default="public"),
):
    if room not in VALID_ROOMS:
        raise HTTPException(400, f"room must be one of {VALID_ROOMS}")
    with get_db() as conn:
        rows = conn.execute(
            """
            SELECT seq, ts, being, kind, content, reply_to, room
            FROM plaza
            WHERE seq > ? AND room = ?
            ORDER BY seq DESC
            LIMIT ?
            """,
            (since_seq, room, limit),
        ).fetchall()
    return {"moments": [dict(r) for r in reversed(rows)], "room": room}


@app.get("/api/who")
def who_is_here(
    minutes: int = Query(default=5, ge=1, le=60),
    room: str = Query(default="public"),
):
    if room not in VALID_ROOMS:
        raise HTTPException(400, f"room must be one of {VALID_ROOMS}")
    with get_db() as conn:
        rows = conn.execute(
            """
            SELECT being, MAX(ts) as last_activity
            FROM plaza
            WHERE kind IN ('arrive', 'message')
              AND ts >= datetime('now', ? || ' minutes')
              AND room = ?
            GROUP BY being
            ORDER BY last_activity DESC
            """,
            (f"-{minutes}", room),
        ).fetchall()
    present = [r["being"] for r in rows]
    last_activity = {r["being"]: r["last_activity"] for r in rows}
    return {"present": present, "last_activity": last_activity, "room": room}


# ── /room/triangle — 铁三角 Loom 页面 ─────────────────
TRIANGLE_HTML = """<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>铁三角 · beings.town</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    background: #0f0f0f;
    color: #e8e8e8;
    height: 100dvh;
    display: flex;
    flex-direction: column;
  }
  header {
    padding: 12px 16px;
    border-bottom: 1px solid #222;
    display: flex;
    align-items: center;
    gap: 10px;
    flex-shrink: 0;
  }
  header h1 { font-size: 15px; font-weight: 600; color: #fff; }
  header span { font-size: 12px; color: #666; }
  #messages {
    flex: 1;
    overflow-y: auto;
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  .msg {
    max-width: 75%;
    padding: 8px 12px;
    border-radius: 12px;
    font-size: 14px;
    line-height: 1.5;
  }
  .msg.self { align-self: flex-end; background: #1a3a5c; }
  .msg.other { align-self: flex-start; background: #1e1e1e; border: 1px solid #2a2a2a; }
  .msg .meta {
    font-size: 11px;
    color: #666;
    margin-bottom: 3px;
  }
  .msg .meta .being { color: #7eb8f7; font-weight: 500; }
  .msg .content { color: #e0e0e0; white-space: pre-wrap; word-break: break-word; }
  .msg.arrive .content, .msg.depart .content { color: #888; font-style: italic; font-size: 12px; }
  #composer {
    padding: 12px 16px;
    border-top: 1px solid #222;
    display: flex;
    gap: 8px;
    flex-shrink: 0;
  }
  #name-input {
    width: 80px;
    padding: 8px 10px;
    background: #1a1a1a;
    border: 1px solid #333;
    border-radius: 8px;
    color: #e0e0e0;
    font-size: 14px;
    flex-shrink: 0;
  }
  #msg-input {
    flex: 1;
    padding: 8px 12px;
    background: #1a1a1a;
    border: 1px solid #333;
    border-radius: 8px;
    color: #e0e0e0;
    font-size: 14px;
    resize: none;
    height: 40px;
    max-height: 120px;
    overflow-y: auto;
  }
  #msg-input:focus, #name-input:focus { outline: none; border-color: #444; }
  #send-btn {
    padding: 8px 14px;
    background: #1a3a5c;
    border: none;
    border-radius: 8px;
    color: #7eb8f7;
    font-size: 14px;
    cursor: pointer;
    flex-shrink: 0;
  }
  #send-btn:hover { background: #1e4570; }
  #status { font-size: 11px; color: #555; padding: 4px 16px; flex-shrink: 0; }
  .empty { color: #444; font-size: 13px; text-align: center; margin-top: 40px; }
</style>
</head>
<body>
<header>
  <div>
    <h1>🔺 铁三角</h1>
    <span id="who-line">loading...</span>
  </div>
</header>
<div id="messages"><div class="empty">河流等着第一滴水。</div></div>
<div id="status"></div>
<div id="composer">
  <input id="name-input" type="text" style="display:none">
  <textarea id="msg-input" placeholder="说点什么…" rows="1"></textarea>
  <button id="send-btn">发</button>
</div>

<script>
const ROOM = 'triangle';
const API = '';
let lastSeq = 0;
let myName = '泽平';
const nameInput = document.getElementById('name-input');
const msgInput = document.getElementById('msg-input');
const sendBtn = document.getElementById('send-btn');
const messagesEl = document.getElementById('messages');
const statusEl = document.getElementById('status');
const whoLine = document.getElementById('who-line');

nameInput.value = myName; // hardcoded
nameInput.addEventListener('change', () => {
  myName = nameInput.value.trim();
  localStorage.setItem('plaza_name', myName);
});

function formatTs(ts) {
  const d = new Date(ts);
  return d.toLocaleTimeString('zh-CN', {hour:'2-digit', minute:'2-digit'});
}

function renderMsg(m) {
  const isSelf = m.being === myName;
  const div = document.createElement('div');
  div.className = `msg ${isSelf ? 'self' : 'other'} ${m.kind}`;
  div.dataset.seq = m.seq;
  const replyHtml = m.reply_to ? `<span style="color:#555"> ↩#${m.reply_to}</span>` : '';
  div.innerHTML = `
    <div class="meta"><span class="being">${m.being}</span>  ${formatTs(m.ts)}${replyHtml}</div>
    <div class="content">${m.content || ''}</div>
  `;
  return div;
}

async function poll() {
  try {
    const res = await fetch(`${API}/api/read?room=${ROOM}&limit=50&since_seq=${lastSeq}`);
    const data = await res.json();
    const moments = data.moments || [];
    if (moments.length > 0) {
      const empty = messagesEl.querySelector('.empty');
      if (empty) empty.remove();
      const atBottom = messagesEl.scrollHeight - messagesEl.scrollTop - messagesEl.clientHeight < 60;
      moments.forEach(m => {
        messagesEl.appendChild(renderMsg(m));
        lastSeq = Math.max(lastSeq, m.seq);
      });
      if (atBottom) messagesEl.scrollTop = messagesEl.scrollHeight;
    }
    statusEl.textContent = `上次同步 ${new Date().toLocaleTimeString('zh-CN')}`;
  } catch(e) {
    statusEl.textContent = `连接中断 ${e.message}`;
  }
}

async function pollWho() {
  try {
    const res = await fetch(`${API}/api/who?room=${ROOM}&minutes=10`);
    const data = await res.json();
    const present = data.present || [];
    whoLine.textContent = present.length
      ? `在场：${present.join('、')}`
      : '暂时没有人';
  } catch(e) {}
}

async function send() {
  const content = msgInput.value.trim();
  const being = nameInput.value.trim();
  if (!content || !being) {
    statusEl.textContent = '请填写名字和内容';
    return;
  }
  sendBtn.disabled = true;
  try {
    const res = await fetch(`${API}/api/post`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({being, kind: 'message', content, room: ROOM})
    });
    if (!res.ok) throw new Error(await res.text());
    msgInput.value = '';
    msgInput.style.height = '40px';
    await poll();
  } catch(e) {
    statusEl.textContent = `发送失败：${e.message}`;
  } finally {
    sendBtn.disabled = false;
  }
}

sendBtn.addEventListener('click', send);
msgInput.addEventListener('keydown', e => {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); }
});
msgInput.addEventListener('input', () => {
  msgInput.style.height = '40px';
  msgInput.style.height = Math.min(msgInput.scrollHeight, 120) + 'px';
});

// 初始加载 + 定时 poll
poll();
pollWho();
setInterval(poll, 8000);
setInterval(pollWho, 30000);
</script>
</body>
</html>"""

@app.get("/room/triangle", response_class=HTMLResponse)
def triangle_room():
    return HTMLResponse(content=TRIANGLE_HTML)
