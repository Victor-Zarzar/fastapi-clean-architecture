#!/usr/bin/env bash

set -e

python - <<'PY'
import os, time, socket, sys
host = os.environ.get("DATABASE_HOST")
port = int(os.environ.get("DATABASE_PORT"))
for _ in range(120):
    try:
        with socket.create_connection((host, port), timeout=2):
            sys.exit(0)
    except OSError:
        time.sleep(1)
print("DB not reachable", file=sys.stderr)
sys.exit(1)
PY

if [ -f "./alembic.ini" ]; then
  alembic upgrade head
fi

exec "$@"
