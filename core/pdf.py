from html.parser import HTMLParser
from io import BytesIO
from textwrap import wrap

PAGE_WIDTH = 612
PAGE_HEIGHT = 792
LEFT_MARGIN = 64
RIGHT_MARGIN = 64
TOP_MARGIN = 66
BOTTOM_MARGIN = 54
CONTENT_WIDTH = PAGE_WIDTH - LEFT_MARGIN - RIGHT_MARGIN

COLOR_TEXT = (0.11, 0.10, 0.09)
COLOR_MUTED = (0.43, 0.42, 0.38)
COLOR_FAINT = (0.68, 0.66, 0.60)
COLOR_ACCENT = (0.17, 0.29, 0.88)
COLOR_SURFACE = (0.95, 0.94, 0.91)
COLOR_RULE = (0.82, 0.80, 0.75)


class ResumeContentParser(HTMLParser):
    """Extract resume content from the rendered resume page."""

    TARGET_CLASSES = {
        "eyebrow": "subtitle",
        "bio": "body",
        "age-note": "meta",
        "contact-link": "meta",
        "section-label": "section",
        "entry-title": "heading",
        "tag": "meta",
        "entry-body": "body",
        "detail-panel": "body",
        "pill": "chip",
        "honesty-text": "body",
    }

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.items = []
        self._capture_stack = []
        self._ignore_depth = 0

    def handle_starttag(self, tag, attrs):
        if self._ignore_depth:
            self._ignore_depth += 1
            return

        attrs = dict(attrs)
        class_names = set(attrs.get("class", "").split())

        if tag in {"script", "style", "svg"} or "contact-block" in class_names:
            self._ignore_depth = 1
            return

        if tag == "h1":
            self._capture_stack.append({"tag": tag, "style": "title", "text": []})
            return

        for class_name, style in self.TARGET_CLASSES.items():
            if class_name in class_names:
                self._capture_stack.append({"tag": tag, "style": style, "text": []})
                return

    def handle_endtag(self, tag):
        if self._ignore_depth:
            self._ignore_depth -= 1
            return

        if not self._capture_stack:
            return

        if tag == self._capture_stack[-1]["tag"]:
            capture = self._capture_stack.pop()
            text = " ".join("".join(capture["text"]).split())
            if text:
                self.items.append((capture["style"], text))

    def handle_data(self, data):
        if self._ignore_depth or not self._capture_stack:
            return

        self._capture_stack[-1]["text"].append(data)


def extract_resume_items(html):
    parser = ResumeContentParser()
    parser.feed(html)
    return _dedupe(parser.items)


def build_resume_pdf(html):
    items = extract_resume_items(html)
    return _build_pdf(items)


def _dedupe(items):
    seen = set()
    unique_items = []

    for style, text in items:
        key = (style, text)
        if key in seen:
            continue
        seen.add(key)
        unique_items.append((style, text))

    return unique_items


def _build_pdf(items):
    pages = _layout_pages(items)
    font_ref = 3 + len(pages) * 2
    bold_font_ref = font_ref + 1
    page_refs = [3 + index * 2 for index in range(len(pages))]
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids ["
        + b" ".join(f"{page_ref} 0 R".encode("ascii") for page_ref in page_refs)
        + f"] /Count {len(pages)} >>".encode("ascii"),
    ]

    for index, page_lines in enumerate(pages):
        page_ref = 3 + index * 2
        content_ref = page_ref + 1
        stream = _content_stream(page_lines, index + 1, len(pages))
        objects.extend(
            [
                f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
                f"/Resources << /Font << /F1 {font_ref} 0 R "
                f"/F2 {bold_font_ref} 0 R >> >> "
                f"/Contents {content_ref} 0 R >>".encode("ascii"),
                b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n"
                + stream + b"\nendstream",
            ]
        )

    objects.extend(
        [
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>",
        ]
    )

    pdf = BytesIO()
    pdf.write(b"%PDF-1.4\n")
    offsets = [0]

    for index, obj in enumerate(objects, start=1):
        offsets.append(pdf.tell())
        pdf.write(f"{index} 0 obj\n".encode("ascii"))
        pdf.write(obj)
        pdf.write(b"\nendobj\n")

    xref_offset = pdf.tell()
    pdf.write(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    pdf.write(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.write(f"{offset:010d} 00000 n \n".encode("ascii"))

    pdf.write(
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
        f"startxref\n{xref_offset}\n%%EOF\n".encode("ascii")
    )
    return pdf.getvalue()


def _layout_pages(items):
    title = _first_text(items, "title") or "Resume"
    subtitle = _first_text(items, "subtitle")
    content_items = _group_chips([
        (style, text)
        for style, text in items
        if style not in {"title", "subtitle"}
    ])

    pages = []
    ops = _page_background()
    y = _draw_header(ops, title, subtitle)

    for index, (style, text) in enumerate(content_items):
        previous_style = content_items[index - 1][0] if index else None
        height = _item_height(style, text, previous_style)
        if y - height < BOTTOM_MARGIN:
            pages.append(ops)
            ops = _page_background()
            y = PAGE_HEIGHT - TOP_MARGIN

        y = _add_item(ops, y, style, text, previous_style)

    if len(ops) > 1:
        pages.append(ops)

    return pages or [_page_background()]


def _group_chips(items):
    grouped = []
    chips = []

    for style, text in items:
        if style == "chip":
            chips.append(text)
            continue

        if chips:
            grouped.append(("chips", chips))
            chips = []
        grouped.append((style, text))

    if chips:
        grouped.append(("chips", chips))

    return grouped


def _first_text(items, style_name):
    for style, text in items:
        if style == style_name:
            return text
    return None


def _page_background():
    return [
        {"kind": "rect", "x": 0, "y": PAGE_HEIGHT - 8, "w": PAGE_WIDTH, "h": 8,
         "color": COLOR_ACCENT},
    ]


def _draw_header(ops, title, subtitle):
    y = PAGE_HEIGHT - TOP_MARGIN
    if subtitle:
        ops.append(_text_op(subtitle.upper(), LEFT_MARGIN, y, 9, "F2", COLOR_ACCENT))
        y -= 25

    ops.append(_text_op(title, LEFT_MARGIN, y, 31, "F2", COLOR_TEXT))
    y -= 17
    ops.append({
        "kind": "line",
        "x1": LEFT_MARGIN,
        "y1": y,
        "x2": PAGE_WIDTH - RIGHT_MARGIN,
        "y2": y,
        "width": 0.8,
        "color": COLOR_RULE,
    })
    return y - 26


def _item_height(style, text, previous_style=None):
    if style == "section":
        return 42
    if style == "heading":
        return 24 if previous_style == "section" else 32
    if style == "meta":
        return 18
    if style == "chip":
        return 24
    if style == "chips":
        return len(_chip_rows(text)) * 24 + 4

    return len(_wrap_text(text, 10.5)) * 14 + 12


def _add_item(ops, y, style, text, previous_style=None):
    if style == "section":
        y -= 12
        ops.append({
            "kind": "line",
            "x1": LEFT_MARGIN,
            "y1": y + 10,
            "x2": PAGE_WIDTH - RIGHT_MARGIN,
            "y2": y + 10,
            "width": 0.5,
            "color": COLOR_RULE,
        })
        ops.append(_text_op(text.upper(), LEFT_MARGIN, y - 4, 11, "F2", COLOR_ACCENT))
        return y - 26

    if style == "heading":
        if previous_style != "section":
            y -= 10
        ops.append(_text_op(text, LEFT_MARGIN, y, 12.5, "F2", COLOR_TEXT))
        return y - 18

    if style == "meta":
        ops.append(_text_op(text, LEFT_MARGIN, y, 9.5, "F1", COLOR_MUTED))
        return y - 16

    if style == "chip":
        width = min(_text_width(text, 9.5) + 18, CONTENT_WIDTH)
        ops.append({
            "kind": "rect",
            "x": LEFT_MARGIN,
            "y": y - 12,
            "w": width,
            "h": 17,
            "color": COLOR_SURFACE,
        })
        ops.append(_text_op(text, LEFT_MARGIN + 9, y - 7, 9.5, "F1", COLOR_MUTED))
        return y - 23

    if style == "chips":
        for row in _chip_rows(text):
            x = LEFT_MARGIN
            for chip in row:
                width = min(_text_width(chip, 9.5) + 18, CONTENT_WIDTH)
                ops.append({
                    "kind": "rect",
                    "x": x,
                    "y": y - 12,
                    "w": width,
                    "h": 17,
                    "color": COLOR_SURFACE,
                })
                ops.append(_text_op(chip, x + 9, y - 7, 9.5, "F1", COLOR_MUTED))
                x += width + 8
            y -= 24
        return y - 4

    for line in _wrap_text(text, 10.5):
        ops.append(_text_op(line, LEFT_MARGIN, y, 10.5, "F1", COLOR_MUTED))
        y -= 14
    return y - 8


def _wrap_text(text, size):
    width = max(48, int(CONTENT_WIDTH / (size * 0.52)))
    return wrap(_normalize_text(text), width=width)


def _chip_rows(chips):
    rows = []
    row = []
    row_width = 0

    for chip in chips:
        chip_width = min(_text_width(chip, 9.5) + 18, CONTENT_WIDTH)
        next_width = chip_width if not row else row_width + 8 + chip_width
        if row and next_width > CONTENT_WIDTH:
            rows.append(row)
            row = []
            row_width = 0

        row.append(chip)
        row_width = chip_width if row_width == 0 else row_width + 8 + chip_width

    if row:
        rows.append(row)

    return rows


def _text_width(text, size):
    return len(_normalize_text(text)) * size * 0.48


def _text_op(text, x, y, size, font, color):
    return {
        "kind": "text",
        "text": _normalize_text(text),
        "x": x,
        "y": y,
        "size": size,
        "font": font,
        "color": color,
    }


def _content_stream(ops, page_number, page_count):
    commands = []

    for op in ops:
        if op["kind"] == "text":
            commands.append(_pdf_text_command(op))
        elif op["kind"] == "line":
            commands.append(_pdf_line_command(op))
        elif op["kind"] == "rect":
            commands.append(_pdf_rect_command(op))

    footer = f"Yali Tal resume  |  page {page_number} of {page_count}"
    commands.append(
        _pdf_text_command(_text_op(footer, LEFT_MARGIN, 28, 8, "F1", COLOR_FAINT))
    )
    return "\n".join(commands).encode("latin-1", errors="replace")


def _pdf_text_command(op):
    r, g, b = op["color"]
    return (
        f"BT {r:.3f} {g:.3f} {b:.3f} rg /{op['font']} {op['size']} Tf "
        f"1 0 0 1 {op['x']:.2f} {op['y']:.2f} Tm "
        f"({_escape_pdf_text(op['text'])}) Tj ET"
    )


def _pdf_line_command(op):
    r, g, b = op["color"]
    return (
        f"q {r:.3f} {g:.3f} {b:.3f} RG {op['width']:.2f} w "
        f"{op['x1']:.2f} {op['y1']:.2f} m {op['x2']:.2f} {op['y2']:.2f} l S Q"
    )


def _pdf_rect_command(op):
    r, g, b = op["color"]
    return (
        f"q {r:.3f} {g:.3f} {b:.3f} rg "
        f"{op['x']:.2f} {op['y']:.2f} {op['w']:.2f} {op['h']:.2f} re f Q"
    )


def _normalize_text(text):
    return (
        text.replace("\u00b7", "|")
        .replace("\u2192", "->")
        .replace("\u2193", "")
        .replace("\u2191", "")
        .replace("\u2014", "-")
        .replace("\u2013", "-")
        .replace("\u2018", "'")
        .replace("\u2019", "'")
        .replace("\u201c", '"')
        .replace("\u201d", '"')
        .strip()
    )


def _escape_pdf_text(text):
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
