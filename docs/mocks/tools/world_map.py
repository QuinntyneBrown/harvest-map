#!/usr/bin/env python3
"""Regenerate assets/world-dots.svg and assets/world-dots.css from a world GeoJSON.

    python docs/mocks/tools/world_map.py path/to/countries.geo.json

Source used on 16 Oct 2026: https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json
The SVG is a dot matrix on an equirectangular grid (2.4° spacing, Antarctica
skipped); the CSS inlines it as a mask data URI so it works from file://.
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ASSETS = Path(__file__).resolve().parents[1] / "assets"
W, H = 3600, 1800  # 0.1° raster
STEP, RADIUS = 2.4, 2.2


def px(lon: float, lat: float) -> tuple[float, float]:
    return (lon + 180) / 360 * W, (90 - lat) / 180 * H


def main(src: str) -> int:
    img = Image.new("1", (W, H), 0)
    draw = ImageDraw.Draw(img)
    for feature in json.load(open(src, encoding="utf-8"))["features"]:
        geom = feature["geometry"]
        polys = geom["coordinates"] if geom["type"] == "Polygon" else [p for mp in geom["coordinates"] for p in mp]
        for ring in polys:
            pts = [px(x, y) for x, y in ring]
            if len(pts) > 2:
                draw.polygon(pts, fill=1)
    dots = []
    lat = 84.0
    while lat > -58:
        lon = -180 + STEP / 2
        while lon < 180:
            x, y = px(lon, lat)
            if img.getpixel((int(x), int(y))):
                dots.append((round((lon + 180) / 360 * 1000, 1), round((90 - lat) / 180 * 500, 1)))
            lon += STEP
        lat -= STEP
    circles = "".join(f'<circle cx="{x}" cy="{y}" r="{RADIUS}"/>' for x, y in dots)
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 500"><g fill="currentColor">{circles}</g></svg>'
    (ASSETS / "world-dots.svg").write_text(svg, encoding="utf-8")
    enc = svg.replace('"', "'").replace("#", "%23").replace("<", "%3C").replace(">", "%3E")
    css = ("/* world-dots.css — the dot-matrix world map as a CSS mask, inlined as a data URI so it\n"
           "   loads from file:// (external SVG masks are blocked by CORS under file://). Linked only by\n"
           "   mocks that show the map. Regenerate from a world GeoJSON with tools/world_map.py. */\n"
           f".map__land {{ mask-image: url(\"data:image/svg+xml;utf8,{enc}\"); -webkit-mask-image: url(\"data:image/svg+xml;utf8,{enc}\"); }}\n")
    (ASSETS / "world-dots.css").write_text(css, encoding="utf-8")
    print(f"{len(dots)} dots · world-dots.svg {len(svg) // 1024} KB · world-dots.css {len(css) // 1024} KB")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    raise SystemExit(main(sys.argv[1]))
