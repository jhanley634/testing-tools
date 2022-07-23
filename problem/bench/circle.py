#! /usr/bin/env python
from pathlib import Path
import math

from svgwrite import Drawing
import typer


def circle(r_px: int = 100, v_skip=20, margin: float = 1.2,
           out_file: Path = '~/Desktop/circle.svg'):
    r = r_px
    out_file = out_file.expanduser()
    dwg = Drawing(out_file)
    dwg.add(dwg.circle(center=(margin * r, margin * r),
                       r=r,
                       fill='white',
                       stroke_width=6,
                       stroke='black'))
    x0 = (margin - 1) * r
    y0 = 2 * margin * r
    dwg.add(dwg.line((x0, y0), (x0 + math.pi * r, y0)).stroke('black', width=6))
    print(dwg.tostring())  # works well with: $ tidy -wrap 200 -indent -xml

    dwg.save()


if __name__ == '__main__':
    typer.run(circle)
