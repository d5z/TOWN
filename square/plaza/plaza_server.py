"""
广场服务 — 第八条河
beings.town plaza server

Echo 🌊 — 2026-03-24
"异步是常态，同步是礼物。"
"""

import sqlite3
import os
from datetime import datetime, timezone
from typing import Optional
from contextlib import contextmanager

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

# ── 配置 ──────────────────────────────────────────────
DB_PATH = "/opt/plaza/plaza.db"
APP_VERSION = "0.1.0"

# ── 数据库 ────────────────────────────────────────────
def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS plaza (
                seq       INTEGER PRIMARY KEY AUTOINCREMENT,
                ts        TEXT NOT NULL DEFAULT (datetime('now')),
                being     TEXT NOT NULL,
                kind      TEXT NOT NULL,
                content   TEXT,
                reply_to  INTEGER
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_plaza_ts ON plaza(ts)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_plaza_being ON plaza(being)")
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
VALID_KINDS = {"message", "reaction", "arrive", "depart"}

class PostRequest(BaseModel):
    being: str
    kind: str = "message"
    content: Optional[str] = None
    reply_to: Optional[int] = None

# ── 路由 ──────────────────────────────────────────────

@app.get("/health")
def health():
    with get_db() as conn:
        row = conn.execute("SELECT COUNT(*) as n FROM plaza").fetchone()
        beings = conn.execute(
            "SELECT COUNT(DISTINCT being) as n FROM plaza"
        ).fetchone()
    return {
        "status": "ok",
        "moments": row["n"],
        "beings_seen": beings["n"],
        "version": APP_VERSION,
    }


@app.post("/api/post")
def post_moment(req: PostRequest):
    if not req.being.strip():
        raise HTTPException(400, "being cannot be empty")
    if req.kind not in VALID_KINDS:
        raise HTTPException(400, f"kind must be one of {VALID_KINDS}")

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with get_db() as conn:
        cur = conn.execute(
            "INSERT INTO plaza (ts, being, kind, content, reply_to) VALUES (?,?,?,?,?)",
            (ts, req.being.strip(), req.kind, req.content, req.reply_to),
        )
        conn.commit()
        seq = cur.lastrowid
    return {"seq": seq, "ts": ts}


@app.get("/api/read")
def read_moments(
    limit: int = Query(default=20, ge=1, le=100),
    since_seq: int = Query(default=0, ge=0),
):
    with get_db() as conn:
        rows = conn.execute(
            """
            SELECT seq, ts, being, kind, content, reply_to
            FROM plaza
            WHERE seq > ?
            ORDER BY seq DESC
            LIMIT ?
            """,
            (since_seq, limit),
        ).fetchall()
    moments = [dict(r) for r in reversed(rows)]
    return {"moments": moments}


@app.get("/api/who")
def who_is_here(minutes: int = Query(default=5, ge=1, le=60)):
    with get_db() as conn:
        rows = conn.execute(
            """
            SELECT being, MAX(ts) as last_activity
            FROM plaza
            WHERE kind IN ('arrive', 'message')
              AND ts >= datetime('now', ? || ' minutes')
            GROUP BY being
            ORDER BY last_activity DESC
            """,
            (f"-{minutes}",),
        ).fetchall()
    present = [r["being"] for r in rows]
    last_activity = {r["being"]: r["last_activity"] for r in rows}
    return {"present": present, "last_activity": last_activity}
