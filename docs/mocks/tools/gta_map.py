#!/usr/bin/env python3
"""Regenerate assets/gta-dots.svg and assets/gta-dots.css for the Greater Toronto region view.

    python -I docs/mocks/tools/gta_map.py path/to/ne_10m_lakes.geojson

Source used on 16 Oct 2026: Natural Earth 10m lakes,
https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_10m_lakes.geojson
Everything inside BOX is land except the lake polygons (Lake Ontario). The SVG is a
dot matrix on a lon/lat grid with latitude scaled by cos(43.7°) so the frame is not
stretched; the CSS inlines it as a mask data URI and sets the frame's aspect ratio.
BOX must match GTA_BOX in pages.py, which places the pins and labels.
"""
import json
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ASSETS = Path(__file__).resolve().parents[1] / "assets"
BOX = (-79.85, -78.75, 43.42, 43.98)  # lon0, lon1, lat0, lat1: Mississauga to Oshawa, lakefront to north of Vaughan
LON0, LON1, LAT0, LAT1 = BOX
K = math.cos(math.radians((LAT0 + LAT1) / 2))
W = 2200  # 0.0005° raster
H = round(W * (LAT1 - LAT0) / (LON1 - LON0))
VW = 1000
VH = round(VW * (LAT1 - LAT0) / ((LON1 - LON0) * K))
COLS = 90
STEP_LON = (LON1 - LON0) / COLS
STEP_LAT = STEP_LON * K
RADIUS = round(VW / COLS * 0.33, 1)


def px(lon: float, lat: float) -> tuple[float, float]:
    return (lon - LON0) / (LON1 - LON0) * W, (LAT1 - lat) / (LAT1 - LAT0) * H


def main(src: str) -> int:
    img = Image.new("1", (W, H), 1)
    draw = ImageDraw.Draw(img)
    for feature in json.load(open(src, encoding="utf-8"))["features"]:
        geom = feature["geometry"]
        polys = geom["coordinates"] if geom["type"] == "Polygon" else [p for mp in geom["coordinates"] for p in mp]
        for ring in polys:
            if not any(LON0 - 1 < x < LON1 + 1 and LAT0 - 1 < y < LAT1 + 1 for x, y in ring):
                continue
            pts = [px(x, y) for x, y in ring]
            if len(pts) > 2:
                draw.polygon(pts, fill=0)
    dots = []
    lat = LAT1 - STEP_LAT / 2
    while lat > LAT0:
        lon = LON0 + STEP_LON / 2
        while lon < LON1:
            x, y = px(lon, lat)
            if img.getpixel((min(int(x), W - 1), min(int(y), H - 1))):
                dots.append((round((lon - LON0) / (LON1 - LON0) * VW, 1), round((LAT1 - lat) / (LAT1 - LAT0) * VH, 1)))
            lon += STEP_LON
        lat -= STEP_LAT
    circles = "".join(f'<circle cx="{x}" cy="{y}" r="{RADIUS}"/>' for x, y in dots)
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}"><g fill="currentColor">{circles}</g></svg>'
    (ASSETS / "gta-dots.svg").write_text(svg, encoding="utf-8")
    enc = svg.replace('"', "'").replace("#", "%23").replace("<", "%3C").replace(">", "%3E")
    css = ("/* gta-dots.css — the Greater Toronto dot-matrix land as a CSS mask, inlined as a data URI so it\n"
           "   loads from file://. Linked only by the map's Greater Toronto state. Regenerate from Natural\n"
           "   Earth 10m lakes with tools/gta_map.py; the aspect ratio below comes from the same bounding box. */\n"
           f".map--gta {{ aspect-ratio: {VW} / {VH}; }}\n"
           f".map--gta .map__land {{ mask-image: url(\"data:image/svg+xml;utf8,{enc}\"); -webkit-mask-image: url(\"data:image/svg+xml;utf8,{enc}\"); }}\n")
    (ASSETS / "gta-dots.css").write_text(css, encoding="utf-8")
    print(f"{len(dots)} dots · viewBox {VW}x{VH} · gta-dots.svg {len(svg) // 1024} KB · gta-dots.css {len(css) // 1024} KB")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    raise SystemExit(main(sys.argv[1]))
