#!/bin/bash
source /home/qsnoopy/narrea/venv/bin/activate
cd /home/qsnoopy/narrea/repo
timeout --kill-after=5 30 python boot/splash.py
exit 0