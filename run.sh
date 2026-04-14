#!/bin/sh
set -eu

PROJECT_DIR="/root/code/2libraAuto"
IMAGE_NAME="2libra-checkin"
CONTAINER_NAME="2libra-checkin-job"
COOKIE_FILE="$PROJECT_DIR/2libra_cookie.txt"

docker run --rm --name "$CONTAINER_NAME" -v "$COOKIE_FILE:/app/2libra_cookie.txt:ro" "$IMAGE_NAME"
