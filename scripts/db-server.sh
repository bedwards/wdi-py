#!/bin/sh
set -eu

docker compose -f db/server.yml up -d 

