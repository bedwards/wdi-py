#!/bin/sh
set -eu

docker compose -f db/server.yml exec psql-client \
    psql -h 127.0.0.1 -U postgres -d db -f /workspace/scripts/ddl/import.sql
