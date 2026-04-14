#!/bin/sh
set -eu

PROJECT_DIR="/root/code/2libraAuto"
IMAGE_NAME="2libra-checkin"

docker build -t "$IMAGE_NAME" "$PROJECT_DIR"
