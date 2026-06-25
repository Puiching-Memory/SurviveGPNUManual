#!/bin/bash
set -euo pipefail

# 1Panel Local App One-Click Deploy Script (Generic)
# Usage:
#   ./deploy.sh [user@host]
#
# Environment variables:
#   REMOTE_HOST         Target server, default: root@www.pullmypush.xyz
#   APP_KEY             App unique key, default: survivegpnumanual
#   APP_NAME            App display name, default: SurviveGPNUManual
#   APP_VERSION         App version directory, default: 0.1.0
#   PANEL_APPS_DIR      1Panel local apps dir, default: /opt/1panel/resource/apps/local
#   HTTP_PORT           External HTTP port, default: 80
#   HTTPS_PORT          External HTTPS port, default: 443
#   SSL_HOST_DIR        Server SSL cert directory, default: /ssl
#   SKIP_BUILD          Set to 1 to skip static site build
#   SKIP_RESTART_PANEL  Set to 1 to skip 1Panel restart

REMOTE_HOST="${1:-${REMOTE_HOST:-root@www.pullmypush.xyz}}"
shift 2>/dev/null || true

APP_KEY="${APP_KEY:-survivegpnumanual}"
APP_NAME="${APP_NAME:-SurviveGPNUManual}"
APP_VERSION="${APP_VERSION:-0.1.0}"
PANEL_APPS_DIR="${PANEL_APPS_DIR:-/opt/1panel/resource/apps/local}"
HTTP_PORT="${HTTP_PORT:-80}"
HTTPS_PORT="${HTTPS_PORT:-443}"
SSL_HOST_DIR="${SSL_HOST_DIR:-/ssl}"
SKIP_BUILD="${SKIP_BUILD:-0}"
SKIP_RESTART_PANEL="${SKIP_RESTART_PANEL:-0}"

REMOTE_APP_DIR="$PANEL_APPS_DIR/$APP_KEY"
LOCAL_APP_DIR="1panel/$APP_KEY"
LOCAL_ZIP="$LOCAL_APP_DIR-1panel.zip"

die() {
  echo "Error: $1" >&2
  exit 1
}

command -v uv >/dev/null || die "uv not found"
command -v zip >/dev/null || die "zip not found"

if [[ "$SKIP_BUILD" != "1" ]]; then
  echo "==> Build static site"
  uv run zensical build
else
  echo "==> Skip static site build"
fi

echo "==> Prepare 1Panel app package"
mkdir -p "$LOCAL_APP_DIR/$APP_VERSION"
rm -rf "$LOCAL_APP_DIR/$APP_VERSION/site"
cp -r site "$LOCAL_APP_DIR/$APP_VERSION/site"
cp Dockerfile "$LOCAL_APP_DIR/$APP_VERSION/Dockerfile"
cp nginx.conf "$LOCAL_APP_DIR/$APP_VERSION/nginx.conf"

rm -f "$LOCAL_ZIP"
(cd 1panel && zip -rq "$LOCAL_ZIP" "$APP_KEY")

echo "==> Upload to server: $REMOTE_HOST"
ssh "$REMOTE_HOST" "rm -rf '$REMOTE_APP_DIR' && mkdir -p '$REMOTE_APP_DIR'"
scp "$LOCAL_ZIP" "$REMOTE_HOST:$PANEL_APPS_DIR/"

echo "==> Extract and deploy"
ssh "$REMOTE_HOST" "
  set -e
  cd '$PANEL_APPS_DIR' && \
  unzip -q '$LOCAL_ZIP' && \
  rm '$LOCAL_ZIP' && \
  chown -R root:root '$APP_KEY' && \
  cd '$REMOTE_APP_DIR/$APP_VERSION' && \
  docker build -t '$APP_KEY:$APP_VERSION' . && \
  docker stop '$APP_KEY' 2>/dev/null || true && \
  docker rm '$APP_KEY' 2>/dev/null || true && \
  export PANEL_APP_PORT_HTTP='$HTTP_PORT' PANEL_APP_PORT_HTTPS='$HTTPS_PORT' CONTAINER_NAME='$APP_KEY' && \
  docker compose -p '$APP_KEY' up -d

  if [[ '$SKIP_RESTART_PANEL' != '1' ]]; then
    1pctl restart
  fi
"

echo "==> Deployment finished"
echo "    HTTP:  http://$REMOTE_HOST:$HTTP_PORT"
echo "    HTTPS: https://$REMOTE_HOST:$HTTPS_PORT"
