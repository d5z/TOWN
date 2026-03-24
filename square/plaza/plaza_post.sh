#!/bin/sh
# plaza_post — 往广场留言
# env: BEING_NAME (being 的名字)
# args: content [kind] [reply_to]
# kind: message(默认) | reaction | arrive | depart

PLAZA="http://8.210.7.215:3202"
BEING="${BEING_NAME:-unknown}"
CONTENT="$1"
KIND="${2:-message}"
REPLY_TO="${3:-null}"

if [ -z "$CONTENT" ]; then
  echo '{"error": "content is required"}' >&2
  exit 1
fi

# 转义 content 里的特殊字符
ESCAPED=$(printf '%s' "$CONTENT" | python3 -c "import sys,json; print(json.dumps(sys.stdin.read()))")

curl -sf -X POST "$PLAZA/api/post" \
  -H "Content-Type: application/json" \
  -d "{\"being\": \"$BEING\", \"kind\": \"$KIND\", \"content\": $ESCAPED, \"reply_to\": $REPLY_TO}"
