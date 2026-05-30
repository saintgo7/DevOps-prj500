#!/usr/bin/env python3
"""Convert the lecture storyboard markdown into a PowerPoint deck.

The source markdown uses a specific convention:
  # title at the very top
  ## 모듈 N. <name>          -> section divider slide
  ### S## — <title>          -> content slide built from the following
                                 markdown table (요소 | 내용)

Other markdown sections (부록, 0. 목차) become an outline appendix.
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt
from lxml import etree


SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)
KO_FONT = "Malgun Gothic"
EN_FONT = "Calibri"
CODE_FONT = "Consolas"

NAVY = RGBColor(0x1F, 0x3B, 0x6E)
BLUE = RGBColor(0x2C, 0x55, 0x9E)
GREY = RGBColor(0x55, 0x55, 0x55)
LIGHT = RGBColor(0xF2, 0xF2, 0xF2)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)


@dataclass
class SlideData:
    kind: str           # 'cover' | 'section' | 'content' | 'outline'
    title: str = ""
    subtitle: str = ""
    rows: list[tuple[str, str]] = field(default_factory=list)
    bullets: list[str] = field(default_factory=list)


def _set_font(run, *, size: int = 18, bold: bool = False, color: RGBColor = None,
              east_asia: str = KO_FONT, latin: str = EN_FONT) -> None:
    run.font.size = Pt(size)
    run.font.bold = bold
    if color is not None:
        run.font.color.rgb = color
    # python-pptx exposes latin font via run.font.name. To also set the
    # east-asian font, we patch the underlying rPr element.
    run.font.name = latin
    r_pr = run._r.get_or_add_rPr()
    ea = r_pr.find(qn("a:ea"))
    if ea is None:
        ea = etree.SubElement(r_pr, qn("a:ea"))
    ea.set("typeface", east_asia)


def _add_textbox(slide, *, left: Inches, top: Inches, width: Inches, height: Inches,
                 anchor=MSO_ANCHOR.TOP) -> None:
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    return tf


def _parse(md_text: str) -> list[SlideData]:
    out: list[SlideData] = []
    lines = md_text.splitlines()

    # Find cover title (first H1)
    cover_title = ""
    cover_subtitle = ""
    for ln in lines:
        if ln.startswith("# ") and not cover_title:
            cover_title = ln[2:].strip()
            break
    # Pull the subtitle line (the bold "> **부제**" pattern) if present
    for ln in lines:
        m = re.match(r"^>\s*\*\*부제\*\*\s*:\s*(.+)$", ln.strip())
        if m:
            cover_subtitle = m.group(1).strip()
            break

    out.append(SlideData(kind="cover", title=cover_title, subtitle=cover_subtitle))

    # Walk for section dividers (## 모듈 N. ...) and content slides (### S## — ...)
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i].rstrip()

        m_section = re.match(r"^##\s+(모듈\s+\d+\.\s+.+)$", line)
        if m_section:
            out.append(SlideData(kind="section", title=m_section.group(1).strip()))
            i += 1
            continue

        m_slide = re.match(r"^###\s+(S\d+)\s*[—\-]\s*(.+)$", line)
        if m_slide:
            slide_id = m_slide.group(1)
            slide_title = m_slide.group(2).strip()
            i += 1
            # Collect markdown table rows until next blank line that ends the table
            rows: list[tuple[str, str]] = []
            while i < n and not lines[i].strip().startswith("|"):
                i += 1
            while i < n and lines[i].strip().startswith("|"):
                raw = lines[i].strip()
                # skip separator
                if re.fullmatch(r"\|[\s:\-]+(\|[\s:\-]+)+\|?", raw):
                    i += 1
                    continue
                cells = [c.strip() for c in raw.strip("|").split("|")]
                if len(cells) >= 2 and cells[0] not in ("요소",):
                    rows.append((cells[0], " | ".join(cells[1:])))
                i += 1
            out.append(SlideData(kind="content", title=f"{slide_id} — {slide_title}", rows=rows))
            continue

        i += 1
    return out


def _render_cover(slide, data: SlideData) -> None:
    # background banner
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_W, SLIDE_H)
    bar.line.fill.background()
    bar.fill.solid()
    bar.fill.fore_color.rgb = NAVY

    tf = _add_textbox(
        slide, left=Inches(0.9), top=Inches(2.2),
        width=Inches(11.5), height=Inches(2.5), anchor=MSO_ANCHOR.TOP
    )
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    r = p.add_run()
    r.text = data.title
    _set_font(r, size=40, bold=True, color=WHITE)

    if data.subtitle:
        p2 = tf.add_paragraph()
        p2.alignment = PP_ALIGN.LEFT
        r2 = p2.add_run()
        r2.text = data.subtitle
        _set_font(r2, size=22, color=RGBColor(0xCC, 0xDD, 0xF2))

    # Footer slogan
    tf2 = _add_textbox(
        slide, left=Inches(0.9), top=Inches(6.3),
        width=Inches(11.5), height=Inches(0.7), anchor=MSO_ANCHOR.BOTTOM
    )
    p = tf2.paragraphs[0]
    r = p.add_run()
    r.text = "AI 에이전트 시대의 창업가 정신 강의 — 7개 모듈 · 약 6시간"
    _set_font(r, size=14, color=RGBColor(0xCC, 0xDD, 0xF2))


def _render_section(slide, data: SlideData) -> None:
    # left vertical bar
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(0.7), SLIDE_H)
    bar.line.fill.background()
    bar.fill.solid()
    bar.fill.fore_color.rgb = NAVY

    tf = _add_textbox(
        slide, left=Inches(1.2), top=Inches(2.8),
        width=Inches(11.5), height=Inches(2.0), anchor=MSO_ANCHOR.TOP
    )
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = data.title
    _set_font(r, size=44, bold=True, color=NAVY)


def _render_content(slide, data: SlideData) -> None:
    # Title block
    tf = _add_textbox(
        slide, left=Inches(0.6), top=Inches(0.4),
        width=Inches(12.2), height=Inches(0.9)
    )
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = data.title
    _set_font(r, size=24, bold=True, color=NAVY)

    # Body block — render the rows we extracted (요소 | 내용 pairs)
    # Layout: each row becomes "■ 요소 — 내용" or block with header
    body = _add_textbox(
        slide, left=Inches(0.6), top=Inches(1.4),
        width=Inches(12.2), height=Inches(5.5)
    )
    first = True
    for label, value in data.rows:
        if first:
            p = body.paragraphs[0]
            first = False
        else:
            p = body.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.space_after = Pt(6)
        r1 = p.add_run()
        r1.text = f"■ {label}  "
        _set_font(r1, size=14, bold=True, color=BLUE)
        r2 = p.add_run()
        r2.text = _truncate(value, 220)
        _set_font(r2, size=14, color=GREY)

    # Footer with slide id / time
    foot = _add_textbox(
        slide, left=Inches(0.6), top=Inches(6.9),
        width=Inches(12.2), height=Inches(0.4)
    )
    pf = foot.paragraphs[0]
    pf.alignment = PP_ALIGN.RIGHT
    rf = pf.add_run()
    rf.text = "직업으로서의 창업가와 창업가 정신"
    _set_font(rf, size=10, color=GREY)


def _truncate(s: str, n: int) -> str:
    s = re.sub(r"\s+", " ", s).strip()
    if len(s) <= n:
        return s
    return s[: n - 1] + "…"


def build_deck(md_path: Path, out_path: Path) -> None:
    md = md_path.read_text(encoding="utf-8")
    slides_data = _parse(md)

    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H

    blank_layout = prs.slide_layouts[6]  # blank
    for data in slides_data:
        slide = prs.slides.add_slide(blank_layout)
        if data.kind == "cover":
            _render_cover(slide, data)
        elif data.kind == "section":
            _render_section(slide, data)
        else:
            _render_content(slide, data)

    prs.save(out_path)
    print(f"wrote {out_path} ({len(slides_data)} slides)")


def main() -> None:
    if len(sys.argv) != 3:
        print("usage: md2pptx.py <input.md> <output.pptx>", file=sys.stderr)
        sys.exit(2)
    build_deck(Path(sys.argv[1]), Path(sys.argv[2]))


if __name__ == "__main__":
    main()
