# VMAF
### Install Meson + Ninja:
`sudo apt-get install ninja-build meson`

### Install VMAF SDK
[Latest VMAF SDK](github.com/Netflix/vmaf/releases) -> unpack

`cd vmaf-x.x.x/libvmaf`

`meson build --buildtype release`

`ninja -vC build`

`ninja -vC build install`

### Install ffmpeg with libvmaf
[Source ffmpeg](ffmpeg.org/download.html) -> unpack

`cd ffmpeg`

`./configure --enable-libvmaf`

`sudo make -j4`

`sudo make install`

`export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib/aarch64-linux-gnu`

-> if export doesnt work, you get an error message: `ffmpeg error while loading shared libraries`

## Run test video
[Test Video Github Repo](github.com/Netflix/cmaf_resource) -> move to vmaf-2.3.1 and unpack (renamed in ressource_test here)

`ffmpeg
  -video_size 576x324 -r 24 -pixel_format yuv420p -i VMAF/vmaf-2.3.1/resource_test/yuv/src01_hrc00_576x324.yuv
  -video_size 576x324 -r 24 -pixel_format yuv420p -i VMAF/vmaf-2.3.1/resource_test/yuv/src01_hrc01_576x324.yuv
  -lavfi
    "[0:v]setpts=PTS-STARTPTS[reference];
    [1:v]setpts=PTS-STARTPTS[distorted];
    [distorted][reference]libvmaf=log_fmt=xml:log_path=/home/pi/VMAF/log_latest_vmaf.xml:model='path=VMAF/vmaf-2.3.1/model/vmaf_v0.6.1.json':n_threads=4" -f null -`

### Options
(note: some formats dont have video_size or pixel_format -> those can be omitted)

`-video_size` set video size

if video-size differentiate (eg 480p and 288p) -> upscaling of 288p to 720x480 with bicubic 

`ffmpeg
  -r 24 -i VMAF/vmaf-2.3.1/resource_test/mp4/Seeking_30_480_1050.mp4
  -r 24 -i VMAF/vmaf-2.3.1/resource_test/mp4/Seeking_10_288_375.mp4
  -lavfi "[0:v]setpts=PTS-STARTPTS[reference];
    [1:v]scale=720:480:flags=bicubic,setpts=PTS-STARTPTS[distorted];
    [distorted][reference]libvmaf=log_fmt=xml:log_path=/home/pi/VMAF/log_latest_vmaf.xml:model='path=VMAF/vmaf-2.3.1/model/vmaf_v0.6.1.json':n_threads=4" -f null -`

`-r` set framerate (MUST be the same framerate in both videos)

`setpts=PTS-STARTPTS` synchronize the PTS (presentation time stamps) -> important, if PTS is not 0 (eg cutting a clip out of a video)

`log_fmt=` xml or json

PTS and framerate must be set correctly, since ffmpeg synchronizes with timestamps and not frames

# Capture Video
`libcamera-vid -t 10000 [-n/-p] --width=xxx --height=xxx --framerate=30 [--codec h264/mjpeg/yuv420] -o test.[h264/mjpeg/data]`

Videocapture without (-n) / with (-p) preview with specified width, height, framerate and codec

## Experiment with encoding settings via ffmpeg

Different CRF value (0 - 51): 0 lossless (best quality); 23 default; 51 wort quality (in-/decreases bitrate automatically)

`ffmpeg -i input.h264 -c:v libx264 -crf xx -r 30 -c:a copy output.mkv`

Zero Latency

`ffmpeg -i input.h264 -c:v libx264 -tune zerolatency -r 30 -c:a copy output.mkv`

Downscale video resolution

`ffmpeg -i input.h264 -vf scale=xxx:xxx output.mkv`

Set maximum bitrate

`ffmpeg -i input.h264 -c:v libx264 -r 30 -maxrate 1M -bufsize 500k -c:a copy output.mkv`

Set constant bitrate (`-b:v 1M` average bitrate, `-bufsize` interval in which bitrate is checked (shouldnt be lower than half of the average bitrate))

`ffmpeg -i input.h264 -c:v libx264 -r 30 -b:v 1M -minrate 1M -maxrate 1M -bufsize 500k -c:a copy output.mkv`

