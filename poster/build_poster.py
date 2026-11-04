"""Build the poster: swap the figures in the Google Slides SVG export for our vector figures, then write a PDF.

Run from the repository root with `pixi run poster`.
"""
import re
import subprocess
from pathlib import Path

SLIDES = Path("poster/landau_poster_slides.svg")
OUT = Path("poster/landau_poster.svg")
PDF = OUT.with_suffix(".pdf")

# figure top left corner on the poster (SVG units, rounded) -> figure file
FIGURES = {
    (1001, 669): "Intro/MgCa_Phasediagram_Construction_landau.svg",
    (146, 2040): "Ase/Solid_Gas_ASE.svg",
    (909, 2040): "Point/Point_Defects_Exact.svg",
    (1672, 2040): "CuPt/figures/CuPt_cT_T_lines.svg",
    (2435, 2040): "CuPt/figures/CuPt_cT_by_mu.svg",
    (146, 2806): "Ideal/Ideal_Solution_1D.svg",
    (909, 2806): "Ideal/Ideal_Solution.svg",
    (1672, 2806): "CuPt/figures/CuPt_muT_T_lines.svg",
    (2435, 2806): "CuPt/figures/CuPt_muT_by_c.svg",
    (982, 3549): "RealWorld/AuCu_Phasediagram_LDA.svg",
    (2184, 3549): "RealWorld/MgCa_Phasediagram_Full.svg",
}

IMAGE = re.compile(
    r'<g transform="matrix\((?P<sx>\S+) 0\.0 0\.0 (?P<sy>\S+) (?P<x>\S+) (?P<y>\S+)\)">'
    r'<clipPath id="[^"]+"><path [^>]*/></clipPath>'
    r'<image [^>]*?width="(?P<w>[\d.]+)" height="(?P<h>[\d.]+)"[^>]*?/></g>'
)


def inline_figure(path, prefix, x, y, width, height):
    """The figure as a nested <svg> at the given position, with its own ids so figures can't clash."""
    svg = Path(path).read_text()
    viewbox = re.search(r'viewBox="([^"]+)"', svg).group(1)
    body = svg[svg.index(">", svg.index("<svg")) + 1 : svg.rindex("</svg>")]
    body = re.sub(r"<metadata>.*?</metadata>", "", body, flags=re.S)
    body = re.sub(r"<style.*?</style>", "", body, flags=re.S)  # its global rule moves to the <svg> below
    body = re.sub(r'\bid="([^"]+)"', rf'id="{prefix}\1"', body)
    body = re.sub(r"url\(#([^)]+)\)", rf"url(#{prefix}\1)", body)
    body = re.sub(r'href="#([^"]+)"', rf'href="#{prefix}\1"', body)
    return (
        f'<svg x="{x}" y="{y}" width="{width}" height="{height}" viewBox="{viewbox}" '
        # back to the SVG defaults the figure relies on, which the Slides export overrides at its root
        f'style="fill:#000;stroke:none;stroke-miterlimit:4;stroke-linejoin:round;stroke-linecap:butt">{body}</svg>'
    )


def main():
    poster = SLIDES.read_text()
    replaced = []

    def swap(match):
        x, y = float(match["x"]), float(match["y"])
        figure = FIGURES.get((round(x), round(y)))
        if figure is None:  # logos and QR codes stay
            return match[0]
        replaced.append(figure)
        width = float(match["sx"]) * float(match["w"])
        height = float(match["sy"]) * float(match["h"])
        return inline_figure(figure, f"fig{len(replaced)}-", x, y, width, height)

    poster = IMAGE.sub(swap, poster)
    missing = set(FIGURES.values()) - set(replaced)
    if missing:
        raise SystemExit(f"Not on the poster at the expected position: {sorted(missing)}")

    # physical size: 3401.57 x 4535.43 px at 96 dpi = 35.4 x 47.2 in
    width, height = re.search(r'viewBox="0\.0 0\.0 (\S+) (\S+)"', poster).groups()
    poster = poster.replace("<svg ", f'<svg width="{width}" height="{height}" ', 1)

    OUT.write_text(poster)
    subprocess.run(["rsvg-convert", "-f", "pdf", "-o", str(PDF), str(OUT)], check=True)
    print(f"Replaced {len(replaced)} figures; wrote {OUT} and {PDF}")


if __name__ == "__main__":
    main()
