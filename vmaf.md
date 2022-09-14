# VMAF Quality measurement

### Install Meson + Ninja:
`sudo apt-get install ninja-build meson`

### Install VMAF SDK
[Latest VMAF SDK](github.com/Netflix/vmaf/releases) -> entpacken

`cd vmaf-x.x.x/libvmaf`

`meson build --buildtype release`

`ninja -vC build`

`ninja -vC build install`

### Install ffmpeg with libvmaf
[Source ffmpeg](ffmpeg.org/download.html) -> entpacken

`cd ffmpeg`

`./configure --enable-libvmaf`

`sudo make -j4`

`sudo make install`

`export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib/aarch64-linux-gnu`

-> falls export nicht funktioniert gibts Fehler `ffmpeg error while loading shared libraries`

## Run test video
[Test Video Github Repo](github.com/Netflix/cmaf_resource) -> nach vmaf-2.3.1 verschieben und entpacken (hier umbenannt in ressource_test)

`ffmpeg
  -video_size 576x324 -r 24 -pixel_format yuv420p -i VMAF/vmaf-2.3.1/resource_test/yuv/src01_hrc00_576x324.yuv
  -video_size 576x324 -r 24 -pixel_format yuv420p -i VMAF/vmaf-2.3.1/resource_test/yuv/src01_hrc01_576x324.yuv
  -lavfi
    "[0:v]setpts=PTS-STARTPTS[reference];
    [1:v]setpts=PTS-STARTPTS[distorted];
    [distorted][reference]libvmaf=log_fmt=xml:log_path=/dev/stdout:model='path=VMAF/vmaf-2.3.1/model/vmaf_v0.6.1.json':n_threads=4" -f null -`

### Options
`-video_size` setze video size

falls video-size unterschiedlich ist (zB 480p und 288p) -> upscaling with bicubic to 720x480

`ffmpeg
  -r 24 -i VMAF/vmaf-2.3.1/resource_test/mp4/Seeking_30_480_1050.mp4
  -r 24 -i VMAF/vmaf-2.3.1/resource_test/mp4/Seeking_10_288_375.mp4
  -lavfi "[0:v]setpts=PTS-STARTPTS[reference];
    [1:v]scale=720:480:flags=bicubic,setpts=PTS-STARTPTS[distorted];
    [distorted][reference]libvmaf=log_fmt=xml:log_path=/dev/stdout:model='path=VMAF/vmaf-2.3.1/model/vmaf_v0.6.1.json':n_threads=4" -f null -`

`-r` setze framerate (MUSS dieselbe framerate in beiden Videos sein)

`setpts=PTS-STARTPTS` synchronisiert die PTS (presentation time stamps) -> wichtig, falls PTS nicht 0 ist (zB Ausschnitt aus Video)

`log_fmt=` xml oder json

PTS und framerate müssen richtig gesetzt werden, da ffmpeg mit timestamps synchronisiert und nicht mit frames

