from html.parser import HTMLParser
from io import BytesIO
from textwrap import wrap


class ResumeContentParser(HTMLParser):
    """Extract resume content from the rendered resume page."""

    TARGET_CLASSES = {
        "eyebrow": "subtitle",
        "bio": "body",
        "age-note": "body",
        "section-label": "section",
        "entry-title": "heading",
        "tag": "body",
        "entry-body": "body",
        "detail-panel": "body",
        "pill": "body",
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
    lines = _layout_items(items)
    pages = _paginate(lines)
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
        stream = _content_stream(page_lines)
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


def _layout_items(items):
    lines = []

    for style, text in items:
        if style == "title":
            lines.append({"text": text, "font": "F2", "size": 26, "gap": 24})
        elif style == "subtitle":
            lines.append({"text": text, "font": "F1", "size": 12, "gap": 16})
        elif style == "section":
            lines.append({"text": text.upper(), "font": "F2", "size": 15, "gap": 22})
        elif style == "heading":
            lines.append({"text": text, "font": "F2", "size": 12, "gap": 15})
        else:
            for part in wrap(text, width=82):
                lines.append({"text": part, "font": "F1", "size": 10, "gap": 13})
            lines.append({"text": "", "font": "F1", "size": 10, "gap": 4})

    return lines


def _paginate(lines):
    pages = []
    page = []
    used_height = 0
    max_height = 700

    for line in lines:
        if page and used_height + line["gap"] > max_height:
            pages.append(page)
            page = []
            used_height = 0

        page.append(line)
        used_height += line["gap"]

    if page:
        pages.append(page)

    return pages or [[{"text": "Resume", "font": "F2", "size": 20, "gap": 24}]]


def _content_stream(lines):
    commands = ["BT", "72 750 Td"]
    current_font = None
    current_size = None

    for line in lines:
        commands.append(f"0 -{line['gap']} Td")
        if line["font"] != current_font or line["size"] != current_size:
            commands.append(f"/{line['font']} {line['size']} Tf")
            current_font = line["font"]
            current_size = line["size"]
        if line["text"]:
            commands.append(f"({_escape_pdf_text(line['text'])}) Tj")

    commands.append("ET")
    return "\n".join(commands).encode("latin-1", errors="replace")


def _escape_pdf_text(text):
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
