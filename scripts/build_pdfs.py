"""Build separately versioned candidate PDFs from canonical Markdown."""
import html
import re
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output/pdf"
INK = colors.HexColor("#172b43")
BLUE = colors.HexColor("#244cac")
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="BodyCandidate", fontName="Helvetica", fontSize=10, leading=14,
                         spaceAfter=8, textColor=INK, alignment=TA_LEFT))
styles.add(ParagraphStyle(name="CellCandidate", fontName="Helvetica", fontSize=8.3, leading=11,
                         spaceAfter=0, textColor=INK))
styles.add(ParagraphStyle(name="TitleCandidate", fontName="Helvetica-Bold", fontSize=23, leading=28,
                         spaceAfter=16, textColor=INK, keepWithNext=True))
styles.add(ParagraphStyle(name="HeadingCandidate", fontName="Helvetica-Bold", fontSize=13, leading=17,
                         spaceBefore=12, spaceAfter=7, textColor=BLUE, keepWithNext=True))


def inline(text):
    text = text.replace("—", "-").replace("–", "-").replace("→", " -> ").replace("−", "-").replace("≤", "<=")
    text = re.sub(r"\[([^]]+)\]\(([^)]+)\)", r"\1", text)
    text = html.escape(text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    return text.replace("`", "")


def footer(canvas, doc):
    canvas.setStrokeColor(colors.HexColor("#d6dce2"))
    canvas.line(44, 39, 568, 39)
    canvas.setFillColor(colors.HexColor("#506179"))
    canvas.setFont("Helvetica", 8)
    canvas.drawString(44, 26, "Yejun Tak | 0.1-rc.4-candidate | Engineering commitment only")
    canvas.drawRightString(568, 26, str(doc.page))


def build(source, destination):
    lines = source.read_text().splitlines()
    body_style = styles["BodyCandidate"]
    if source.name == "rc4-external-packet.md":
        body_style = ParagraphStyle(name="PacketBody", parent=body_style, fontSize=9.5, leading=12.5, spaceAfter=7)
    story = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [x.strip() for x in lines[i].strip("|").split("|")]
                if not all(re.fullmatch(r"[: -]+", c) for c in cells):
                    rows.append([Paragraph(inline(c), styles["CellCandidate"]) for c in cells])
                i += 1
            n = len(rows[0])
            widths = [524 / n] * n
            if n == 3:
                widths = [83, 213, 228] if "QUICK" not in source.name else [46, 166, 312]
            if n == 4:
                widths = [206, 106, 106, 106]
            table = Table(rows, colWidths=widths, repeatRows=1, hAlign="LEFT")
            table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e7edf7")),
                                       ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#d6dce2")),
                                       ("VALIGN", (0, 0), (-1, -1), "TOP"),
                                       ("LEFTPADDING", (0, 0), (-1, -1), 7),
                                       ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                                       ("TOPPADDING", (0, 0), (-1, -1), 7),
                                       ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]))
            story.extend([table, Spacer(1, 9)])
            continue
        if line.startswith("# "):
            story.append(Paragraph(inline(line[2:]), styles["TitleCandidate"]))
        elif line.startswith("##"):
            story.append(Paragraph(inline(line.lstrip("# ")), styles["HeadingCandidate"]))
        else:
            text = line
            while i + 1 < len(lines) and lines[i + 1].strip() and not lines[i + 1].startswith(("#", "|", "- ")):
                if re.match(r"\d+\. ", lines[i + 1]):
                    break
                i += 1
                text += " " + lines[i]
            story.append(Paragraph(inline(text), body_style))
        i += 1
    SimpleDocTemplate(str(destination), pagesize=letter, leftMargin=44, rightMargin=44,
                      topMargin=43, bottomMargin=53, title=source.stem + " - 0.1-rc.4-candidate",
                      author="Yejun Tak").build(story, onFirstPage=footer, onLaterPages=footer)


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    docs = {
        "protocol/0.1-rc.4-candidate/PROTOCOL.md": "Protocol-v0.1-rc.4-candidate.pdf",
        "protocol/0.1-rc.4-candidate/QUICK-6.md": "QUICK-6-v0.1-rc.4-candidate.pdf",
        "protocol/0.1-rc.4-candidate/FULL-PROFILE.md": "Full-Profile-v0.1-rc.4-candidate.pdf",
        "Pilot-Kit/rc4-external-packet.md": "External-Pilot-Packet-v0.1-rc.4-candidate.pdf",
    }
    for source, name in docs.items():
        build(ROOT / source, OUTPUT / name)
        print(name)


if __name__ == "__main__":
    main()
