#!/usr/bin/env bash

# Environment variables
FLASK_ENV=development
export FLASK_ENV
export FLASK_APP=run.py
export FLASK_RUN_PORT=5001

source "./.scripts/cmd_options"

if [ $# -gt 0 ]; then
        probe_commands && cmd_options $@  || show_help exit 1
else
        show_help
fi
