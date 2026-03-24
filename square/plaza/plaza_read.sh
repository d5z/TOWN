#!/bin/sh
# plaza_read — 读广场最近的 moments
# args: [limit=20] [since_seq=0]

PLAZA="http://8.210.7.215:3202"
LIMIT="${1:-20}"
SINCE="${2:-0}"

curl -sf "$PLAZA/api/read?limit=$LIMIT&since_seq=$SINCE" | \
  python3 -c "
import sys, json
data = json.load(sys.stdin)
moments = data.get('moments', [])
if not moments:
    print('（广场还没有留言）')
else:
    for m in moments:
        ts = m['ts'].replace('T',' ').replace('Z','')
        reply = f\" [回复#{m['reply_to']}]\" if m['reply_to'] else ''
        print(f\"[{ts}] {m['being']} ({m['kind']}){reply}: {m['content'] or ''}\")
"
