# Installation guide
## ffmpeg
`.`

## VMAF
`.`

# Commands
## Recording with libcamera-vid
`.`


## Encoding with ffmpeg
### Bitrate (h264,h265)
`.`

### Tune Zerolatency (h264,h265)
`.`

### Quality (mjpeg)
`.`

### Scaling
`.`


## VMAF score with ffmpeg
### VMAF score on the same resolution
`.`

### VMAF score on different resolution
`.`




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
| Original file             | vmaf value  |
| :-----------------------: | :---------: |
| ORIGINAL-720p30fps.h264   | 99.7924     |
| ORIGINAL-600p30fps.h264		|	99.7756     |
| ORIGINAL-480p30fps.h264		|	99.7715     |
| ORIGINAL-240p30fps.h264		|	99.7606     |
| ORIGINAL-144p30fps.h264		|	99.7538     |


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
| 99.9999 | xxyzzzz | xxyzzzz | xxyzzzz | xxyzzzz |
| xxyzzzz | xxyzzzz | xxyzzzz | xxyzzzz | xxyzzzz |
| xxyzzzz | xxyzzzz | xxyzzzz | xxyzzzz | xxyzzzz |
| xxyzzzz | xxyzzzz | xxyzzzz | xxyzzzz | xxyzzzz |
| xxyzzzz | xxyzzzz | xxyzzzz | xxyzzzz | xxyzzzz |

| 720p    | 600p    | 480p    | 240p    | 144p    |
| :---:   | :---:   | :---:   | :---:   | :---:   |
| 99.9999 | xxyzzzz | xxyzzzz | xxyzzzz | xxyzzzz |
| xxyzzzz | xxyzzzz | xxyzzzz | xxyzzzz | xxyzzzz |
| xxyzzzz | xxyzzzz | xxyzzzz | xxyzzzz | xxyzzzz |
| xxyzzzz | xxyzzzz | xxyzzzz | xxyzzzz | xxyzzzz |
| xxyzzzz | xxyzzzz | xxyzzzz | xxyzzzz | xxyzzzz |

| 720p    | 600p    | 480p    | 240p    | 144p    |
| :---:   | :---:   | :---:   | :---:   | :---:   |
| 99.9999 | xxyzzzz | xxyzzzz | xxyzzzz | xxyzzzz |
| xxyzzzz | xxyzzzz | xxyzzzz | xxyzzzz | xxyzzzz |
| xxyzzzz | xxyzzzz | xxyzzzz | xxyzzzz | xxyzzzz |

</td><td>

| 720p    | 600p    | 480p    | 240p    | 144p    |
| :---:   | :---:   | :---:   | :---:   | :---:   |
| 99.9999 | xxyzzzz | xxyzzzz | xxyzzzz | xxyzzzz |
| xxyzzzz | xxyzzzz | xxyzzzz | xxyzzzz | xxyzzzz |
| xxyzzzz | xxyzzzz | xxyzzzz | xxyzzzz | xxyzzzz |
| xxyzzzz | xxyzzzz | xxyzzzz | xxyzzzz | xxyzzzz |
| xxyzzzz | xxyzzzz | xxyzzzz | xxyzzzz | xxyzzzz |

| 720p    | 600p    | 480p    | 240p    | 144p    |
| :---:   | :---:   | :---:   | :---:   | :---:   |
| 99.9999 | xxyzzzz | xxyzzzz | xxyzzzz | xxyzzzz |
| xxyzzzz | xxyzzzz | xxyzzzz | xxyzzzz | xxyzzzz |
| xxyzzzz | xxyzzzz | xxyzzzz | xxyzzzz | xxyzzzz |
| xxyzzzz | xxyzzzz | xxyzzzz | xxyzzzz | xxyzzzz |
| xxyzzzz | xxyzzzz | xxyzzzz | xxyzzzz | xxyzzzz |

| 720p    | 600p    | 480p    | 240p    | 144p    |
| :---:   | :---:   | :---:   | :---:   | :---:   |
| 99.9999 | xxyzzzz | xxyzzzz | xxyzzzz | xxyzzzz |
| xxyzzzz | xxyzzzz | xxyzzzz | xxyzzzz | xxyzzzz |
| xxyzzzz | xxyzzzz | xxyzzzz | xxyzzzz | xxyzzzz |
  
</td>
</tr>
</table>
