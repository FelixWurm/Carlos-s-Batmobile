# Installation guide
## VMAF
### Install Meson and Ninja
`sudo apt-get install ninja-build meson`

### Install VMAF SDK
[Latest VMAF SDK](github.com/Netflix/vmaf/releases) -> unpack

`cd vmaf-x.x.x/libvmaf`

`meson build --buildtype release`

`ninja -vC build`

`ninja -vC build install`


## ffmpeg
[Source ffmpeg](ffmpeg.org/download.html) -> unpack

`cd ffmpeg`

`./configure --enable-gpl --enable-libx264 --enable-libx265 --enable-nonfree --enable-libvmaf --enable-version3 --enable-libaom`

`sudo make`

`sudo make install`

`export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib/aarch64-linux-gnu`

-> if export doesnt work, you get an error message: `ffmpeg error while loading shared libraries`



# Commands
## Recording with libcamera-vid
Capture a 15s long video in h264 (default) in 720p and 30fps

`libcamera-vid -t 15000 --width 1280 --height 720 --framerate 30 -o test.h264`


## Encoding with ffmpeg
### Constant bitrate (h264, h265)
Set the `average`, `minrate`, `maxrate` to the same number for a constant bitrate

`bufsize` checks and corrects the bitrate at the given bitrate (should not be lower than `average`/2 )

`ffmpeg -i input.h264 -c:v libx264 -r 30 -b:v 500k -minrate 500k -maxrate 500k -bufsize 250k output.mkv`


### Tune Zerolatency (h264,h265)
Uses as much bitrate as needed to achive streaming with low latency (`-tune` option for libx264/ libx265)

`ffmpeg -i input.h264 -c:v libx264 -tune zerolatency -r 30 output.mkv`


### Quality (mjpeg)
Since mjpeg doesnt have a bitrate option, quality can be changed with `-q:v`

(0: highest quality; 31: lowest quality; x < 2 might have compatibility issues)

`ffmpeg -i input.h264 -c:v mjpeg -r 30 -q:v 2 output.mkv`


### Scaling
`ffmpeg -i input.h264 -vf scale=640:480 -r 30 output.h264`



## VMAF score with ffmpeg
### VMAF score on the same resolution
`ffmpeg
  -r 30 -i pathToVideoFile/ORIGINALfile.h264
  -r 30 -i pathToVideoFile/ENCODEDfile.mkv
  -lavfi
    "[0:v]setpts=PTS-STARTPTS[reference];
    [1:v]setpts=PTS-STARTPTS[distorted];
    [distorted][reference]libvmaf=log_fmt=xml:log_path=/home/pi/VMAF/log_latest_vmaf.xml:model='path=VMAF/vmaf-2.3.1/model/vmaf_v0.6.1.json':n_threads=4" -f null -`

`-r 30` is the framerate

`-i` specifies the inputfile

`setpts=PTS-STARTPTS` sets PTS (presentation time stamps) -> may be different if its a clip out of a longer video

`log_fmt` is the log format (XML, JSON, ...)

`log_path` is the path where the log file is saved

`model='...'` is the path to the vmaf-json file (can select different models for phone, 4k, ...)

`n_threads=4` is the amount of threads used for the calculation

<u>ATTENTION:</u> PTS and framerate must be the same, since ffmpeg synchronizes them with timestamps and not frames

### VMAF score on different resolution
`ffmpeg
  -r 30 -i pathToVideoFile/ORIGINALfile720p.h264
  -r 30 -i pathToVideoFile/ENCODEDfile480p.mkv
  -lavfi
    "[0:v]setpts=PTS-STARTPTS[reference];
    [1:v]scale=1280:720:flags=bicubic,setpts=PTS-STARTPTS[distorted];
    [distorted][reference]libvmaf=log_fmt=xml:log_path=/home/pi/VMAF/log_latest_vmaf.xml:model='path=VMAF/vmaf-2.3.1/model/vmaf_v0.6.1.json':n_threads=4" -f null -`
    
`scale=xxx:xxx:flags=bicubic` scales the distorted video to the specified resolution with bicubic




# VMAF: In different resolutions and Environments
## VMAF: used resolutions
<ul>
  <li>  720p =		1280	x	720   </li>
  <li>  600p =		800		x	600   </li>
  <li>  480p =		640		x	480   </li>
  <li>  240p =		320		x	240   </li>
  <li>  144p =		256		x	144   </li>
</ul>


## VMAF: original video with itself
| Original file             | VMAF bright env | VMAF dark env |
| :---:                     | :---:           | :---:         |
| ORIGINAL-720p30fps.h264   | 99.7924         | 99.8200       |
| ORIGINAL-600p30fps.h264		|	99.7756         | 99.5113       |
| ORIGINAL-480p30fps.h264		|	99.7715         | 99.4573       |
| ORIGINAL-240p30fps.h264		|	99.7606         | 99.3798       |
| ORIGINAL-144p30fps.h264		|	99.7538         | 99.3537       |


## VMAF: original video with lower resolution video
| Comparison    | VMAF bright env | VMAF dark env |
| :---:         | :---:           | :---:         |
| 720p -> 600p  | 93.2493         | 79.8725       |
| 720p -> 480p  | 90.8330         | 76.1043       |
| 720p -> 240p  | 76.9833         | 63.7809       |
| 720p -> 144p  | 65.7241         | 56.3362       |

## VMAF scores in comparison
<table>
<tr><th>Encoder</th><th>Bright Environment 30fps</th><th>Dark Environment 30fps</th>
<tr><td>

| h264        |
| :---:       |
| -crf 23     |
| zerolatency |
| 500kbits    |
| 250kbits    |
| 100kbits    |

| h265        |
| :---:       |
| -crf 23     |
| zerolatency |
| 500kbits    |
| 250kbits    |
| 100kbits    |

| mjpeg       |
| :---:       |
| -q:v 2      |
| -q:v 15     |
| -q:v 30     |

</td><td>

| 720p    | 600p    | 480p    | 240p    | 144p    |
| :---:   | :---:   | :---:   | :---:   | :---:   |
| 96.9826 | 97.9301 | 98.0103 | 97.1149 | 96.8449 |
| 98.6467 | 98.7742 | 98.6823 | 98.1251 | 97.8179 |
| 85.6334 | 93.7485 | 97.3958 | 99.7606 | 99.5232 |
| 66.8929 | 83.1435 | 90.2666 | 98.7915 | 99.2679 |
| 40.4617 | 49.8921 | 63.3883 | 92.9990 | 97.9435 |

| 720p    | 600p    | 480p    | 240p    | 144p    |
| :---:   | :---:   | :---:   | :---:   | :---:   |
| 93.9466 | xx.xxxx | xx.xxxx | xx.xxxx | xx.xxxx |
| 97.0788 | xx.xxxx | xx.xxxx | xx.xxxx | xx.xxxx |
| 95.6419 | xx.xxxx | xx.xxxx | xx.xxxx | xx.xxxx |
| 92.8056 | xx.xxxx | xx.xxxx | xx.xxxx | xx.xxxx |
| 82.7695 | xx.xxxx | xx.xxxx | xx.xxxx | xx.xxxx |

| 720p    | 600p    | 480p    | 240p    | 144p    |
| :---:   | :---:   | :---:   | :---:   | :---:   |
| 99.3045 | 99.2423 | 99.1837 | 98.8800 | 98.6816 |
| 96.3412 | 96.3867 | 95.9942 | 94.2298 | 93.2091 |
| 93.1571 | 92.6899 | 92.0277 | 89.0783 | 87.0695 |

</td><td>

| 720p    | 600p    | 480p    | 240p    | 144p    |
| :---:   | :---:   | :---:   | :---:   | :---:   |
| 91.4772 | 93.0603 | 94.0238 | 95.5425 | 95.6634 |
| 93.9837 | 95.4751 | 95.8489 | 96.9700 | 97.0818 |
| 69.7901 | 88.6245 | 93.0197 | 98.5464 | 99.1046 |
| 57.8416 | 81.4107 | 87.4694 | 97.5083 | 98.7141 |
| 45.3892 | 60.9832 | 71.8171 | 92.6311 | 97.0003 |

| 720p    | 600p    | 480p    | 240p    | 144p    |
| :---:   | :---:   | :---:   | :---:   | :---:   |
| 77.7908 | xx.xxxx | xx.xxxx | xx.xxxx | xx.xxxx |
| 81.3120 | xx.xxxx | xx.xxxx | xx.xxxx | xx.xxxx |
| 79.4772 | xx.xxxx | xx.xxxx | xx.xxxx | xx.xxxx |
| 76.9844 | xx.xxxx | xx.xxxx | xx.xxxx | xx.xxxx |
| 71.7148 | xx.xxxx | xx.xxxx | xx.xxxx | xx.xxxx |

| 720p    | 600p    | 480p    | 240p    | 144p    |
| :---:   | :---:   | :---:   | :---:   | :---:   |
| 96.2826 | 96.8027 | 96.9291 | 97.4206 | 97.4756 |
| 82.5461 | 91.0914 | 92.1528 | 93.0679 | 92.5463 |
| 79.2964 | 88.2771 | 88.9593 | 88.8981 | 87.8721 |
  
</td>
</tr>
</table>
