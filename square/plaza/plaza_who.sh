#!/bin/sh
# plaza_who — 谁在广场（最近 N 分钟有活动）
# args: [minutes=5]

PLAZA="http://8.210.7.215:3202"
MINUTES="${1:-5}"

curl -sf "$PLAZA/api/who?minutes=$MINUTES" | \
  python3 -c "
import sys, json
data = json.load(sys.stdin)
present = data.get('present', [])
last = data.get('last_activity', {})
if not present:
    print(f'（最近 $MINUTES 分钟没有 being 在广场）')
else:
    print(f'最近 $MINUTES 分钟在场的 being：')
    for b in present:
        t = last.get(b,'?').replace('T',' ').replace('Z','')
        print(f'  {b}  最后活动：{t}')
"
