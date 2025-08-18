"""
Generate a modern, simple honeycomb icon in a hexagonal shape.
Outputs:
 - app/icons/app_icon.png (512x512, transparent outside the hex)
 - app/icons/app_icon.ico  (multi-size, transparent outside the hex)
 - app/icons/app_icon.svg  (vector reference)
"""
from __future__ import annotations

import math
import os
from pathlib import Path

from PIL import Image, ImageDraw


def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def hex_points(cx: float, cy: float, r: float) -> list[tuple[float, float]]:
    # Flat-top hexagon
    pts = []
    for i in range(6):
        angle = math.radians(60 * i)
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        pts.append((x, y))
    return pts


def draw_honeycomb_cluster(draw: ImageDraw.ImageDraw, center: tuple[int, int], r: float,
               stroke: int, color: tuple[int, int, int, int]) -> None:
  """Draw a triangular 1-2-3 hex outline cluster centered at 'center'."""
  cx, cy = center
  dx = 1.5 * r
  dy = math.sqrt(3) * r

  rows = [
    (0, -dy),                # 1 on top
    (-0.75 * r, 0), (0.75 * r, 0),  # 2 in middle
    (-1.5 * r, dy), (0, dy), (1.5 * r, dy),  # 3 at bottom
  ]
  for i in range(0, len(rows)):
    ox, oy = rows[i]
    pts = hex_points(cx + ox, cy + oy, r)
    draw.polygon(pts, outline=color, fill=None)


def draw_hex_mask(size: int, radius: float) -> Image.Image:
  """Return an alpha mask with a filled hexagon in white (opaque)."""
  mask = Image.new("L", (size, size), 0)
  d = ImageDraw.Draw(mask)
  pts = hex_points(size/2, size/2, radius)
  d.polygon(pts, fill=255)
  return mask


def generate_icon(out_dir: Path) -> None:
    ensure_dir(out_dir)

  size = 512
  # Create transparent base
  img = Image.new("RGBA", (size, size), (0, 0, 0, 0))

  # Create hex mask and white fill inside
  hex_radius = size * 0.46  # fits well with padding
  mask = draw_hex_mask(size, hex_radius)
  base = Image.new("RGBA", (size, size), (255, 255, 255, 255))
  img = Image.composite(base, img, mask)

  # Draw honeycomb cluster lines
  draw = ImageDraw.Draw(img)
  stroke = 26
  color = (244, 178, 63, 255)  # warm honey yellow
  center = (size // 2, int(size * 0.52))
  r = 62  # cell radius
  draw_honeycomb_cluster(draw, center=center, r=r, stroke=stroke, color=color)

  # Optional subtle inner shadow for depth
  pad = 10
  draw.polygon(hex_points(size/2, size/2, hex_radius - 8), outline=(0, 0, 0, 35), width=8)

    # Export PNG
    png_path = out_dir / "app_icon.png"
    img.save(png_path, format="PNG")

    # Export ICO (multiple sizes)
    ico_path = out_dir / "app_icon.ico"
    sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    img.save(ico_path, format="ICO", sizes=sizes)

    # Export simple SVG (vector reference)
    svg_path = out_dir / "app_icon.svg"
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">
  <defs>
    <clipPath id="hex">
      <polygon points="{ ' '.join(f'{x:.1f},{y:.1f}' for x,y in hex_points(256,256,256*0.46)) }" />
    </clipPath>
  </defs>
  <g clip-path="url(#hex)">
    <rect width="512" height="512" fill="#ffffff"/>
    <g fill="none" stroke="#f4b23f" stroke-width="26" transform="translate(256,266)">
      <polygon points="{ ' '.join(f'{x-256:.1f},{y-266:.1f}' for x,y in hex_points(256,266,62)) }"/>
    </g>
  </g>
  <!-- Cluster -->
  <g fill="none" stroke="#f4b23f" stroke-width="26" transform="translate(256,266)">
    <!-- top -->
    <polygon points="{ ' '.join(f'{x-256:.1f},{y-266-math.sqrt(3)*62:.1f}' for x,y in hex_points(256,266,62)) }"/>
    <!-- middle -->
    <g transform="translate(-46.5,0)">
      <polygon points="{ ' '.join(f'{x-256:.1f},{y-266:.1f}' for x,y in hex_points(256,266,62)) }"/>
    </g>
    <g transform="translate(46.5,0)">
      <polygon points="{ ' '.join(f'{x-256:.1f},{y-266:.1f}' for x,y in hex_points(256,266,62)) }"/>
    </g>
    <!-- bottom row -->
    <g transform="translate(-93, {math.sqrt(3)*62:.1f})">
      <polygon points="{ ' '.join(f'{x-256:.1f},{y-266:.1f}' for x,y in hex_points(256,266,62)) }"/>
    </g>
    <g transform="translate(0, {math.sqrt(3)*62:.1f})">
      <polygon points="{ ' '.join(f'{x-256:.1f},{y-266:.1f}' for x,y in hex_points(256,266,62)) }"/>
    </g>
    <g transform="translate(93, {math.sqrt(3)*62:.1f})">
      <polygon points="{ ' '.join(f'{x-256:.1f},{y-266:.1f}' for x,y in hex_points(256,266,62)) }"/>
    </g>
  </g>
 </svg>'''
    svg_path.write_text(svg, encoding="utf-8")

    print(f"Wrote: {png_path}")
    print(f"Wrote: {ico_path}")
    print(f"Wrote: {svg_path}")


if __name__ == "__main__":
    repo = Path(__file__).resolve().parents[1]
    out = repo / "app" / "icons"
    generate_icon(out)
