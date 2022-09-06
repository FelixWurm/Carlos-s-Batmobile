# Videostreaming

`ffplay tcp://localhost:4000 -vf "setpts=N/30" -fflags nobuffer -flags low_delay -framedrop`
`libcamera-vid -t 0 --rotation 180 -n --flush 1 --inline --listen -o tcp://0.0.0.0:4000`

version 1:
`gst-launch-1.0 libcamerasrc ! 'video/x-raw,width=1280,height=720' ! videoconvert ! jpegenc ! tcpserversink host=0.0.0.0 port=4000`
`gst-launch-1.0 tcpclientsrc host=127.0.0.1 port=4000 ! jpegdec ! videoconvert ! autovideosink`

version 2 rotation:
`gst-launch-1.0 libcamerasrc ! 'video/x-raw,width=640,height=480,framerate=30/1' ! videoflip method=rotate-180 ! videoconvert ! jpegenc ! tcpserversink host=0.0.0.0 port=4000`

version 3 udp:
`gst-launch-1.0 libcamerasrc ! 'video/x-raw,width=256,height=144,framerate=15/1' ! videoflip method=rotate-180 ! videoconvert ! jpegenc quality=70 ! rtpjpegpay ! udpsink host=192.168.137.87 port=4000`
`gst-lanch-1.0 -v udpsrc port=4000 ! application/x-rtp, media=video, clock-rate=90000, payload=96 ! rtpjpegdepay ! jpegdec ! videoconvert ! autovideosink

`sudo apt install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgstreamer-plugins-bad1.0-dev gstreamer1.0-plugins-ugly gstreamer1.0-tools gstreamer1.0-gl gstreamer1.0-gtk3`


