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
| latency     |
| 500kbits    |
| 250kbits    |
| 100kbits    |

| h265        |
| :---:       |
| -crf 23     |
| latency     |
| 500kbits    |
| 250kbits    |
| 100kbits    |

| mjpeg       |
| :---:       |
| -q:v 2      |
| -q:v 15     |
| -q:v 30     |

</td><td>

|&nbsp; 720p &nbsp;&nbsp;|&nbsp; 600p &nbsp;&nbsp;|&nbsp; 480p &nbsp;&nbsp;|&nbsp; 240p &nbsp;&nbsp;|&nbsp; 144p &nbsp;&nbsp;|
| :---:   | :---:   | :---:   | :---:   | :---:   |
| 96.9826 | 97.9301 | 98.0103 | 97.1149 | 96.8449 |
| 98.6467 | 98.7742 | 98.6823 | 98.1251 | 97.8179 |
| 85.6334 | 93.7485 | 97.3958 | 99.7606 | 99.5232 |
| 66.8929 | 83.1435 | 90.2666 | 98.7915 | 99.2679 |
| 40.4617 | 49.8921 | 63.3883 | 92.9990 | 97.9435 |

|&nbsp; 720p &nbsp;&nbsp;|&nbsp; 600p &nbsp;&nbsp;|&nbsp; 480p &nbsp;&nbsp;|&nbsp; 240p &nbsp;&nbsp;|&nbsp; 144p &nbsp;&nbsp;|
| :---:   | :---:   | :---:   | :---:   | :---:   |
| 93.9466 | 94.5633 | 94.4431 | 92.7328 | 91.6086 |
| 97.0788 | 97.5523 | 97.3682 | 96.4584 | 95.8907 |
| 95.6419 | 97.6536 | 98.3223 | 99.1758 | 99.3437 |
| 92.8056 | 95.7647 | 96.7827 | 98.4841 | 98.8526 |
| 82.7695 | 88.8063 | 91.8605 | 96.2599 | 97.4556 |

|&nbsp; 720p &nbsp;&nbsp;|&nbsp; 600p &nbsp;&nbsp;|&nbsp; 480p &nbsp;&nbsp;|&nbsp; 240p &nbsp;&nbsp;|&nbsp; 144p &nbsp;&nbsp;|
| :---:   | :---:   | :---:   | :---:   | :---:   |
| 99.3045 | 99.2423 | 99.1837 | 98.8800 | 98.6816 |
| 96.3412 | 96.3867 | 95.9942 | 94.2298 | 93.2091 |
| 93.1571 | 92.6899 | 92.0277 | 89.0783 | 87.0695 |

</td><td>

|&nbsp; 720p &nbsp;&nbsp;|&nbsp; 600p &nbsp;&nbsp;|&nbsp; 480p &nbsp;&nbsp;|&nbsp; 240p &nbsp;&nbsp;|&nbsp; 144p &nbsp;&nbsp;|
| :---:   | :---:   | :---:   | :---:   | :---:   |
| 91.4772 | 93.0603 | 94.0238 | 95.5425 | 95.6634 |
| 93.9837 | 95.4751 | 95.8489 | 96.9700 | 97.0818 |
| 69.7901 | 88.6245 | 93.0197 | 98.5464 | 99.1046 |
| 57.8416 | 81.4107 | 87.4694 | 97.5083 | 98.7141 |
| 45.3892 | 60.9832 | 71.8171 | 92.6311 | 97.0003 |

|&nbsp; 720p &nbsp;&nbsp;|&nbsp; 600p &nbsp;&nbsp;|&nbsp; 480p &nbsp;&nbsp;|&nbsp; 240p &nbsp;&nbsp;|&nbsp; 144p &nbsp;&nbsp;|
| :---:   | :---:   | :---:   | :---:   | :---:   |
| 77.7908 | 87.6920 | 88.9879 | 90.3929 | 90.2325 |
| 81.3120 | 91.4298 | 92.4915 | 94.4442 | 94.7432 |
| 79.4772 | 91.9383 | 94.2330 | 97.9836 | 98.6177 |
| 76.9844 | 89.5868 | 92.1102 | 96.8463 | 97.8919 |
| 71.7148 | 85.2299 | 88.5674 | 94.5355 | 96.3337 |

|&nbsp; 720p &nbsp;&nbsp;|&nbsp; 600p &nbsp;&nbsp;|&nbsp; 480p &nbsp;&nbsp;|&nbsp; 240p &nbsp;&nbsp;|&nbsp; 144p &nbsp;&nbsp;|
| :---:   | :---:   | :---:   | :---:   | :---:   |
| 96.2826 | 96.8027 | 96.9291 | 97.4206 | 97.4756 |
| 82.5461 | 91.0914 | 92.1528 | 93.0679 | 92.5463 |
| 79.2964 | 88.2771 | 88.9593 | 88.8981 | 87.8721 |
  
</td>
</tr>
</table>

Note: 100 is the best possible value and 20 the worst possible value




## Bitrate / VMAF scores: better comparison with each other
<table>
<tr><th>Encoder</th><th>Bright Environment 30fps</th><th>Dark Environment 30fps</th>
<tr><td>

| h264        |
| :---:       |
| -crf 23     |
| latency     |
| 500kbits    |
| 250kbits    |
| 100kbits    |

| h265        |
| :---:       |
| -crf 23     |
| latency     |
| 500kbits    |
| 250kbits    |
| 100kbits    |

| mjpeg       |
| :---:       |
| -q:v 2      |
| -q:v 15     |
| -q:v 30     |

</td><td>

|&nbsp; 720p &nbsp;&nbsp;|&nbsp; 600p &nbsp;&nbsp;|&nbsp; 480p &nbsp;&nbsp;|&nbsp; 240p &nbsp;&nbsp;|&nbsp; 144p &nbsp;&nbsp;|
| :---:   | :---:   | :---:   | :---:   | :---:   |
| 17.6114 |  8.7205 |  5.5708 |  1.5343 |  0.8467 |
| 29.8236 | 14.6699 |  9.7586 |  2.6701 |  1.3699 |
|  5.6170 |  5.0987 |  4.9591 |  4.7213 |  4.7828 |
|  3.6476 |  2.8505 |  2.6366 |  2.4091 |  2.4177 |
|  2.3726 |  1.8841 |  1.5145 |  1.0215 |  1.0006 |

|&nbsp; 720p &nbsp;&nbsp;|&nbsp; 600p &nbsp;&nbsp;|&nbsp; 480p &nbsp;&nbsp;|&nbsp; 240p &nbsp;&nbsp;|&nbsp; 144p &nbsp;&nbsp;|
| :---:   | :---:   | :---:   | :---:   | :---:   |
|  3.5446 |  2.1996 |  1.5671 |  0.6470 |  0.4257 |
|  8.6116 |  4.8282 |  3.2557 |  1.0989 |  0.6674 |
|  5.9075 |  5.6936 |  5.5938 |  5.6163 |  5.3954 |
|  3.1571 |  2.8612 |  2.8621 |  2.8939 |  2.8022 |
|  1.5222 |  1.3513 |  1.2628 |  1.2155 |  1.1800 |

|&nbsp; 720p &nbsp;&nbsp;|&nbsp; 600p &nbsp;&nbsp;|&nbsp; 480p &nbsp;&nbsp;|&nbsp; 240p &nbsp;&nbsp;|&nbsp; 144p &nbsp;&nbsp;|
| :---:   | :---:   | :---:   | :---:   | :---:   |
| 69.3423 | 38.0987 | 27.7969 | 11.1650 |  6.8807 |
| 30.7345 | 18.8096 | 13.2300 |  4.9666 |  3.0791 |
| 29.5630 | 17.8337 | 12.3767 |  4.4904 |  2.7679 |

</td><td>

|&nbsp; 720p &nbsp;&nbsp;|&nbsp; 600p &nbsp;&nbsp;|&nbsp; 480p &nbsp;&nbsp;|&nbsp; 240p &nbsp;&nbsp;|&nbsp; 144p &nbsp;&nbsp;|
| :---:   | :---:   | :---:   | :---:   | :---:   |
| 65.0217 | 10.9714 |  6.3388 |  1.5176 |  0.8154 |
| 90.8987 | 17.5962 | 10.6730 |  2.7019 |  1.4009 |
|  3.8114 |  5.1792 |  5.2785 |  4.7998 |  4.6315 |
|  2.3685 |  2.4935 |  2.6409 |  2.4408 |  2.4313 |
|  1.5863 |  1.2626 |  1.1975 |  1.0364 |  1.0103 |

|&nbsp; 720p &nbsp;&nbsp;|&nbsp; 600p &nbsp;&nbsp;|&nbsp; 480p &nbsp;&nbsp;|&nbsp; 240p &nbsp;&nbsp;|&nbsp; 144p &nbsp;&nbsp;|
| :---:   | :---:   | :---:   | :---:   | :---:   |
|  4.4864 |  2.0298 |  1.3710 |  0.5421 |  0.3546 |
|  9.7772 |  4.5281 |  2.8651 |  0.9847 |  0.6016 |
|  7.3229 |  6.2216 |  6.0913 |  5.7663 |  6.0740 |
|  4.1178 |  3.3264 |  3.1810 |  3.0254 |  3.0442 |
|  2.0777 |  1.5370 |  1.4339 |  1.2799 |  1.2664 |

|&nbsp; 720p &nbsp;&nbsp;|&nbsp; 600p &nbsp;&nbsp;|&nbsp; 480p &nbsp;&nbsp;|&nbsp; 240p &nbsp;&nbsp;|&nbsp; 144p &nbsp;&nbsp;|
| :---:   | :---:   | :---:   | :---:   | :---:   |
| 172.409 | 41.9943 | 25.7020 |  8.5403 |  5.1090 |
| 33.9326 | 17.5867 | 11.8282 |  4.0938 |  2.5177 |
| 33.3180 | 16.9353 | 11.2861 |  3.7909 |  2.3216 |
  
</td>
</tr>
</table>

Note: If the value is lower, the better the vmaf-bitrate score is

It's hard to compare the values of different resolutions tho, since they need lower bitrate for the same vmaf score

Additionally the bitrate of `zerolatency` is a lot higher, since they send a lot more i-frames, so their score is fairly low

Since mjpeg encodes each frame in itself, the bitrate is very high here too, which leads to a low score
