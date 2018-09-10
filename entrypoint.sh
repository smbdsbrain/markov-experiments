#!/usr/bin/env bash

set -e

# Choose command
case "$1" in
inv)
    shift
    exec invoke $@
    ;;
api)
    shift
    aioworkers -c config.yaml $@
    ;;
*) exec "$@"
esac