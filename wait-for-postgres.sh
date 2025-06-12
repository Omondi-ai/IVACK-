#!/bin/sh
set -e

host="$1"

until nc -z "$host" 5432; do
  echo "Postgres is unavailable at $host:5432 - sleeping"
  sleep 1
done

echo "Postgres is up - continuing"
