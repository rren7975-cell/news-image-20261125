#!/usr/bin/env python3
"""Render a 1024x1024 newspaper front page summarising 25 November 2026 world news.

Deterministic: fixed layout, seeded stars, no network, Pillow only.
Output: entry.png next to this file.
"""
import random
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 30
CONTENT_W = W - 2 * MARGIN

PAPER = (247, 241, 227)
INK = (26, 26, 26)
MUTED = (92, 84, 70)
RED = (164, 31, 33)
NAVY = (16, 32, 66)
RULE = (26, 26, 26)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


F_MASTHEAD = font("DejaVuSerif-Bold.ttf", 46)
F_META = font("DejaVuSans.ttf", 14)
F_STRAP = font("DejaVuSans-Bold.ttf", 14)
F_FOOTER = font("DejaVuSans.ttf", 11)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap using real font metrics."""
    words = text.split()
    lines, cur = [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def line_h(fnt, extra=2):
    a, d = fnt.getmetrics()
    return a + d + extra


# ---------------------------------------------------------------- stories
LEAD1 = (
    "SPACE",
    "Shenzhou-24 carries first Pakistani into orbit",
    "Muhammad Zeeshan Ali, a 40-year-old Pakistan Air Force pilot, blasted off "
    "this morning aboard China's Shenzhou-24 for the Tiangong station - the "
    "first foreign astronaut the station has hosted. He will spend about a "
    "week in orbit running Pakistani biotech experiments.",
)
LEAD2 = (
    "MARKETS",
    "AI rally collapses a day after Huang's return",
    "The Nasdaq fell 1.5% and Nvidia about 6% as the comeback rally faded. "
    "Reinstated on Monday, Jensen Huang told staff he is in therapy and "
    "admitted he had made 'some terrible mistakes'.",
)
LEAD3 = (
    "CHINA",
    "China investigates Politburo member Chen Jining",
    "Shanghai's party chief is the latest senior figure caught by Beijing's "
    "anti-corruption investigators, the Associated Press reported - a rare "
    "move against a sitting Politburo member.",
)

BRIEFS = [
    ("USA", "Trump awards Giuliani the Medal of Freedom",
     "America's highest civilian honour for the former New York mayor."),
    ("MIDDLE EAST", "Saudi condemns attack on Riyadh tower",
     "The PIF Tower, home of the sovereign wealth fund, was hit twice within a week."),
    ("GAZA", "Israeli strike kills Hamas security chief",
     "Naeem Abu Nahel, head of Hamas's internal security, died in Gaza City; seven Palestinians killed in the day."),
    ("EUROPE", "Russian strikes kill 14 in Kyiv region",
     "The barrages follow Putin's vow of a \"painful\" response to damage on the Crimean bridge."),
    ("EUROPE", "Russia tows drone-hit ship in the Baltic",
     "Finland says the vessel struck by Ukrainian drones is under tow; another warship was hit at a Libyan base."),
    ("USA", "Democrats take biggest House majority since 1992",
     "At least 258 seats give the party power to block Trump's agenda for two years."),
    ("BUSINESS", "US jury convicts Huawei of stealing trade secrets",
     "The Chinese technology giant was found guilty in an American courtroom."),
    ("AMERICAS", "Gunmen seize 25 hostages in Colombia",
     "The supermarket siege came a day after a car bomb destroyed buildings in a central Colombian city."),
    ("ASIA", "Hasina to return home on 16 December",
     "Bangladesh's ousted prime minister plans a Victory Day return from exile in India."),
    ("ASIA", "Malaysia to send 6,500 Rohingya to Myanmar",
     "Repatriation begins in December, days after the ICJ's genocide ruling on Myanmar."),
    ("EUROPE", "Sarkozy corruption case ordered to trial",
     "French officials send the former president's case before a court."),
    ("EUROPE", "Pelicot slams publisher over case photos",
     "Nude images taken by her rapist ex-husband were used to promote a book about her fight for justice."),
    ("BRITAIN", "Thousands evacuated from UK concert",
     "Police say an unknown substance released in the venue may be linked to robberies."),
    ("USA", "Extreme flooding threatens California",
     "Forecasters warn a storm system could bring dangerous flooding across the state."),
    ("BUSINESS", "Shein to pay $100m in FTC settlement",
     "The fast-fashion giant settles US allegations of deceptive practices."),
    ("USA", "Soldier admits selling secrets to China",
     "A US soldier admitted selling military information to Chinese buyers, AFP reported."),
    ("WORLD", "Five women killed hourly by relatives - UN",
     "A UN report says family members killed five women every hour in 2025."),
    ("HEALTH", "AIDS deaths fall to 20-year low",
     "570,000 died in 2025, UNAIDS says - but HIV funding fell 18%."),
    ("MIDDLE EAST", "Ship hits mine near Strait of Hormuz",
     "Iran's Revolutionary Guards say a container ship struck a mine on an \"unauthorised\" route."),
    ("USA", "Trump pardons the Thanksgiving turkeys",
     "The annual White House reprieve, two days before the holiday."),
]


# ---------------------------------------------------------------- illustration
def make_space_tile(tw, th):
    """Night-launch scene drawn on its own tile so nothing can overflow."""
    tile = Image.new("RGB", (tw, th), NAVY)
    d = ImageDraw.Draw(tile)
    # vertical sky gradient
    for y in range(th):
        t = y / th
        d.line([(0, y), (tw, y)],
               fill=(int(10 + 14 * t), int(20 + 22 * t), int(48 + 40 * t)))
    # stars (seeded -> deterministic)
    rng = random.Random(20261125)
    for _ in range(90):
        x, y = rng.randrange(tw), rng.randrange(int(th * 0.72))
        r = rng.choice([1, 1, 1, 2])
        d.ellipse([x - r, y - r, x + r, y + r], fill=(235, 238, 245))
    # earth curve along the bottom of the tile
    d.ellipse([-tw // 3, int(th * 0.78), int(tw * 1.35), int(th * 2.1)],
              fill=(38, 84, 140))
    d.arc([-tw // 3, int(th * 0.78), int(tw * 1.35), int(th * 2.1)],
          start=180, end=360, fill=(150, 190, 230), width=3)
    # space station (upper right): core, truss, two solar wings
    sx, sy = int(tw * 0.66), int(th * 0.20)
    d.rectangle([sx - 52, sy - 7, sx + 52, sy + 7], fill=(58, 96, 160))
    d.rectangle([sx - 52, sy + 7, sx + 52, sy + 13], fill=(40, 70, 122))
    d.rectangle([sx + 58, sy - 7, sx + 64, sy + 7], fill=(58, 96, 160))
    d.rectangle([sx + 58, sy + 7, sx + 64, sy + 13], fill=(40, 70, 122))
    d.line([sx - 70, sy + 3, sx + 76, sy + 3], fill=(210, 216, 228), width=3)
    d.rectangle([sx - 16, sy - 10, sx + 16, sy + 16], fill=(226, 230, 238))
    d.ellipse([sx - 5, sy - 1, sx + 5, sy + 9], fill=(120, 170, 220))
    d.rectangle([sx - 3, sy + 16, sx + 3, sy + 30], fill=(200, 206, 216))
    # rocket climbing from lower left
    rx, ry = int(tw * 0.30), int(th * 0.52)
    d.polygon([(rx - 13, ry + 34), (rx + 13, ry + 34), (rx + 9, ry - 26),
               (rx, ry - 52), (rx - 9, ry - 26)], fill=(238, 240, 244))
    d.ellipse([rx - 5, ry - 34, rx + 5, ry - 24], fill=(120, 170, 220))
    d.polygon([(rx - 13, ry + 30), (rx - 30, ry + 52), (rx - 12, ry + 46)],
              fill=(196, 52, 48))
    d.polygon([(rx + 13, ry + 30), (rx + 30, ry + 52), (rx + 12, ry + 46)],
              fill=(196, 52, 48))
    d.rectangle([rx - 13, ry + 12, rx + 13, ry + 20], fill=(196, 52, 48))
    # exhaust flame + glow
    d.polygon([(rx - 8, ry + 36), (rx + 8, ry + 36), (rx, ry + 78)],
              fill=(250, 176, 64))
    d.polygon([(rx - 4, ry + 36), (rx + 4, ry + 36), (rx, ry + 58)],
              fill=(255, 226, 150))
    d.line([rx - 2, ry + 84, rx - 10, ry + 112], fill=(170, 180, 200), width=3)
    d.line([rx + 3, ry + 84, rx + 8, ry + 112], fill=(150, 162, 186), width=2)
    return tile


# ---------------------------------------------------------------- stories on page
def draw_story(d, x, y, w, story, f_kick, f_head, f_body):
    kicker, head, body = story
    d.text((x, y), kicker, font=f_kick, fill=RED)
    y += line_h(f_kick) + 1
    for ln in wrap(d, head, f_head, w):
        d.text((x, y), ln, font=f_head, fill=INK)
        y += line_h(f_head, 1)
    y += 1
    for ln in wrap(d, body, f_body, w):
        d.text((x, y), ln, font=f_body, fill=INK)
        y += line_h(f_body, 1)
    return y


def story_height(d, w, story, f_kick, f_head, f_body):
    kicker, head, body = story
    h = line_h(f_kick) + 1
    h += len(wrap(d, head, f_head, w)) * line_h(f_head, 1) + 1
    h += len(wrap(d, body, f_body, w)) * line_h(f_body, 1)
    return h


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    x0, x1 = MARGIN, W - MARGIN

    # ---- masthead
    y = 20
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=F_MASTHEAD)
    d.text(((W - tw) / 2, y), title, font=F_MASTHEAD, fill=INK)
    y += line_h(F_MASTHEAD, 1) + 2
    d.line([x0, y, x1, y], fill=RULE, width=2)
    y += 5
    left, mid, right = "No. 25 · 2026", "Wednesday 25 November 2026", "One picture · One day"
    d.text((x0, y), left, font=F_META, fill=MUTED)
    mw = d.textlength(mid, font=F_META)
    d.text(((W - mw) / 2, y), mid, font=F_META, fill=INK)
    rw = d.textlength(right, font=F_META)
    d.text((x1 - rw, y), right, font=F_META, fill=MUTED)
    y += line_h(F_META, 1) + 5
    d.line([x0, y, x1, y], fill=RULE, width=5)
    y += 7
    strap = "The day's world news in one picture · 23 stories · All stories dated 25 November 2026"
    sw = d.textlength(strap, font=F_STRAP)
    d.text(((W - sw) / 2, y), strap, font=F_STRAP, fill=INK)
    y += line_h(F_STRAP, 1) + 7
    d.line([x0, y, x1, y], fill=RULE, width=2)
    y += 12

    # ---- leads: row A = tile | lead 1 ; row B = lead 2 | lead 3
    f_lkick = font("DejaVuSans-Bold.ttf", 13)
    f_lhead = font("DejaVuSerif-Bold.ttf", 20)
    f_lbody = font("DejaVuSans.ttf", 12)
    lead_top = y
    tile_w = 452
    tile = make_space_tile(tile_w, 140)
    img.paste(tile, (x0, lead_top))
    d = ImageDraw.Draw(img)
    l1x = x0 + tile_w + 24
    l1w = x1 - l1x
    end_a = draw_story(d, l1x, lead_top, l1w, LEAD1, f_lkick, f_lhead, f_lbody)
    row_a_h = max(140, end_a - lead_top)
    yb = lead_top + row_a_h + 10
    d.line([x0, yb - 5, x1, yb - 5], fill=(205, 196, 172), width=1)
    col_w2 = (CONTENT_W - 24) // 2
    end_b1 = draw_story(d, x0, yb, col_w2, LEAD2, f_lkick, f_lhead, f_lbody)
    end_b2 = draw_story(d, x0 + col_w2 + 24, yb, col_w2, LEAD3,
                        f_lkick, f_lhead, f_lbody)
    lead_bottom = max(end_b1, end_b2) + 10
    d.line([x0, lead_bottom, x1, lead_bottom], fill=RULE, width=3)
    print("lead block:", lead_top, "->", lead_bottom)

    # ---- briefs grid: 4 cols x 5 rows; auto-fit type size to the space left
    cols, gap = 4, 18
    col_w = (CONTENT_W - (cols - 1) * gap) // cols
    grid_top = lead_bottom + 10
    footer_h = line_h(F_FOOTER, 1) + 20
    grid_avail = H - MARGIN - footer_h - grid_top
    rows = [BRIEFS[i * cols:(i + 1) * cols] for i in range(5)]

    chosen = None
    for ks, hs, bs, pad in [(12, 14, 12, 10), (11, 13, 11, 9), (11, 13, 11, 7),
                            (10, 12, 11, 7), (10, 12, 10, 6), (10, 11, 10, 5)]:
        fk = font("DejaVuSans-Bold.ttf", ks)
        fh = font("DejaVuSerif-Bold.ttf", hs)
        fb = font("DejaVuSans.ttf", bs)
        row_hs = [max(story_height(d, col_w, s, fk, fh, fb) for s in row) + pad
                  for row in rows]
        if sum(row_hs) <= grid_avail:
            chosen = (fk, fh, fb, row_hs)
            print("grid type:", ks, hs, bs, "pad", pad, "rows", row_hs,
                  "total", sum(row_hs), "avail", grid_avail)
            break
    assert chosen, "grid does not fit at any type size"
    fk, fh, fb, row_hs = chosen

    gy = grid_top
    for r, row in enumerate(rows):
        for c, story in enumerate(row):
            draw_story(d, x0 + c * (col_w + gap), gy, col_w, story, fk, fh, fb)
        gy += row_hs[r]
        if r < 4:
            d.line([x0, gy - 5, x1, gy - 5], fill=(205, 196, 172), width=1)
    print("grid:", grid_top, "->", gy)

    # ---- footer
    fy = H - MARGIN - footer_h + 6
    d.line([x0, fy, x1, fy], fill=RULE, width=2)
    foot = ("Stories compiled from wire and newspaper reporting of 25 November 2026 · "
            "Illustration drawn in code · THE WORLD IN ONE DAY")
    fw = d.textlength(foot, font=F_FOOTER)
    d.text(((W - fw) / 2, fy + 7), foot, font=F_FOOTER, fill=MUTED)

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
