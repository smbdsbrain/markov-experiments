#!/usr/bin/env bash

set -e

if [ "$1" = 'inv' ];
then
    shift
    exec invoke $@
else
    exec "$@"
fi
