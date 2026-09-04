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
               keep_together=False):
    from odf.style import (ParagraphProperties, Style, TextProperties)

    st = Style(name=name, family="paragraph")
    pp_kwargs = {}
    if align:
        pp_kwargs["textalign"] = align
    if space_before:
        pp_kwargs["margintop"] = space_before
    if space_after:
        pp_kwargs["marginbottom"] = space_after
    if line_height:
        pp_kwargs["lineheight"] = line_height
    if border_bottom:
        pp_kwargs["borderbottom"] = border_bottom
    if keep_together:
        pp_kwargs["keeptogether"] = "always"
    st.addElement(ParagraphProperties(**pp_kwargs))
    tp_kwargs = {"fontsize": size, "fontname": FONT,
                 "fontfamily": "'" + FONT + "',Georgia,serif"}
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
    level.addElement(ListLevelProperties(spacebefore="0.459cm",
                                         minlabelwidth="0.45cm"))
    st.addElement(level)
    doc.styles.addElement(st)


def add_styles(doc, ats):
    para_style(doc, "Name", "21pt", bold=True, align="center",
               space_after="0.071cm")                                   # 2pt
    para_style(doc, "Headline", "10pt", bold=True, color="#222222",
               align="center", space_after="0.177cm")                    # 5pt
    para_style(doc, "Contact", "8.5pt" if not ats else "8.8pt",
               align="center", space_after="0.141cm")                    # 4pt
    para_style(doc, "Divider", "2pt", space_before="0.212cm",            # 6pt
               space_after="0.247cm", border_bottom="0.7pt solid #222222")
    para_style(doc, "Section", "12.5pt" if not ats else "11.5pt",
               bold=False if not ats else True,
               weight="600" if not ats else None,
               space_before="0.212cm", space_after="0.141cm")            # 6/4pt
    para_style(doc, "Summary", "9.2pt" if not ats else "9.1pt",
               line_height="150%")
    para_style(doc, "Role", "9.3pt", bold=True, space_before="0.177cm")  # 5pt
    para_style(doc, "Date", "8.4pt", color="#555555" if not ats else "#333333",
               space_after="0.053cm")
    para_style(doc, "Bullet", "8.7pt", color="#222222", line_height="140%")
    para_style(doc, "Project", "8.7pt", color="#222222",
               line_height="145%", space_after="0.088cm")
    para_style(doc, "TechCat", "8.6pt", bold=True, space_after="0.071cm")
    para_style(doc, "TechItems", "8.6pt", line_height="145%",
               space_after="0.071cm")
    para_style(doc, "EntryTitle", "9.5pt", "B")
    para_style(doc, "EntryMeta", "8.8pt", align="end")
    para_style(doc, "EntrySub", "8.8pt", space_after="0.035cm")
    para_style(doc, "EntrySubR", "8.8pt", align="end", space_after="0.035cm")
    para_style(doc, "EntryLink", "8.5pt", underline=True,
               space_after="0.141cm")
    para_style(doc, "Plain", "8.8pt", line_height="140%")
    para_style(doc, "SkillsLine", "8.5pt", line_height="145%",
               space_after="0.035cm")
    para_style(doc, "ProfileLabel", "9.5pt", bold=True, space_after="0.035cm")
    para_style(doc, "ProfileLink", "8.8pt", underline=True)
    para_style(doc, "SpokenName", "9pt", bold=True)
    para_style(doc, "SpokenLevel", "8.8pt")
    para_style(doc, "Interest", "8.8pt", bold=True)
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


def table(ctx, col_widths):
    from odf.table import Table, TableColumn
    t = Table()
    for w in col_widths:
        t.addElement(TableColumn(stylename=_col_style(ctx.doc, w)))
    ctx.doc.text.addElement(t)
    return t


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
    doc = ctx.doc
    P(doc, "Name", "Subhan Gadirli")
    P(doc, "Headline", "Full-Stack Developer")
    p = P(doc, "Contact")
    if not ats:
        for i, (icon, kind) in enumerate(CONTACT_ICONS):
            if i:
                p.addText("   ")
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
        span(p, " " + PHONE_RAW, "SmallGray")
        p.addText("  |  " + LOCATION + "  |  ")
        link(p, WEBSITE, WEBSITE, "Link")
    P(doc, "Divider")


def section(doc, title):
    P(doc, "Section", title)


def profiles(ctx):
    doc = ctx.doc
    section(doc, "Profiles")
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
    section(doc, "Links")
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
        for b in exp["bullets"]:
            item = ListItem()
            item.addElement(_P(stylename="Bullet", text=b))
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
        t = table(ctx, ["3.246cm", "16.484cm"])
        def catfill(p, cat=cat):
            span(p, cat, "B")
        def itemsfill(p, items=items):
            for j, (icon, label) in enumerate(items):
                if j:
                    span(p, " \u00b7 ", "Gray")
                    p.addText(" ")
                image_run(p, ctx, icon, "0.265cm")
                p.addText(" ")
                span(p, label, "B")
        row(t, [("TechItems", catfill), ("TechItems", itemsfill)])


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
        for icon, label in INTERESTS[i:i + 3]:
            tc = TableCell()
            p = _P(stylename="Interest")
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


if __name__ == "__main__":
    sys.exit(main())
