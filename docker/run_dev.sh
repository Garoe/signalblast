#!/bin/bash
REPO_DIR=$(dirname $(dirname $(realpath $0)))

SIGNALBLAST_VERSION=$(uvx hatch version)
DOCKER_TAG="${SIGNALBLAST_VERSION//+/-}"

echo $REPO_DIR

docker run \
 --rm \
 -v $HOME/.local/share/signal-api/:/home/user/.local/share/signal-api/ \
 -v $REPO_DIR:/home/user/signalblast \
 --interactive=true \
 --tty=true \
 --entrypoint bash \
 --network host \
  eradorta/signalblast:$DOCKER_TAG