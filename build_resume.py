#!/usr/bin/env python3
"""Build Subhan Gadirli's resume ODT files (design + ATS).

The ODT is the canonical artifact: CI exports the PDF from the same ODT
with LibreOffice, so ODT and PDF are layout-identical by construction.

Usage:
    python3 build_resume.py [--out dist/]

Dependencies (pip): odfpy, cairosvg
"""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ICONS_SVG = ROOT / "assets" / "icons"
ICONS_PNG = ROOT / "build" / "icons"

FONT = "IBM Plex Serif"

# ----------------------------------------------------------------------------
# Content (ported verbatim from the retired HTML sources; no em dashes)
# ----------------------------------------------------------------------------

EMAIL = "subhanqedirli@protonmail.com"
PHONE = "+994 55 667 19 03"
PHONE_RAW = "+994556671903"
LOCATION = "Baku, Azerbaijan"
WEBSITE = "https://jkgadirli.dev/"

SUMMARY = (
    "Junior full-stack developer and Computer Science student with hands-on "
    "experience in backend development, REST API design, and server-side "
    "applications using TypeScript (Node.js, Deno) and Python. Skilled in "
    "PostgreSQL, Docker, CI/CD, automated testing, Git, and Linux "
    "environments, with frontend experience in React, Next.js, and SvelteKit. "
    "Active open-source contributor and Community Lead of the Azerbaijan "
    "GitHub Community."
)

EXPERIENCE = [
    {
        "role": "Founder & Full-Stack Developer - Omicron",
        "date": "Jun 2026 - Present",
        "bullets": [
            "Building a minimal, modern, self-hostable blogging platform with ActivityPub federation; backend on Deno, Hono, Fedify, Drizzle, and PostgreSQL with CI/CD via GitHub Actions.",
            "Developing the frontend with SvelteKit, bits-ui, Tiptap, and Tailwind CSS; Astro powers the docs and onboarding sites at docs.omicron.blog and join.omicron.blog.",
            "Developing REST APIs and frontend features with code review and testing; iterating on performance and self-hosting workflows.",
        ],
    },
    {
        "role": "Community Lead - Azerbaijan GitHub Community",
        "date": "Jan 2026 - Present",
        "bullets": [
            "Lead a local developer community focused on GitHub, open source, and developer education; organized community events and grew the GitHub organization.",
            "Maintain community website and initiatives with TypeScript and CI/CD, reviewing pull requests and coordinating contributors in an Agile workflow.",
        ],
    },
    {
        "role": "Member of Corporate Relations - ESTIEM LG Baku",
        "date": "Mar 2025 - Feb 2026",
        "bullets": [
            "Built corporate partnerships and managed communications through stakeholder and negotiation management.",
        ],
    },
    {
        "role": "Linux Developer - Cyber Security Platform / Turan Linux",
        "date": "May 2020 - Jun 2024",
        "bullets": [
            "Contributed to Linux distribution tooling and desktop packages, including work on Khazar/Turan Linux components and system utilities; packaged and tested builds for Debian-based environments.",
            "Worked with Linux environments, shell scripting, and open-source collaboration using Git and code review across a 4-year span.",
        ],
    },
]

PROJECTS = [
    ("Webmius", "https://github.com/subhangadirli/webmius",
     "TypeScript, SSH. Web-based SSH management system for remote servers; REST API backend and Docker deployment."),
    ("Gazan", "https://github.com/subhangadirli/gazan",
     "Python, GTK4, Linux. Desktop app for browsing and managing cloud files via rclone; GTK4/libadwaita interface."),
    ("Kagi Translate MCP", "https://github.com/subhangadirli/kagi-translate-mcp",
     "TypeScript, MCP, API. Model Context Protocol server exposing Kagi Translate to MCP clients with REST integration."),
    ("X to Mastodon Bot", "https://github.com/subhangadirli/x-to-mastodon-bot",
     "JavaScript, API. Automation bot mirroring posts from X to Mastodon via REST APIs."),
]

SKILLS = [
    ("Proficient:", [
        ("typescript.svg", "Typescript"), ("python.svg", "Python"),
        ("react.svg", "React"), ("nextdotjs.svg", "Next.js"),
        ("svelte.svg", "SvelteKit"), ("nodedotjs.svg", "Node.js"),
        ("deno.svg", "Deno"), ("hono.svg", "Hono"),
        ("drizzle.svg", "Drizzle ORM"), ("postgresql.svg", "PostgreSQL"),
        ("docker.svg", "Docker"), ("git.svg", "Git"),
        ("linux.svg", "Linux"),
    ]),
    ("Familiar:", [
        ("javascript.svg", "Javascript"), ("ruby.svg", "Ruby"),
        ("astro.svg", "Astro"), ("tailwindcss.svg", "Tailwind CSS"),
        ("express.svg", "Express.js"), ("flask.svg", "Flask"),
        ("django.svg", "Django"), ("bun.svg", "Bun"),
        ("sqlite.svg", "SQLite"), ("prisma.svg", "Prisma ORM"),
        ("github.svg", "GitHub"), ("gitlab.svg", "GitLab"),
        ("podman.svg", "Podman"), ("caddy.svg", "Caddy"),
        ("anubis.svg", "Anubis"),
    ]),
    ("Cloud & Hosting:", [
        ("vercel.svg", "Vercel"), ("netlify.svg", "Netlify"),
        ("heroku.svg", "Heroku"), ("hetzner.svg", "Hetzner (VPS)"),
        ("cloudflare.svg", "Cloudflare"), ("awsamplify.svg", "AWS Amplify"),
    ]),
]

EDUCATION = [
    {"title": "Azerbaijan Technical University", "meta": "Bachelor \u2022 89/100",
     "left": "Computer Science (English)", "right": "Baku, Azerbaijan \u2022 DATES"},
    {"title": "Qwasar Silicon Valley", "meta": "Course",
     "left": "Full-Stack Development", "right": "Baku, Azerbaijan \u2022 DATES"},
]
EDU_DATES = {"design": ("2024-2028", "2025-2026"), "ats": ("2024 - 2028", "2025 - 2026")}

CERTS = [{"title": "Introduction to Entrepreneurship", "meta": "Jan 1, 2025",
          "org": "SABAH.HUB"}]

LANGUAGES = [("Azerbaijani", "Native"), ("English", "B2 Upper-Intermediate")]

PROFILES = [
    ("github.svg", "Github", "subhangadirli", "https://github.com/subhangadirli"),
    ("linkedin.svg", "LinkedIn", "subhangadirli", "https://www.linkedin.com/in/subhangadirli/"),
    ("codeberg.svg", "Codeberg", "subhangadirli", "https://codeberg.org/subhangadirli"),
]

INTERESTS = [
    ("lucide-terminal.svg", "Linux & system optimization"),
    ("lucide-git-merge.svg", "Open-source contributions"),
    ("lucide-cpu.svg", "Embedded systems"),
    ("lucide-app-window.svg", "Building full-stack applications"),
    ("lucide-server.svg", "Open-source tools and self-hosting"),
    ("lucide-cloud.svg", "Cloud platforms & containerization"),
]

CONTACT_ICONS = [
    ("lucide-mail.svg", ("link", "mailto:" + EMAIL, EMAIL)),
    ("lucide-phone.svg", ("link", "tel:" + PHONE_RAW, PHONE)),
    ("lucide-map-pin.svg", ("text", LOCATION)),
    ("lucide-globe.svg", ("link", WEBSITE, WEBSITE)),
]


# ----------------------------------------------------------------------------
# Icon rasterization (SVG -> PNG at build time for ODT embedding)
# ----------------------------------------------------------------------------

def render_icons():
    import cairosvg

    ICONS_PNG.mkdir(parents=True, exist_ok=True)
    for svg in sorted(ICONS_SVG.glob("*.svg")):
        png = ICONS_PNG / (svg.stem + ".png")
        if png.exists() and png.stat().st_mtime >= svg.stat().st_mtime:
            continue
        cairosvg.svg2png(url=str(svg), write_to=str(png),
                         output_width=64, output_height=64)
    return ICONS_PNG


# ----------------------------------------------------------------------------
# ODT document scaffold
# ----------------------------------------------------------------------------

def new_document():
    from odf.opendocument import OpenDocumentText
    from odf.style import (FontFace, MasterPage, PageLayout,
                           PageLayoutProperties)

    doc = OpenDocumentText()
    doc.fontfacedecls.addElement(FontFace(name=FONT, fontfamily="'" + FONT + "'"))
    doc.fontfacedecls.addElement(FontFace(name="Liberation Serif",
                                          fontfamily="'Liberation Serif'"))

    layout = PageLayout(name="A4Resume")
    # A4 with the retired design margins: 14pt top, 18pt sides, 12pt bottom
    layout.addElement(PageLayoutProperties(
        pagewidth="21cm", pageheight="29.7cm", printorientation="portrait",
        margintop="0.494cm", marginbottom="0.423cm",
        marginleft="0.635cm", marginright="0.635cm"))
    doc.automaticstyles.addElement(layout)
    doc.masterstyles.addElement(MasterPage(name="Standard", pagelayoutname=layout))
    return doc


def para_style(doc, name, size, bold=False, weight=None, color=None,
               align=None, space_before=None, space_after=None,
               line_height=None, underline=False, border_bottom=None,
               padding_bottom=None, letter_spacing=None,
               text_align_last=None, keep_together=False):
    from odf.style import (ParagraphProperties, Style, TextProperties)

    st = Style(name=name, family="paragraph")
    pp_kwargs = {}
    if align:
        pp_kwargs["textalign"] = align
    if text_align_last:
        pp_kwargs["textalignlast"] = text_align_last
    if space_before:
        pp_kwargs["margintop"] = space_before
    if space_after:
        pp_kwargs["marginbottom"] = space_after
    if line_height:
        pp_kwargs["lineheight"] = line_height
    if border_bottom:
        pp_kwargs["borderbottom"] = border_bottom
    if padding_bottom:
        pp_kwargs["paddingbottom"] = padding_bottom
    if keep_together:
        pp_kwargs["keeptogether"] = "always"
    st.addElement(ParagraphProperties(**pp_kwargs))
    tp_kwargs = {"fontsize": size, "fontname": FONT,
                 "fontfamily": "'" + FONT + "',Georgia,serif"}
    if letter_spacing:
        tp_kwargs["letterspacing"] = letter_spacing
    if bold:
        tp_kwargs["fontweight"] = "bold"
    elif weight:
        tp_kwargs["fontweight"] = weight
    if color:
        tp_kwargs["color"] = color
    if underline:
        tp_kwargs["textunderlinestyle"] = "solid"
        tp_kwargs["textunderlinewidth"] = "auto"
        tp_kwargs["textunderlinecolor"] = "font-color"
    st.addElement(TextProperties(**tp_kwargs))
    doc.styles.addElement(st)
    return name


def char_style(doc, name, bold=False, color=None, size=None,
               underline=False):
    from odf.style import Style, TextProperties
    st = Style(name=name, family="text")
    kwargs = {"fontname": FONT,
              "fontfamily": "'" + FONT + "',Georgia,serif"}
    if bold:
        kwargs["fontweight"] = "bold"
    if color:
        kwargs["color"] = color
    if size:
        kwargs["fontsize"] = size
    if underline:
        kwargs["textunderlinestyle"] = "solid"
        kwargs["textunderlinewidth"] = "auto"
    st.addElement(TextProperties(**kwargs))
    doc.styles.addElement(st)


def bullet_list_style(doc):
    from odf.style import ListLevelProperties
    from odf.text import ListLevelStyleBullet, ListStyle

    st = ListStyle(name="ResumeBullets")
    level = ListLevelStyleBullet(level="1", bulletchar="\u2022")
    # Text starts 13pt in (matches retired ul margin); bullet sits in the
    # label box like the old outside marker.
    level.addElement(ListLevelProperties(spacebefore="0.261cm",
                                         minlabelwidth="0.2cm"))
    st.addElement(level)
    doc.styles.addElement(st)


def add_styles(doc, ats):
    # Absolute line heights replicate the retired CSS pt-for-pt. LibreOffice
    # resolves relative (%) line heights against the wrong base, which
    # inflated every line ~28% and repaginated the document.
    sect_size = "12.5pt" if not ats else "11.5pt"
    sect_lh = "15pt" if not ats else "13.8pt"
    para_style(doc, "Name", "21pt", bold=True, align="center",
               line_height="23.1pt", space_after="0.071cm")                # 2pt
    para_style(doc, "Headline", "10pt", bold=True, color="#222222",
               align="center", line_height="14.5pt",
               space_after="0.177cm")                                      # 5pt
    para_style(doc, "Contact", "8.5pt" if not ats else "8.8pt",
               align="center",
               line_height="12.3pt" if not ats else "12.8pt",
               space_after="0.212cm",                                     # 6pt collapsed
               border_bottom="0.7pt solid #222222")
    para_style(doc, "SectionFirst", sect_size,
               bold=True if ats else False,
               weight=None if ats else "600",
               line_height=sect_lh,
               space_before="0.247cm", space_after="0.141cm")              # 7/4pt
    para_style(doc, "Section", sect_size,
               bold=True if ats else False,
               weight=None if ats else "600",
               line_height=sect_lh,
               space_before="0.212cm", space_after="0.141cm")              # 6/4pt
    # ATS gets hairline-negative tracking: LibreOffice sets type a touch
    # wider than the retired engine, which wrapped long lines early and
    # spilled ATS onto two pages. -0.1pt restores the old breaks invisibly.
    # Bullets share it in both variants: design needs the same two wrapped
    # lines pulled back so Education still fits on page one.
    ats_track = "-0.1pt" if ats else None
    bullet_track = "-0.1pt"
    para_style(doc, "Summary", "9.2pt" if not ats else "9.1pt",
               line_height="13.8pt" if not ats else "13.65pt",
               letter_spacing=ats_track)
    para_style(doc, "Role", "9.3pt", bold=True, line_height="12.1pt")
    para_style(doc, "Date", "8.4pt", color="#555555" if not ats else "#333333",
               line_height="12.2pt", space_after="0.088cm")                # 2.5pt
    para_style(doc, "Bullet", "8.7pt", color="#222222",
               line_height="12.2pt", space_after="0.035cm",                # 1pt
               letter_spacing=bullet_track)
    para_style(doc, "BulletLast", "8.7pt", color="#222222",
               line_height="12.2pt", space_after="0.212cm",                # 1+5pt
               letter_spacing=bullet_track)
    para_style(doc, "Project", "8.7pt", color="#222222",
               line_height="12.6pt", space_after="0.088cm",                # 2.5pt
               letter_spacing=ats_track)
    para_style(doc, "TechCat", "8.6pt", bold=True, line_height="12.5pt",
               space_after="0.071cm")                                      # 2pt
    para_style(doc, "TechItems", "8.6pt", line_height="22pt",
               align="justify", text_align_last="justify",
               space_after="0.071cm")                                      # 2pt
    para_style(doc, "EntryTitle", "9.5pt", bold=True, line_height="13.8pt")
    para_style(doc, "EntryMeta", "8.8pt", align="end", line_height="12.8pt")
    para_style(doc, "EntrySub", "8.8pt", line_height="12.8pt",
               space_after="0.035cm", padding_bottom="0.141cm")            # 1+4pt
    para_style(doc, "EntrySubR", "8.8pt", align="end", line_height="12.8pt",
               space_after="0.035cm", padding_bottom="0.141cm")            # 1+4pt
    para_style(doc, "EntryLink", "8.5pt", underline=True,
               line_height="12.3pt", space_after="0.141cm")
    para_style(doc, "Plain", "8.8pt", line_height="12.3pt",
               letter_spacing=ats_track)
    para_style(doc, "SkillsLine", "8.5pt", line_height="12.3pt",
               space_after="0.035cm",                                      # 1pt
               letter_spacing="-0.15pt" if ats else None)
    para_style(doc, "ProfileLabel", "9.5pt", bold=True,
               line_height="13.8pt", space_after="0.035cm")                # 1pt
    para_style(doc, "ProfileLink", "8.8pt", underline=True,
               line_height="12.8pt")
    para_style(doc, "SpokenName", "9pt", bold=True, line_height="13.05pt")
    para_style(doc, "SpokenLevel", "8.8pt", line_height="12.8pt")
    para_style(doc, "Interest", "8.8pt", bold=True, line_height="12.8pt")
    para_style(doc, "InterestT", "8.8pt", bold=True, line_height="12.8pt",
               space_after="0.141cm")                                      # 4pt row gap
    char_style(doc, "B", bold=True)
    char_style(doc, "Gray", color="#999999")
    char_style(doc, "SmallGray", size="7pt", color="#555555")
    char_style(doc, "U", underline=True)
    char_style(doc, "BU", bold=True, underline=True)
    char_style(doc, "Link", color="#111111", underline=True)
    char_style(doc, "LinkB", bold=True, color="#111111", underline=True)
    # LibreOffice paints hyperlinks with its built-in "Internet Link"
    # character style, overriding inner spans. Redefining it here forces
    # the document's dark link styling in both ODT and PDF export.
    char_style(doc, "Internet Link", color="#111111", underline=True)
    char_style(doc, "Visited Internet Link", color="#111111",
               underline=True)
    bullet_list_style(doc)


# ----------------------------------------------------------------------------
# Element helpers
# ----------------------------------------------------------------------------

class Ctx:
    def __init__(self, doc):
        self.doc = doc
        self.png = {}

    def icon_file(self, name):
        if name not in self.png:
            self.png[name] = str(ICONS_PNG / name.replace(".svg", ".png"))
        return self.png[name]


def P(doc, style, text=None):
    from odf.text import P as _P
    p = _P(stylename=style)
    if text:
        p.addText(text)
    doc.text.addElement(p)
    return p


def span(p, text, style=None):
    from odf.text import Span
    s = Span(stylename=style) if style else Span()
    if text:
        s.addText(text)
    p.addElement(s)
    return s


def link(p, href, text, style=None):
    from odf.text import A, Span
    a = A(href=href)
    if style:
        s = Span(stylename=style)
        s.addText(text)
        a.addElement(s)
    else:
        a.addText(text)
    p.addElement(a)
    return a


def image_run(p, ctx, svg_name, size_cm):
    from odf.draw import Frame, Image
    href = ctx.doc.addPicture(ctx.icon_file(svg_name))
    frame = Frame(anchortype="as-char", width=size_cm, height=size_cm)
    frame.addElement(Image(href=href))
    p.addElement(frame)


def table(ctx, col_widths, align="left"):
    from odf.table import Table, TableColumn
    from odf.style import Style, TableProperties
    total_cm = sum(float(w.replace("cm", "")) for w in col_widths)
    tname = "T" + ("%.3f" % total_cm).replace(".", "_")
    if tname not in _table_cache:
        st = Style(name=tname, family="table")
        st.addElement(TableProperties(width="%.3fcm" % total_cm,
                                      align=align))
        ctx.doc.automaticstyles.addElement(st)
        _table_cache[tname] = True
    t = Table(stylename=tname)
    for w in col_widths:
        t.addElement(TableColumn(stylename=_col_style(ctx.doc, w)))
    ctx.doc.text.addElement(t)
    return t


_table_cache = {}


_col_cache = {}


def _col_style(doc, width):
    from odf.style import Style, TableColumnProperties
    if width not in _col_cache:
        name = "Col" + width.replace(".", "_")
        st = Style(name=name, family="table-column")
        st.addElement(TableColumnProperties(columnwidth=width))
        doc.automaticstyles.addElement(st)
        _col_cache[width] = name
    return _col_cache[width]


def row(t, cells):
    """cells: list of (paragraph_style, builder_fn(p))."""
    from odf.table import TableCell, TableRow
    tr = TableRow()
    for style, fill in cells:
        from odf.text import P as _P
        tc = TableCell()
        p = _P(stylename=style)
        fill(p)
        tc.addElement(p)
        tr.addElement(tc)
    t.addElement(tr)


# ----------------------------------------------------------------------------
# Sections
# ----------------------------------------------------------------------------

def header(ctx, ats):
    from odf.text import S
    doc = ctx.doc
    P(doc, "Name", "Subhan Gadirli")
    P(doc, "Headline", "Full-Stack Developer")
    p = P(doc, "Contact")
    if not ats:
        for i, (icon, kind) in enumerate(CONTACT_ICONS):
            if i:
                # Preserved spaces: raw runs collapse in ODF. ~14pt gap
                # replicates the retired flex contact spacing.
                p.addElement(S(c="6"))
            image_run(p, ctx, icon, "0.318cm")
            p.addText(" ")
            if kind[0] == "link":
                link(p, kind[1], kind[2], "Link")
            else:
                p.addText(kind[1])
    else:
        link(p, "mailto:" + EMAIL, EMAIL, "Link")
        p.addText("  |  ")
        link(p, "tel:" + PHONE_RAW, PHONE, "Link")
        p.addElement(S(c="1"))
        span(p, PHONE_RAW, "SmallGray")
        p.addText("  |  " + LOCATION + "  |  ")
        link(p, WEBSITE, WEBSITE, "Link")
def section(doc, title, first=False):
    P(doc, "SectionFirst" if first else "Section", title)


def profiles(ctx):
    doc = ctx.doc
    section(doc, "Profiles", first=True)
    t = table(ctx, ["6.577cm", "6.577cm", "6.576cm"])
    # one row, each cell stacks label + link (two paragraphs per cell)
    from odf.table import TableCell, TableRow
    from odf.text import P as _P
    tr = TableRow()
    for icon, label, handle, url in PROFILES:
        tc = TableCell()
        p1 = _P(stylename="ProfileLabel")
        image_run(p1, ctx, icon, "0.301cm")
        p1.addText(" ")
        span(p1, label, "B")
        tc.addElement(p1)
        p2 = _P(stylename="ProfileLink")
        link(p2, url, handle, "Link")
        tc.addElement(p2)
        tr.addElement(tc)
    t.addElement(tr)


def links_ats(ctx):
    doc = ctx.doc
    section(doc, "Links", first=True)
    p = P(doc, "Plain")
    p.addText("GitHub: ")
    link(p, "https://github.com/subhangadirli", "github.com/subhangadirli", "Link")
    p.addText("  |  LinkedIn: ")
    link(p, "https://www.linkedin.com/in/subhangadirli/",
         "linkedin.com/in/subhangadirli", "Link")
    p.addText("  |  Codeberg: ")
    link(p, "https://codeberg.org/subhangadirli", "codeberg.org/subhangadirli", "Link")


def summary(doc):
    section(doc, "Professional Summary")
    P(doc, "Summary", SUMMARY)


def experience(doc):
    from odf.text import List, ListItem
    from odf.text import P as _P
    section(doc, "Experience")
    for exp in EXPERIENCE:
        P(doc, "Role", exp["role"])
        P(doc, "Date", exp["date"])
        lst = List(stylename="ResumeBullets")
        for i, b in enumerate(exp["bullets"]):
            item = ListItem()
            style = "BulletLast" if i == len(exp["bullets"]) - 1 else "Bullet"
            item.addElement(_P(stylename=style, text=b))
            lst.addElement(item)
        doc.text.addElement(lst)


def projects(doc, ats):
    section(doc, "Projects" if ats else "Selected Projects")
    for name, url, desc in PROJECTS:
        p = P(doc, "Project")
        link(p, url, name, "LinkB")
        p.addText(" - " + desc)


def skills_design(ctx):
    doc = ctx.doc
    section(doc, "Technical Skills")
    for cat, items in SKILLS:
        # Label col 92pt like the retired grid; items col ends where the old
        # rows ended (old rows never filled the full content width).
        t = table(ctx, ["3.246cm", "15.697cm"])
        def catfill(p, cat=cat):
            span(p, cat, "B")
        def itemsfill(p, items=items):
            from odf.text import S
            for j, (icon, label) in enumerate(items):
                if j:
                    span(p, " \u00b7 ", "Gray")
                    # Explicit preserved spaces: raw runs collapse in ODF.
                    # Wide trailing gap replicates the retired flex separator
                    # margins and forces the historical line breaks.
                    p.addElement(S(c="2"))
                image_run(p, ctx, icon, "0.265cm")
                p.addText(" ")
                # No-break space: the retired style never split a label.
                span(p, label.replace(" ", "\u00a0"), "B")
        row(t, [("TechCat", catfill), ("TechItems", itemsfill)])


def skills_ats(doc):
    section(doc, "Skills")
    lines = [
        ("Proficient:", "TypeScript, Python, React, Next.js, SvelteKit, Node.js, Deno, Hono, Drizzle ORM, PostgreSQL, Docker, Git, Linux"),
        ("Familiar:", "JavaScript, Ruby, Astro, Tailwind CSS, Express.js, Flask, Django, Bun, SQLite, Prisma ORM, GitHub, GitLab, Podman, Caddy, Anubis"),
        ("Cloud & Hosting:", "Vercel, Netlify, Heroku, Hetzner (VPS), Cloudflare, AWS Amplify"),
    ]
    for label, value in lines:
        p = P(doc, "SkillsLine")
        span(p, label + " ", "B")
        p.addText(value)


def education(doc, ats):
    section(doc, "Education")
    dates = EDU_DATES["ats" if ats else "design"]
    for edu, datespan in zip(EDUCATION, dates):
        t = table_ctx(doc, ["13cm", "6.73cm"])
        row(t, [
            ("EntryTitle", lambda p, v=edu["title"]: span(p, v, "B")),
            ("EntryMeta", lambda p, v=edu["meta"]: p.addText(v)),
        ])
        t2 = table_ctx(doc, ["13cm", "6.73cm"])
        row(t2, [
            ("EntrySub", lambda p, v=edu["left"]: p.addText(v)),
            ("EntrySubR", lambda p, v=edu["right"].replace("DATES", datespan): p.addText(v)),
        ])


def table_ctx(doc, widths):
    ctx = Ctx(doc)
    return table(ctx, widths)


def certifications(doc):
    section(doc, "Certifications")
    for c in CERTS:
        t = table_ctx(doc, ["13cm", "6.73cm"])
        row(t, [
            ("EntryTitle", lambda p, v=c["title"]: span(p, v, "B")),
            ("EntryMeta", lambda p, v=c["meta"]: p.addText(v)),
        ])
        P(doc, "EntrySub", c["org"])


def languages(ctx):
    doc = ctx.doc
    section(doc, "Languages")
    t = table(ctx, ["9.865cm", "9.865cm"])
    from odf.table import TableCell, TableRow
    from odf.text import P as _P
    tr = TableRow()
    for name, level in LANGUAGES:
        tc = TableCell()
        p1 = _P(stylename="SpokenName")
        span(p1, name, "B")
        tc.addElement(p1)
        tc.addElement(_P(stylename="SpokenLevel", text=level))
        tr.addElement(tc)
    t.addElement(tr)


def interests(ctx):
    doc = ctx.doc
    section(doc, "Interests")
    t = table(ctx, ["6.577cm", "6.577cm", "6.576cm"])
    from odf.table import TableCell, TableRow
    from odf.text import P as _P
    for i in range(0, len(INTERESTS), 3):
        tr = TableRow()
        style = "InterestT" if i == 0 else "Interest"
        for icon, label in INTERESTS[i:i + 3]:
            tc = TableCell()
            p = _P(stylename=style)
            image_run(p, ctx, icon, "0.318cm")
            p.addText(" ")
            span(p, label, "B")
            tc.addElement(p)
            tr.addElement(tc)
        t.addElement(tr)


# ----------------------------------------------------------------------------
# Build
# ----------------------------------------------------------------------------

def build(variant):
    from odf.dc import Title
    ats = variant == "ats"
    doc = new_document()
    doc.meta.addElement(Title(text="Subhan Gadirli Resume" +
                              (" ATS" if ats else "")))
    add_styles(doc, ats)
    ctx = Ctx(doc)
    header(ctx, ats)
    if ats:
        links_ats(ctx)
    else:
        profiles(ctx)
    summary(doc)
    experience(doc)
    projects(doc, ats)
    if ats:
        skills_ats(doc)
    else:
        skills_design(ctx)
    education(doc, ats)
    certifications(doc)
    languages(ctx)
    if not ats:
        interests(ctx)
    return doc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="dist")
    args = ap.parse_args()

    render_icons()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    names = {"design": "Subhan-Gadirli-Resume.odt",
             "ats": "Subhan-Gadirli-Resume-ATS.odt"}
    for variant, fname in names.items():
        doc = build(variant)
        target = out / fname
        doc.save(str(target))
        print("wrote", target)
        # Self-check with stdlib only: fail loudly if a critical
        # formatting attribute did not survive serialization.
        import zipfile
        xml = (zipfile.ZipFile(str(target)).read("styles.xml").decode() +
               zipfile.ZipFile(str(target)).read("content.xml").decode())
        if variant == "design":
            assert 'fo:text-align="justify"' in xml, "justify lost"
            assert 'fo:text-align-last="justify"' in xml, "last-line justify lost"
            assert 'table:align="left"' in xml, "table align lost"
        else:
            assert 'fo:letter-spacing="-0.1pt"' in xml, "ATS tracking lost"


if __name__ == "__main__":
    sys.exit(main())
