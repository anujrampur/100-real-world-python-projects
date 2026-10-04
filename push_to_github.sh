#!/bin/bash
# 1) Create an EMPTY repository named 100-real-world-python-projects on github.com (no README, no license).
# 2) Replace YOUR_USERNAME below, then run:  bash push_to_github.sh
set -e
USER_NAME="YOUR_USERNAME"
git init
git add .
git commit -m "Add source code for 100 Real-World Python Projects"
git branch -M main
git remote add origin https://github.com/$USER_NAME/100-real-world-python-projects.git
git push -u origin main
