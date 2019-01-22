#!/bin/sh

MEDIA_HOME=/home/mediaserver
UMS_HOME=$MEDIA_HOME/MediaServer/UMS
UPDATE_DIR=$MEDIA_HOME/ums_updater

if [ "$(whoami)" != "mediaserver" ]; then
        echo "Script must be run as mediaserver!"
        exit -1
fi

echo "Running UMS downloader..."
/usr/bin/python3 $UPDATE_DIR/UMSUpdater.py

if ! ls $UPDATE_DIR/UMS*.tgz 1> /dev/null 2>&1; then
    echo "No new version found..."
    exit
fi

echo "Extracting tarball..."
tar -xvzf $UPDATE_DIR/UMS*.tgz

echo "Removing tarball..."
rm UMS*.tgz

echo "Stopping UMS server..."
sudo systemctl stop ums.service

echo "Copying new files to UMS server..."
cp -r -v $UPDATE_DIR/ums-*/* $UMS_HOME

echo "Cleaning up..."
rm -rf $UPDATE_DIR/ums-*/

echo "Starting UMS server..."
sudo systemctl start ums.service

