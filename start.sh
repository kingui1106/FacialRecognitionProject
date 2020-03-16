


#!/bin/sh

#This is Web-streaming server start up script.for raspi
#No warrantly.

STREAMER=/usr/local/bin/mjpg_streamer
DEVICE=/dev/video0
RESOLUTION=640x480
FRAMERATE=10
HTTP_PORT=8080

PLUGINPATH=/usr/lib

#$STREAMER -i "$PLUGINPATH/input_uvc.so -n -d $DEVICE -r $RESOLUTION -f $FRAMERATE" -o "$PLUGINPATH/output_http.so -n -p $HTTP_PORT " &
$STREAMER -i "$PLUGINPATH/input_uvc.so -n -d $DEVICE -r $RESOLUTION -f $FRAMERATE -y YUYV" -o "$PLUGINPATH/output_http.so -n -p $HTTP_PORT " &

echo “正在启动主程序”

#sudo python sunny.py --clientid=ae45ceff231057f6
sudo python index.py 80






