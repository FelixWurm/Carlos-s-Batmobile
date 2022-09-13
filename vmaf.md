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
