#!/bin/sh

CONNECT_DIR="/tmp/sauce-connect-$RANDOM"
CONNECT="eJRF/snap-ci/sauce.jar.zip"

mkdir -p $CONNECT_DIR
unzip $CONNECT -d $CONNECT_DIR
cd $CONNECT_DIR
java -jar sauce.jar --readyfile ready_file $SAUCE_USERNAME $SAUCE_ACCESS_KEY &

# Wait for Connect to be ready before exiting
while [ ! -f ready_file ]; do
  sleep .5
done