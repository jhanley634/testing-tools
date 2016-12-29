#! /usr/bin/env julia

set -e
(
  cd /tmp
  mkdir -p grey
  OPTS="mestimate mpdecimate noise fps=fps=2 sobel showinfo signalstats"
  OPTS="framestep=step=2 scale=w=iw/16:h=ih/16"
  set -x

  test -r drive.mp4 || (
    ffmpeg -i drive-large.mp4 ${OPTS}  drive.mp4)

  ffmpeg -i drive.mp4  grey/foo_%04d.pgm
)

set -x

./gen_frames.jl foo.mp4 grey/foo_%04d.pgm
