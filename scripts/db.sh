#!/bin/sh
set -eu

host="studio"
commands=""

if [ $# -gt 0 ]; then
    commands="-f /workspace/$1"
fi

docker compose -f db/client.yml up -d 2>/dev/null

docker compose -f db/client.yml exec psql-client \
    psql -h "$host" -U postgres -d db $commands
