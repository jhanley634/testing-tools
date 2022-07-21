#! /usr/bin/env python
from pathlib import Path
import difflib

from svgwrite import Drawing
import typer


def circle(r_px: int = 100, v_skip=20, margin: float = 1.1,
           out_file: Path = '~/Desktop/circle.svg'):
    r = r_px
    out_file = out_file.expanduser()
    dwg = Drawing(out_file)
    dwg.add(dwg.rect(insert=(0, 0),
                     size=('220px', '120px'),
                     stroke_width='1',
                     stroke='black',
                     fill='purple'))
    dwg.add(dwg.circle(center=(margin * r, margin * r),
                       r=r,
                       stroke_width=6,
                       fill='white',
                       stroke='black'))
    print(dwg.tostring())  # works well with: $ tidy -wrap 200 -indent -xml

    dwg.save()


if __name__ == '__main__':
    typer.run(circle)
