"""Build separately versioned candidate PDFs from canonical Markdown."""
import html
import re
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, PageBreak

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output/pdf"
INK = colors.HexColor("#172b43")
BLUE = colors.HexColor("#244cac")
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="BodyCandidate", fontName="Helvetica", fontSize=11, leading=15.5,
                         spaceAfter=8, textColor=INK, alignment=TA_LEFT, allowWidows=0, allowOrphans=0))
styles.add(ParagraphStyle(name="CellCandidate", fontName="Helvetica", fontSize=10, leading=13,
                         spaceAfter=0, textColor=INK))
styles.add(ParagraphStyle(name="TitleCandidate", fontName="Helvetica-Bold", fontSize=23, leading=28,
                         spaceAfter=16, textColor=INK, keepWithNext=True))
styles.add(ParagraphStyle(name="HeadingCandidate", fontName="Helvetica-Bold", fontSize=13, leading=17,
                         spaceBefore=12, spaceAfter=7, textColor=BLUE, keepWithNext=True))


def inline(text):
    text = text.replace("\u2014", "-").replace("\u2013", "-").replace("→", " -> ").replace("−", "-").replace("≤", "<=")
    text = html.escape(text)
    def link(match):
        label, target = match.groups()
        if not target.startswith(('https://', 'http://')):
            name = target.rsplit('/', 1)[-1].replace('.md', '.html')
            target = 'https://www.takyejun.com/static/research/ai-readiness/rc4-candidate-6/' + name
        return '<link href="' + target + '" color="#244cac"><u>' + label + '</u></link>'
    text = re.sub(r"\[([^]]+)\]\(([^)]+)\)", link, text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    return text.replace("`", "").replace("\n", "<br/>")


def footer(canvas, doc):
    canvas.setStrokeColor(colors.HexColor("#d6dce2"))
    canvas.line(44, 39, 568, 39)
    canvas.setFillColor(colors.HexColor("#506179"))
    canvas.setFont("Helvetica", 8)
    canvas.drawString(44, 26, "Yejun Tak | 0.1-rc.4-candidate.6 | Engineering commitment only")
    canvas.drawRightString(568, 26, str(doc.page))


def build(source, destination):
    lines = source.read_text().splitlines()
    body_style = styles["BodyCandidate"]
    if source.name == "rc4-candidate-6-external-packet.md":
        body_style = ParagraphStyle(name="PacketBody", parent=body_style, fontSize=11, leading=14.5, spaceAfter=5)
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
                    rows.append([Paragraph(inline(c).replace("PROCEED_TO_ENGINEERING", "PROCEED_TO_<br/>ENGINEERING").replace("INSUFFICIENT_EVIDENCE", "INSUFFICIENT_<br/>EVIDENCE"), styles["CellCandidate"]) for c in cells])
                i += 1
            n = len(rows[0])
            widths = [524 / n] * n
            if n == 3:
                widths = [130, 184, 210] if rows[0][0].getPlainText() == 'Result' else [190, 214, 120]
            if n == 4:
                widths = [128, 132, 132, 132]
            table = Table(rows, colWidths=widths, repeatRows=1, hAlign="LEFT")
            table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e7edf7")),
                                       ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#d6dce2")),
                                       ("VALIGN", (0, 0), (-1, -1), "TOP"),
                                       ("LEFTPADDING", (0, 0), (-1, -1), 7),
                                       ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                                       ("TOPPADDING", (0, 0), (-1, -1), 7),
                                       ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]))
            if len(story) >= 2 and isinstance(story[-2], Paragraph) and story[-2].style.name == "HeadingCandidate":
                paragraph, heading = story.pop(), story.pop()
                story.extend([KeepTogether([heading, paragraph, table]), Spacer(1, 9)])
            else:
                story.extend([KeepTogether([table]), Spacer(1, 9)])
            continue
        if line.startswith("# "):
            story.append(Paragraph(inline(line[2:]), styles["TitleCandidate"]))
        elif line.startswith("##"):
            if source.name == "FULL-PROFILE.md" and line.startswith("## 9."):
                story.append(PageBreak())
            story.append(Paragraph(inline(line.lstrip("# ")), styles["HeadingCandidate"]))
        else:
            text = line
            while i + 1 < len(lines) and lines[i + 1].strip() and not lines[i + 1].startswith(("#", "|", "- ")):
                if re.match(r"\d+\. ", lines[i + 1]):
                    break
                i += 1
                text += ("\n" if text.endswith("  ") else " ") + lines[i]
            story.append(Paragraph(inline(text), body_style))
        i += 1
    SimpleDocTemplate(str(destination), pagesize=letter, leftMargin=44, rightMargin=44,
                      topMargin=43, bottomMargin=53, title=source.stem + " - 0.1-rc.4-candidate.6",
                      author="Yejun Tak").build(story, onFirstPage=footer, onLaterPages=footer)


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    docs = {
        "protocol/0.1-rc.4-candidate.6/PROTOCOL.md": "Protocol-v0.1-rc.4-candidate.6.pdf",
        "protocol/0.1-rc.4-candidate.6/QUICK-6.md": "QUICK-6-v0.1-rc.4-candidate.6.pdf",
        "protocol/0.1-rc.4-candidate.6/FULL-PROFILE.md": "Full-Profile-v0.1-rc.4-candidate.6.pdf",
        "Pilot-Kit/rc4-candidate-6-external-packet.md": "External-Pilot-Packet-v0.1-rc.4-candidate.6.pdf",
    }
    for source, name in docs.items():
        build(ROOT / source, OUTPUT / name)
        print(name)


if __name__ == "__main__":
    main()
