#!/bin/bash
# Compose marketing video from rendered PNG sequence
# Uses simplified font paths in /tmp/fonts to avoid Windows drive-letter escaping

set -e
SHOWCASE="C:/Users/Admin/OneDrive/Pictures/Screenshots 1/VR_Maritime_LMS_Models/_shared/Master_Showcase"
FRAMES="$SHOWCASE/frames/frame_%04d.png"
OUTPUT="$SHOWCASE/VR_Maritime_LMS_Marketing_v1.0.mp4"
FONT_BOLD="/tmp/fonts/arialbd.ttf"
FONT_REG="/tmp/fonts/arial.ttf"

echo "=== Composing Marketing Video ==="
echo "Output: $OUTPUT"

ffmpeg -y \
  -framerate 30 \
  -i "$FRAMES" \
  -vf "fade=t=in:st=0:d=1.5,fade=t=out:st=28.5:d=1.5,eq=saturation=1.2:contrast=1.08:gamma=0.92:brightness=0.02,colorbalance=rs=-0.05:gs=0.02:bs=0.1:rh=0.12:gh=0.06:bh=-0.08,drawbox=x=0:y=0:w=1280:h=80:color=black:t=fill,drawbox=x=0:y=640:w=1280:h=80:color=black:t=fill,drawtext=fontfile=${FONT_BOLD}:text='VR MARITIME LMS':fontcolor=white:fontsize=56:x=(w-text_w)/2:y=h/2-50:enable='between(t,1.5,5.5)':alpha='if(lt(t,2),(t-1.5)/0.5,if(gt(t,5),(5.5-t)/0.5,1))',drawtext=fontfile=${FONT_REG}:text='Professional VR Bridge Training':fontcolor=white:fontsize=28:x=(w-text_w)/2:y=h/2+20:enable='between(t,2,5.5)':alpha='if(lt(t,2.5),(t-2)/0.5,if(gt(t,5),(5.5-t)/0.5,1))',drawtext=fontfile=${FONT_BOLD}:text='Naval Architecture | IMO Standards | 132 Animations':fontcolor=white:fontsize=30:x=(w-text_w)/2:y=h-45:enable='between(t,16,20)':alpha='if(lt(t,16.5),(t-16)/0.5,if(gt(t,19.5),(20-t)/0.5,1))',drawtext=fontfile=${FONT_BOLD}:text='Unity | XR Toolkit | Quest | Vive | Pico':fontcolor=white:fontsize=30:x=(w-text_w)/2:y=h/2-30:enable='between(t,25,29)':alpha='if(lt(t,25.5),(t-25)/0.5,if(gt(t,28.5),(29-t)/0.5,1))',drawtext=fontfile=${FONT_REG}:text='Ready for Production':fontcolor=white:fontsize=22:x=(w-text_w)/2:y=h/2+15:enable='between(t,25.5,29)':alpha='if(lt(t,26),(t-25.5)/0.5,if(gt(t,28.5),(29-t)/0.5,1))'" \
  -c:v libx264 \
  -preset slow \
  -crf 18 \
  -pix_fmt yuv420p \
  -movflags +faststart \
  "$OUTPUT"

echo ""
echo "=== Done ==="
ls -lh "$OUTPUT"
