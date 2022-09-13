# Videostreaming
## Vorbereitung
`sudo raspi-config` -> activate glamor and gl 2

`sudo iw wlan0 set power_save off` (`sudo iwconfig` -> power management should be off)

Preferences -> Raspberry Pi Configuration -> GPU Memory: 256

### To install for gstreamer
`sudo apt install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgstreamer-plugins-bad1.0-dev gstreamer1.0-plugins-ugly gstreamer1.0-tools gstreamer1.0-gl gstreamer1.0-gtk3 libgstrtspserver-1.0-0 libgstrtspserver-1.0-dev`


## Streaming versions

version 0 ffplay:

`ffplay tcp://localhost:4000 -vf "setpts=N/30" -fflags nobuffer -flags low_delay -framedrop`

`libcamera-vid -t 0 --rotation 180 -n --flush 1 --inline --listen -o tcp://0.0.0.0:4000`

version 1:

`gst-launch-1.0 libcamerasrc ! 'video/x-raw,width=1280,height=720' ! videoconvert ! jpegenc ! tcpserversink host=0.0.0.0 port=4000`

`gst-launch-1.0 tcpclientsrc host=127.0.0.1 port=4000 ! jpegdec ! videoconvert ! autovideosink`

version 2 rotation:

`gst-launch-1.0 libcamerasrc ! 'video/x-raw,width=640,height=480,framerate=30/1' ! videoflip method=rotate-180 ! videoconvert ! jpegenc ! tcpserversink host=0.0.0.0 port=4000`

version 3 udp:

`gst-launch-1.0 libcamerasrc ! 'video/x-raw,width=256,height=144,framerate=15/1' ! videoflip method=rotate-180 ! videoconvert ! jpegenc quality=70 ! rtpjpegpay ! udpsink host=0.0.0.0 port=4000`

`gst-launch-1.0 -v udpsrc port=4000 ! application/x-rtp, media=video, clock-rate=90000, payload=96 ! rtpjpegdepay ! jpegdec ! videoconvert ! autovideosink`

version 4 h264:

`gst-launch-1.0 libcamerasrc ! 'video/x-raw,width=256,height=144,framerate=15/1' ! videoflip method=rotate-180 ! x264enc tune=zerolatency ! rtph264pay ! udpsink host=0.0.0.0 port=4000`

`gst-launch-1.0 -v udpsrc port=4000 ! application/x-rtp, media=video, clock-rate=90000, payload=96 ! rtph264depay ! avdec_h264 ! autovideosink`

version 5 h264 hardware:

`gst-launch-1.0 libcamerasrc ! 'video/x-raw,width=256,height=144,framerate=15/1' ! videoflip method=rotate-180 ! v4l2convert ! v4l2h264enc ! 'video/x-h264,level=(string)3' ! rtph264pay ! udpsink host=0.0.0.0 port=4000`

`gst-launch-1.0 -v udpsrc port=4000 ! application/x-rtp, media=video, clock-rate=90000, payload=96 ! rtph264depay ! avdec_h264 ! autovideosink`

version 6 fix color:

`gst-launch-1.0 libcamerasrc ! 'video/x-raw,width=256,height=144,framerate=15/1,format=(string)UYVY' ! videoflip method=rotate-180 ! v4l2convert ! v4l2h264enc ! 'video/x-h264,level=(string)3' ! rtph264pay ! udpsink host=0.0.0.0 port=4000`

version 7 bitrate:

`gst-launch-1.0 libcamerasrc ! 'video/x-raw,width=256,height=144,framerate=15/1,format=(string)UYVY' ! videoflip method=rotate-180 ! v4l2convert ! v4l2h264enc extra-controls='controls,video_bitrate=200000' ! 'video/x-h264,level=(string)3' ! rtph264pay ! udpsink host=0.0.0.0 port=4000`

version 8 i-frames:

`gst-launch-1.0 libcamerasrc ! 'video/x-raw,width=256,height=144,framerate=15/1,format=(string)UYVY' ! v4l2convert ! v4l2h264enc extra-controls='controls,video_bitrate=200000,h264_i_frame_period=15' ! 'video/x-h264,level=(string)3' ! rtph264pay ! udpsink host=0.0.0.0 port=4000`

`gst-launch-1.0 rtspsrc location=rtsp://127.0.0.1:8554/cam latency=0 ! queue ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! autovideosink`

## Rtps server
get Pipelines and rtsp_server from stick into rtsp-server folder

### Sender: rtsp server
`cd rtsp-server` -> `./rtsp_server xxx.conf`

### Receiver (local): rtsp server
`ffplay -fflags nobuffer -flags low_delay -framedrop rtsp://127.0.0.1:8554/cam`
