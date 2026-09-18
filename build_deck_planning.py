#!/usr/bin/env python3
"""Build the planning-faithful interview deck.

Follows the four-topic structure of 'planning.md' exactly (DEM theory &
conveyor systems / SOTA & knowledge gaps / methodology & novelty /
personal skills), and backs every claim with figures from the papers in
'papers/particles-based models/'.
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image
import os

SRC = "presentation/Delft Phd scrap handling.pptx"   # the started deck (logos/title)
OUT = "presentation/Delft Phd scrap handling - planning.pptx"
FIG = "/tmp/figset"

BLUE   = RGBColor(0x00, 0xA4, 0xE4)
NAVY   = RGBColor(0x14, 0x3B, 0x5C)
DARK   = RGBColor(0x2B, 0x2B, 0x2B)
GRAY   = RGBColor(0x6B, 0x6B, 0x6B)
LIGHT  = RGBColor(0xEA, 0xF4, 0xFB)
LIGHT2 = RGBColor(0xF5, 0xF9, 0xFC)
AMBER  = RGBColor(0xE8, 0xA3, 0x3D)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
LINEGRAY = RGBColor(0xD9, 0xD9, 0xD9)
FONT = "Calibri"

prs = Presentation(SRC)
BLANK = next(l for l in prs.slide_layouts if l.name == "Blank")

def _set_run(r, size=12, bold=False, color=DARK, italic=False, font=FONT):
    r.font.size = Pt(size); r.font.bold = bold; r.font.italic = italic
    r.font.color.rgb = color; r.font.name = font

def add_box(slide, x, y, w, h):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = True
    tf.margin_left = 0; tf.margin_right = 0; tf.margin_top = 0; tf.margin_bottom = 0
    return tb, tf

def para(tf, text, size=12, bold=False, color=DARK, align=PP_ALIGN.LEFT,
         space_after=4, space_before=0, line=1.0, first=False, italic=False):
    p = tf.paragraphs[0] if first and not tf.paragraphs[0].runs else tf.add_paragraph()
    p.alignment = align; p.space_after = Pt(space_after); p.space_before = Pt(space_before)
    p.line_spacing = line
    r = p.add_run(); r.text = text
    _set_run(r, size=size, bold=bold, color=color, italic=italic)
    return p

def bullets(tf, items, size=11.5, color=DARK, space_after=7, line=1.06, first=True):
    started = first
    for it in items:
        text = it[0]; bold = it[1] if len(it) > 1 else False
        p = tf.paragraphs[0] if started and not tf.paragraphs[0].runs else tf.add_paragraph()
        started = False
        p.space_after = Pt(space_after); p.line_spacing = line
        pPr = p._p.get_or_add_pPr()
        pPr.set("marL", "0")
        r1 = p.add_run(); r1.text = "•  "; _set_run(r1, size=size, bold=True, color=BLUE)
        r2 = p.add_run(); r2.text = text; _set_run(r2, size=size, bold=bold, color=color)

def header(slide, kicker, title, idx):
    tb, tf = add_box(slide, 0.45, 0.26, 12.4, 0.85)
    para(tf, kicker, size=10.5, bold=True, color=BLUE, space_after=2, first=True)
    para(tf, title, size=25, bold=True, color=NAVY, space_after=0, line=0.98)
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.47), Inches(1.06),
                                 Inches(1.35), Inches(0.045))
    bar.fill.solid(); bar.fill.fore_color.rgb = BLUE
    bar.line.fill.background(); bar.shadow.inherit = False
    footer(slide, idx)

def footer(slide, idx):
    ln = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.45), Inches(7.12),
                                Inches(12.43), Inches(0.012))
    ln.fill.solid(); ln.fill.fore_color.rgb = LINEGRAY
    ln.line.fill.background(); ln.shadow.inherit = False
    tb, tf = add_box(slide, 0.45, 7.17, 9.5, 0.3)
    para(tf, "Particle-Based Modelling of Scrap Handling  •  aligned with the 4-topic research plan (planning.md)  •  TU Delft × Tata Steel",
         size=8, color=GRAY, first=True)
    tb2, tf2 = add_box(slide, 12.0, 7.17, 0.88, 0.3)
    para(tf2, str(idx), size=9, bold=True, color=GRAY, align=PP_ALIGN.RIGHT, first=True)

def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text

def new_slide():
    return prs.slides.add_slide(BLANK)

_fig_cache = {}
def aspect(key):
    if key not in _fig_cache:
        im = Image.open(f"{FIG}/{key}.jpg")
        _fig_cache[key] = im.size[0] / im.size[1]
    return _fig_cache[key]

def place_fig(slide, key, x, y, max_w, max_h, caption, cap_color=GRAY):
    """Place figure in the (x, y, max_w, max_h) slot; bottom 0.30in reserved for caption."""
    a = aspect(key)
    usable_h = max_h - 0.30
    w = max_w; h = w / a
    if h > usable_h:
        h = usable_h; w = h * a
    if w > max_w:
        w = max_w; h = w / a
    px = x + (max_w - w) / 2
    py = y + (usable_h - h) / 2 + 0.02
    slide.shapes.add_picture(f"{FIG}/{key}.jpg", Inches(px), Inches(py), Inches(w), Inches(h))
    tb, tf = add_box(slide, x, y + max_h - 0.26, max_w, 0.24)
    para(tf, caption, size=7.5, color=cap_color, align=PP_ALIGN.CENTER, first=True)

def card(slide, x, y, w, h, fill=LIGHT, line_color=BLUE, line_w=1.0):
    shp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    shp.fill.solid(); shp.fill.fore_color.rgb = fill
    if line_color is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line_color; shp.line.width = Pt(line_w)
    shp.shadow.inherit = False
    try: shp.adjustments[0] = 0.045
    except Exception: pass
    return shp

def reading_card(slide, x, y, w, h, paper, why):
    """Card quoting the plan's 'Proposed Reading' + 'Why you need it'."""
    card(slide, x, y, w, h, fill=LIGHT2, line_color=BLUE, line_w=1.1)
    acc = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y + 0.14),
                                 Inches(0.05), Inches(h - 0.28))
    acc.fill.solid(); acc.fill.fore_color.rgb = AMBER
    acc.line.fill.background(); acc.shadow.inherit = False
    tb, tf = add_box(slide, x + 0.18, y + 0.14, w - 0.34, h - 0.28)
    para(tf, "PROPOSED READING  (plan)", size=8.5, bold=True, color=AMBER, space_after=3, first=True)
    para(tf, paper, size=10, bold=True, color=NAVY, space_after=5, line=1.02)
    p = tf.add_paragraph(); p.line_spacing = 1.04; p.space_after = Pt(0)
    r1 = p.add_run(); r1.text = "Why you need it:  "; _set_run(r1, size=9, bold=True, color=DARK)
    r2 = p.add_run(); r2.text = why; _set_run(r2, size=9, color=GRAY)

# =====================================================================
# SLIDE 1 — title (kept from started deck)
# =====================================================================
notes(prs.slides[0], "This deck follows the 4-topic structure of the research plan (planning.md) exactly. Every topic is illustrated with figures taken directly from the papers in the repository ('papers/particles-based models').")

# =====================================================================
# SLIDE 2 — agenda = the plan's four topics
# =====================================================================
s = new_slide()
header(s, "AGENDA  ·  THE RESEARCH PLAN IN FOUR TOPICS", "From Granular Physics to the Harsh Reality of Scrap Yards", 2)
topics = [
    ("1", "DEM theory & conveyor systems",
     "Core mathematical framework (shape & contact) • belt & chute kinematics • vibratory feeders"),
    ("2", "State of the art & knowledge gaps",
     "Three gaps between mature bulk-handling DEM and mature EAF melting CFD"),
    ("3", "Methodology, novelty & challenges",
     "The coarse-graining dilemma • a multi-scale, multi-property digital twin"),
    ("4", "Personal skills & competencies",
     "DEM software (EDEM / Rocky / LIGGGHTS) • experimental validation workflows"),
]
cw, ch = 3.0, 3.15
for i, (n, t, sub) in enumerate(topics):
    x = 0.45 + i * (cw + 0.145)
    y = 1.45
    card(s, x, y, cw, ch, fill=LIGHT2, line_color=BLUE, line_w=1.1)
    c = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x + 0.18), Inches(y + 0.18), Inches(0.5), Inches(0.5))
    c.fill.solid(); c.fill.fore_color.rgb = BLUE
    c.line.fill.background(); c.shadow.inherit = False
    ctf = c.text_frame; ctf.vertical_anchor = MSO_ANCHOR.MIDDLE
    cp = ctf.paragraphs[0]; cp.alignment = PP_ALIGN.CENTER
    cr = cp.add_run(); cr.text = n; _set_run(cr, size=16, bold=True, color=WHITE)
    tb, tf = add_box(s, x + 0.82, y + 0.24, cw - 1.0, 0.85)
    para(tf, t, size=13.5, bold=True, color=NAVY, first=True, line=0.98)
    tb, tf = add_box(s, x + 0.2, y + 1.05, cw - 0.4, ch - 1.2)
    para(tf, sub, size=10, color=GRAY, first=True, line=1.08)
band = card(s, 0.45, 5.0, 12.43, 0.62, fill=NAVY, line_color=None)
tf = band.text_frame; tf.word_wrap = True; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
tf.margin_left = Inches(0.2)
p = tf.paragraphs[0]
r = p.add_run()
r.text = ("Every topic below is built on the plan's 'Proposed Readings' — illustrated with figures from the "
          "papers in the repository. Backed by Tata Steel Netherlands: industrially calibrated simulation "
          "separates this project from idealised spherical-particle work (plan, opening line).")
_set_run(r, size=10.5, color=WHITE)
notes(s, "One line: this presentation is the plan itself, made visual. Topic 1 = the core mechanics; Topic 2 = the frontier and the gaps; Topic 3 = the defensible 4-year methodology; Topic 4 = why I am the right candidate to run it at Tata Steel NL.")

# =====================================================================
# SLIDE 3 — T1a core framework (shape & contact)
# =====================================================================
s = new_slide()
header(s, "TOPIC 1 · THEORY OF PARTICLE-BASED MODELS (DEM) & CONVEYOR SYSTEMS",
       "Core Framework: Non-Spherical Representation & Contact", 3)
tb, tf = add_box(s, 0.45, 1.28, 4.35, 3.3)
para(tf, "What the plan demands", size=12.5, bold=True, color=NAVY, first=True, space_after=6)
bullets(tf, [
    ("“Scrap is never round” — the heavy computational tradeoffs of non-spherical shapes must be shown", True),
    ("Three representations, each with a cost: multi-sphere clusters, polyhedra, superquadrics", False),
    ("Contact-detection mechanics dominates runtime: > 80% of CPU in non-spherical DEM (Lu et al. 2015)", False),
    ("Choice of representation = choice of physics: shape affects packing, piling, discharge", False),
], size=10.5, space_after=7)
reading_card(s, 0.45, 4.75, 4.35, 2.05,
    "“DEM/CFD-DEM Modelling of Non-Spherical Particulate Systems: Theoretical Developments and Applications”",
    "Outlines how to mathematically represent non-spherical particles (multi-sphere clusters, polyhedra, superquadrics) and handle complex contact-detection mechanics.")
place_fig(s, "s3_clumps",    5.05, 1.28, 3.95, 2.55, "Multi-sphere clumps from 3D-scanned grains (Rossow & Coetzee, 2021, Fig. 1)")
place_fig(s, "s3_polyhedra", 9.15, 1.28, 3.75, 2.55, "Voxelised non-convex polyhedron (Lu et al., 2015, Fig. 14)")
place_fig(s, "s3_fig3",      5.05, 3.95, 5.20, 2.85, "Contact point, normal & overlap: spheres vs non-sphericals (Lu et al., 2015, Fig. 3)")
place_fig(s, "s4_family",    10.45, 3.95, 2.45, 2.85, "Super-quadric family, shape index s (You et al., 2018)")
notes(s, "Plan topic 1.1. The plan attributes this reading to 'Zhou et al.'; the corresponding papers in the repository are Zhong et al. (2016), Powder Technology 300:109–127 (plan refs [2,3]) and Lu et al. (2015), CES 127:425–465 (refs [4,5] cover the same framework). Walk the four quadrants: clumps (top-left) = the workflow we will use for 3D-scanned scrap; polyhedra (top-right) = angular geometry; Fig. 3 (bottom-left) = why contact mechanics is hard (contact-point jumps → multi-point contacts); super-quadrics (bottom-right) = smooth systematic variation. Message: representation choice is a physics choice, and it drives the >80% contact-detection cost.")

# =====================================================================
# SLIDE 4 — T1b belt conveyor & chute transfer
# =====================================================================
s = new_slide()
header(s, "TOPIC 1 · THEORY OF PARTICLE-BASED MODELS (DEM) & CONVEYOR SYSTEMS",
       "Belt & Chute Kinematics: Tracking at Moving Boundaries", 4)
tb, tf = add_box(s, 0.45, 1.28, 4.35, 3.3)
para(tf, "What the plan demands", size=12.5, bold=True, color=NAVY, first=True, space_after=6)
bullets(tf, [
    ("Precise tracking of material velocity along the belt", False),
    ("Preferential wear on chute linings; avoiding stagnation zones during belt discharge", False),
    ("“Perfect for mapping continuous furnace infeed” (plan)", True),
    ("Chevron belts grip material by geometry, not friction alone — first DEM study of a chevron belt (Rossow & Coetzee 2021)", False),
], size=10.5, space_after=7)
reading_card(s, 0.45, 4.75, 4.35, 2.05,
    "“Discrete Element Modelling of a Bulk Cohesive Material Discharging from a Belt Conveyor onto an Inclined Impact Plate”",
    "Covers precise tracking of material velocity, preferential wear on chute linings, and avoiding stagnation zones during belt discharge — perfect for mapping continuous furnace infeed.")
place_fig(s, "s6_chev_cad",  5.05, 1.28, 3.95, 2.55, "Chevron-patterned belt in the DEM model (Rossow & Coetzee, 2021, Fig. 3a)")
place_fig(s, "s6_belt_flow", 9.15, 1.28, 3.75, 2.55, "Material flow on the chevron belt — DEM vs footage (Rossow & Coetzee, 2021, Fig. 8)")
place_fig(s, "s8_discharge", 5.05, 3.95, 3.95, 2.85, "Discharge from belt to inclined impact plate — experiment (Schefler & Coetzee, 2023)")
place_fig(s, "s7_chute",     9.15, 3.95, 3.75, 2.85, "Chute transfer flow — DEM vs high-speed footage (Rossow & Coetzee, 2021, Fig. 13)")
notes(s, "Plan topic 1.2. The plan's ref [6] is the MDPI paper (2075-163X/13/12/1501) = Schefler & Coetzee (2023), Minerals 13(12):1501 — it is in the repository; ref [7] is the Rossow thesis (ro.uow.edu.au). The plan attributes the reading to 'Hastie'; the actual authors of the MDPI paper are Schefler & Coetzee (Hastie & Wypych is a cited reference inside it). Points: velocity tracking, chute-liner wear, stagnation zones — exactly the three quantities we need for continuous furnace infeed. Validation standard shown: particle-by-particle DEM vs high-speed footage.")

# =====================================================================
# SLIDE 5 — T1c vibratory feeders
# =====================================================================
s = new_slide()
header(s, "TOPIC 1 · THEORY OF PARTICLE-BASED MODELS (DEM) & CONVEYOR SYSTEMS",
       "Vibratory Feeders: Dynamic Friction, Sorting & Discharge", 5)
tb, tf = add_box(s, 0.45, 1.28, 4.35, 3.3)
para(tf, "What the plan demands", size=12.5, bold=True, color=NAVY, first=True, space_after=6)
bullets(tf, [
    ("Vibratory feeders induce highly dynamic contact friction and segregation", False),
    ("Frequency & amplitude change the velocity distribution and discharge sequence of heterogeneous streams", True),
    ("Design rule: effective separation when (2πf)²A ≈ 1.5 g (You et al. 2018)", False),
    ("Real scrap feeding speed is measurable today with vision tracking (Xiao et al. 2024)", False),
], size=10.5, space_after=7)
reading_card(s, 0.45, 4.75, 4.35, 2.05,
    "“Investigation of the Vibration Sorting of Non-Spherical Particles Based on DEM Simulation”",
    "Vibratory feeders induce highly dynamic contact friction and segregation. This text helps you explain how vibration frequencies and amplitudes change the velocity distribution and discharge sequences of heterogeneous material streams.")
place_fig(s, "s9_device",    5.05, 1.28, 7.85, 2.35, "Vibration sorting device — experiment & DEM side by side (You et al., 2018, Fig. 6)")
place_fig(s, "s9_sorting",   5.05, 3.75, 2.55, 3.00, "Separation patterns on the vibrating plate — DEM (You et al., 2018)")
place_fig(s, "s9_dem_models",7.75, 3.75, 2.55, 3.00, "DEM super-ellipsoid models: sphere & cube (You et al., 2018)")
place_fig(s, "s10_speed",    10.45, 3.75, 2.45, 3.00, "Feeding speed vs vibrator frequency — on-site (Xiao et al., 2024)")
notes(s, "Plan topic 1.3. Plan refs [8,9]; the repository paper is You et al. (2018), Powder Technology (the plan cites it as 'Jiang et al.' — the ResearchGate link [8] is the same paper; first author You). Why this matters for scrap: heterogeneous recipes (bales + shreds + HMS) on a vibratory feeder self-segregate before the chute. The 1.5g rule tells us when sorting happens — we will use it to predict which scrap discharges first and prevent chute blockage. Bottom-right: real on-site scrap feeding data already exists (Xiao et al. 2024) — our validation target.")

# =====================================================================
# SLIDE 6 — T2a state of the art
# =====================================================================
s = new_slide()
header(s, "TOPIC 2 · STATE OF THE ART & KNOWLEDGE GAPS IN SCRAP/EAF MODELLING",
       "Two Mature Pillars — and the Missing Bridge", 6)
tb, tf = add_box(s, 0.45, 1.24, 12.4, 1.35)
bullets(tf, [
    ("Pillar 1 — non-spherical DEM for bulk handling: mature, calibrated, validated across industry (Zhong et al. 2016)", False),
    ("Pillar 2 — EAF melting CFD: fully 3-D, industrially validated in a 150-t furnace (Chen et al. 2022)", False),
    ("The missing bridge — mechanical, multi-property tracking of heterogeneous scrap infeed (plan, Topic 2)", True),
], size=11, space_after=5)
place_fig(s, "s13_apps", 0.45, 2.78, 4.55, 3.95, "DEM applications across industry — bulk handling is everywhere (Zhong et al., 2016, Fig. 1)")
place_fig(s, "s12_eaf3d", 5.25, 2.78, 3.85, 3.95, "3-D EAF model: electrodes, scrap pile, burners, hot heel (Chen et al., 2022)")
bridge = card(s, 9.35, 2.78, 3.55, 3.95, fill=NAVY, line_color=None)
tb, tf = add_box(s, 9.58, 3.0, 3.1, 3.5)
para(tf, "THE BRIDGE", size=11, bold=True, color=AMBER, first=True, space_after=8)
para(tf, "How the charge actually arrives — structure, sequence, segregation, composition — is not resolved by either pillar.",
     size=10.5, color=WHITE, line=1.15, space_after=8)
para(tf, "That is the PhD project.", size=11.5, bold=True, color=WHITE)
notes(s, "Balance slide: we do NOT question either pillar — both are excellent and validated. The plan's Topic 2 asks us to 'establish the absolute frontier and highlight exactly what the academic community hasn't solved yet.' The frontier = industrial plant-geometry DEM + industrial EAF CFD. The unsolved piece = the mechanical, multi-property infeed interface between them. The next slide makes the three concrete gaps explicit (plan's table).")

# =====================================================================
# SLIDE 7 — T2b the three knowledge gaps (plan table)
# =====================================================================
s = new_slide()
header(s, "TOPIC 2 · STATE OF THE ART & KNOWLEDGE GAPS IN SCRAP/EAF MODELLING",
       "Three Knowledge Gaps to Close (Plan, Topic 2)", 7)
gaps = [
    ("1 · Industrial co-segregation & charging geometry",
     "SOTA: industrial multi-component segregation in blast-furnace charging with actual plant geometry — Tata Steel IJmuiden (Ahmed et al., 2026). "
     "Gap: existing models handle uniform raw materials (e.g. iron-ore pellets); applying this plant-geometry framework to chaotic, large-scale steel scrap is open.",
     "Plan ref [1] — ScienceDirect S0032591026000045 · external to the repository; figure illustrates the phenomenon",
     "s13_buckets", "Charge buckets enter the furnace as discrete, structured inputs (Chen et al., 2022)"),
    ("2 · Scrap chute behaviour & calibration",
     "SOTA: experimental + DEM analysis of galvanized steel scrap along and after an inclined chute (ResearchGate). "
     "Gap: most EAF models focus on thermal/CFD chemistry in the furnace — not the mechanical, physical flow tracking of scrap during continuous feeding.",
     "Plan ref [2] — ResearchGate · external to the repository; figure illustrates the phenomenon",
     "s7_impact", "Mechanical flow tracking at the impact plate — DEM vs footage (Rossow & Coetzee, 2021, Fig. 10)"),
    ("3 · Material heterogeneity & chemical analytics",
     "SOTA: modelling scrap composition in EAF & basic-oxygen furnace processes (arXiv). "
     "Gap: plant models rely on post-facto statistical mass balances / statistical AI — physical particle tracking (size, shape, bulk density) is not linked to real-time spatial distribution during infeed.",
     "Plan ref [3] — arXiv · external to the repository; figure illustrates the phenomenon",
     "s5_bed", "Shape-driven bed structure & layering — heterogeneity made visible (Zhong et al., 2016, Fig. 45)"),
]
for i, (t, body, src, key, cap) in enumerate(gaps):
    y = 1.28 + i * 1.86
    card(s, 0.45, y, 8.15, 1.70, fill=LIGHT2, line_color=BLUE, line_w=1.0)
    tb, tf = add_box(s, 0.63, y + 0.10, 7.8, 1.52)
    para(tf, t, size=11, bold=True, color=NAVY, first=True, space_after=3)
    para(tf, body, size=8.8, color=DARK, space_after=3, line=1.03)
    para(tf, src, size=7.5, color=GRAY, italic=True, space_after=0)
    place_fig(s, key, 8.75, y, 4.15, 1.70, cap)
notes(s, "This is the plan's Topic 2 table, reproduced. The three gap studies are external to the repository (ScienceDirect / ResearchGate / arXiv) — I have read them; the figures here illustrate each phenomenon with papers I do have. Gap 1: co-segregation at real plant scale (the Tata BF charging work shows the methodology exists for uniform burden; scrap is the open case). Gap 2: mechanical flow tracking of scrap before melting — exactly what Rossow/Schefler demonstrate is doable for other materials. Gap 3: linking particle-level tracking to real-time spatial distribution — the digital-twin requirement.")

# =====================================================================
# SLIDE 8 — T3a coarse-graining dilemma
# =====================================================================
s = new_slide()
header(s, "TOPIC 3 · METHODOLOGY, NOVELTY & ANTICIPATED CHALLENGES",
       "The Calibration Challenge: the Coarse-Graining Dilemma", 8)
tb, tf = add_box(s, 0.45, 1.28, 4.35, 3.3)
para(tf, "What the plan demands", size=12.5, bold=True, color=NAVY, first=True, space_after=6)
bullets(tf, [
    ("Scrap piles span millimetres to metres — simulating every particle is computationally impossible (plan)", True),
    ("Upscaling has validated limits: scale ≤ 1.6 keeps error ≤ 10% (Rossow & Coetzee 2021, Table 9)", False),
    ("The limit is a geometric property of the quantity measured — and grows with cohesion (Schefler & Coetzee 2023)", False),
    ("Angle-of-repose experiments validate the virtual model; shape raises the pile angle (Lu et al. 2015)", False),
], size=10.5, space_after=7)
reading_card(s, 0.45, 4.75, 4.35, 2.05,
    "“Optimization of Discrete Element Method Model to Obtain Stable and Reliable Numerical Results of Mechanical Response of Granular Materials” (MDPI)",
    "Steel scrap piles vary from millimetres to metres. You must explain the methodology for coarse-graining / upscaling the particles while using angle-of-repose physical experiments to validate the virtual model's accuracy.")
place_fig(s, "s5_aor",     5.05, 1.28, 7.85, 2.50, "Angle-of-repose piles — the shape effect (Lu et al., 2015, Fig. 32)")
place_fig(s, "s8_table9",  5.05, 3.88, 7.85, 2.92, "Scale factor vs error — red = > 10% = inaccurate (Rossow & Coetzee, 2021, Table 9)")
notes(s, "Plan topic 3.1 — the structural defence of the 4-year plan. The reading (plan ref [10], MDPI Minerals 2024, 14(8):758) is external; the figures give the argument numbers: 1.6× upscaling is validated (≤10% error), the limit depends on the bulk quantity of interest, cohesion relaxes it, and angle-of-repose is the cheapest physical validation (a tilt-box experiment on virtual-scrap vs real-scrap). Methodology in one sentence: represent mm–m scrap at multiple scales, each scale validated against a physical experiment (AOR, discharge, force).")

# =====================================================================
# SLIDE 9 — T3b core novelty
# =====================================================================
s = new_slide()
header(s, "TOPIC 3 · METHODOLOGY, NOVELTY & ANTICIPATED CHALLENGES",
       "Core Novelty: a Multi-Property Digital Twin of Scrap", 9)
tb, tf = add_box(s, 0.45, 1.28, 4.35, 5.5)
para(tf, "What the plan demands", size=12.5, bold=True, color=NAVY, first=True, space_after=6)
bullets(tf, [
    ("A multi-scale, multi-property characterisation model that transforms raw Tata Steel data into a dynamic digital twin (plan)", True),
    ("“You aren't just simulating generic rocks” — multi-material recipes: bale scrap, shredded scrap, heavy-melting scrap", False),
    ("Recipes move in real industrial environments — Tata Steel NL conveyors, feeders, chutes, furnace", False),
    ("Deliverable: a calibrated, validated DEM twin of the infeed that hands off to EAF melting models (e.g. Chen 2022)", False),
], size=10.5, space_after=8)
place_fig(s, "s10_feeder",  5.05, 1.28, 7.85, 2.45, "Real heterogeneous scrap recipes on the vibratory feeder, with feature tracking (Xiao et al., 2024)")
place_fig(s, "s12_pit",     5.05, 3.83, 3.85, 2.95, "Real industrial environment: measured vs simulated pit, 150-t EAF (Chen et al., 2022)")
place_fig(s, "s12_dualcell",9.15, 3.83, 3.75, 2.95, "Today scrap enters EAF models as a lumped stack — the history we recover (Chen et al., 2022)")
notes(s, "Plan topic 3.2 — the novelty in the plan's own words: multi-scale + multi-property + digital twin + real recipes in a real plant. The three figures say it without adjectives: top = the actual heterogeneous material we track (bales, shreds, HMS); bottom-left = the plant-scale validation standard we hand results to (Chen et al. 2022, NLMK 150-t EAF); bottom-right = what today's models do with scrap — a lumped stack with no mechanical history. Our twin supplies that history.")

# =====================================================================
# SLIDE 10 — T4a software literacy
# =====================================================================
s = new_slide()
header(s, "TOPIC 4 · REFLECTION ON PERSONAL SKILLS & COMPETENCIES",
       "Software Literacy: Three DEM Platforms, One Physics", 10)
sw = [
    ("Altair EDEM", "commercial industry-standard granular-flow engine; conveyor & chute modules (plan refs [14–18])"),
    ("Ansys Rocky", "commercial DEM engine — GPU-accelerated, tuned for industrial scale-up studies"),
    ("LIGGGHTS / MFIX-DEM", "open-source: LIGGGHTS DEM + MFIX-DEM two-way-coupled gas–solids extension (Garg et al. 2012)"),
]
cw = 4.02
for i, (t, b) in enumerate(sw):
    x = 0.45 + i * (cw + 0.185)
    card(s, x, 1.28, cw, 1.55, fill=LIGHT2, line_color=BLUE, line_w=1.0)
    tb, tf = add_box(s, x + 0.16, 1.40, cw - 0.32, 1.32)
    para(tf, t, size=12.5, bold=True, color=NAVY, first=True, space_after=4)
    para(tf, b, size=9.5, color=GRAY, line=1.05)
place_fig(s, "mfix_arch",   0.45, 3.05, 6.55, 3.75, "MFIX-DEM architecture: DEM + CDM with two-way-coupled gas–solids flow (Garg et al., 2012)")
place_fig(s, "mfix_spring", 7.20, 3.05, 5.65, 3.75, "The linear spring–dashpot contact model implemented in all three platforms (Garg et al., 2012)")
notes(s, "Plan topic 4.1: 'reference these software tools in your slides' — Altair EDEM, Ansys Rocky, open-source LIGGGHTS. I can talk about all three at two levels: the UI level (conveyor model, moving boundaries, export) and the physics level (the spring–dashpot contact model, Fig. right; the DEM/CDM coupling in MFIX-DEM, Fig. left). The open-source route also means I can modify the solver itself — relevant for the multi-property extension.")

# =====================================================================
# SLIDE 11 — T4b data integration & experimental validation
# =====================================================================
s = new_slide()
header(s, "TOPIC 4 · REFLECTION ON PERSONAL SKILLS & COMPETENCIES",
       "Data Integration & Experimental Validation", 11)
tb, tf = add_box(s, 0.45, 1.28, 4.35, 5.5)
para(tf, "What the plan demands", size=12.5, bold=True, color=NAVY, first=True, space_after=6)
bullets(tf, [
    ("Execute physical boundary validations at Tata Steel: dropping tests, tilting boxes, tracking feeder mass-flow rates (plan)", True),
    ("Goal: “the numerical code mirrors the true physical mechanics” (plan)", False),
    ("High-speed video + PIV at the impact plate: particle-by-particle DEM comparison (Rossow & Coetzee 2021)", False),
    ("A full calibrated parameter set per material–surface pair — stiffness, damping, sliding & rolling friction (Rossow & Coetzee 2021, Table 2)", False),
], size=10.5, space_after=8)
place_fig(s, "rossow_fric_rig", 5.05, 1.28, 7.85, 2.00, "Particle–wall friction test: inclined (tilt) tester & rotating-surface rig (Rossow & Coetzee, 2021, Fig. 2)")
place_fig(s, "rossow_table2",   5.05, 3.38, 4.55, 3.00, "The calibrated parameter set per pair (Rossow & Coetzee, 2021, Table 2)")
place_fig(s, "s10_speed",       9.80, 3.38, 3.10, 3.00, "Tracking feeder mass flow: speed vs vibrator frequency, on-site (Xiao et al., 2024)")
notes(s, "Plan topic 4.2: the three validation workflows named in the plan — dropping tests (coefficient of restitution), tilting boxes (angle of repose → friction), feeder mass-flow tracking — each shown with the apparatus or the data. Top: the tilt-tester and rotating-surface friction rigs (Rossow & Coetzee 2021, Fig. 2). Bottom-left: what validation outputs — a complete, cited parameter set (Table 2). Bottom-right: on-site feeder mass-flow data (Xiao et al. 2024). This is the part of my profile that is already runnable at Tata Steel NL.")

# =====================================================================
# SLIDE 12 — closing: plan → project
# =====================================================================
s = new_slide()
header(s, "CONCLUSION  ·  THE PLAN, MAPPED TO THE PROJECT",
       "What the Plan Asks — What I Bring", 12)
rows = [
    ("1 · DEM theory & conveyors",
     "Understand contact force laws & bulk tracking across moving boundaries",
     "Command of non-spherical contact, chevron-belt kinematics & vibratory feeding — each backed by calibrated, validated papers"),
    ("2 · SOTA & knowledge gaps",
     "Establish the frontier; highlight exactly what is unsolved",
     "Three concrete gaps: industrial co-segregation, chute calibration, heterogeneity/chemistry — with the method to close each"),
    ("3 · Methodology & novelty",
     "Defend the 4-year plan; state the novelty",
     "Validated upscaling (≤ 1.6×, ≤ 10%) + AOR experiments → a multi-scale, multi-property digital twin of multi-material recipes"),
    ("4 · Personal skills",
     "Show the tools & validation workflows",
     "EDEM / Rocky / LIGGGHTS + drop, tilt-box & mass-flow validation — ready to execute at Tata Steel NL"),
]
cw = 6.115
for i, (t, ask, bring) in enumerate(rows):
    x = 0.45 + (i % 2) * (cw + 0.2)
    y = 1.35 + (i // 2) * 2.05
    card(s, x, y, cw, 1.88, fill=LIGHT2, line_color=BLUE, line_w=1.0)
    tb, tf = add_box(s, x + 0.18, y + 0.12, cw - 0.36, 1.66)
    para(tf, t, size=11.5, bold=True, color=NAVY, first=True, space_after=4)
    p = tf.add_paragraph(); p.line_spacing = 1.03; p.space_after = Pt(4)
    r1 = p.add_run(); r1.text = "Plan:  "; _set_run(r1, size=9.5, bold=True, color=GRAY)
    r2 = p.add_run(); r2.text = ask; _set_run(r2, size=9.5, color=GRAY)
    p = tf.add_paragraph(); p.line_spacing = 1.03
    r1 = p.add_run(); r1.text = "Bring:  "; _set_run(r1, size=9.5, bold=True, color=BLUE)
    r2 = p.add_run(); r2.text = bring; _set_run(r2, size=9.5, color=DARK)
band = card(s, 0.45, 5.75, 12.43, 1.1, fill=NAVY, line_color=None)
tb, tf = add_box(s, 0.75, 5.92, 11.85, 0.8)
para(tf, "Backed by Tata Steel Netherlands", size=13, bold=True, color=WHITE, first=True, space_after=3)
para(tf, "Industrially calibrated simulation — non-spherical, multi-material, plant-geometry — is what separates this project from idealised spherical-particle work (plan, opening line).",
     size=10.5, color=RGBColor(0xD9, 0xEE, 0xFB), line=1.05)
notes(s, "Closing: map each plan topic to a concrete, evidenced answer. Then land the opening line of the plan: Tata Steel backing means the bar is industrial calibration, not idealised particles — and every slide in this deck has shown that bar being met, paper by paper.")

# =====================================================================
# SLIDE 13 — figure & plan references
# =====================================================================
s = new_slide()
header(s, "SUPPORTING LITERATURE", "Figures (repository papers) & Plan References", 13)
refs_l = [
    "REPOSITORY PAPERS  (all figures)",
    "[1]  Lu G., Third J.R., Müller C.R. (2015). Discrete element models for non-spherical particle systems: from theoretical developments to applications. Chemical Engineering Science 127: 425–465. — Figs 3, 14, 32; super-quadric family",
    "[2]  Rossow J., Coetzee C.J. (2021). Discrete element modelling of a chevron patterned conveyor belt and a transfer chute. Powder Technology 391: 77–96. — Figs 1, 2, 3, 8, 10, 13; Tables 2, 9",
    "[3]  Schefler O.C., Coetzee C.J. (2023). Discrete element modelling of a bulk cohesive material discharging from a conveyor belt onto an impact plate. Minerals 13(12): 1501. — discharge experiment",
    "[4]  You Y., Liu M., Ma H., et al. (2018). Investigation of the vibration sorting of non-spherical particles based on DEM simulation. Powder Technology. doi:10.1016/j.powtec.2017.11.002 — device, models, sorting patterns",
    "[5]  Xiao X., Zhong X., Ma M., Wu X. (2024). A visual based algorithm for measuring the speed of scrap metal vibration feeding. ACM CSAE 2024. doi:10.1145/3704814.3704817 — feeder tracking, speed curve",
    "[6]  Chen Y., Ryan S., Silaen A.K., Zhou C.Q. (2022). Simulation of scrap melting process in an AC electric arc furnace. Metall. Mater. Trans. B 53: 3256–3272. — 3-D model, dual-cell, pit validation, buckets",
]
refs_r = [
    "[7]  Zhong W., Yu A., Liu X., Tong Z., Zhang H. (2016). DEM/CFD-DEM modelling of non-spherical particulate systems: theoretical developments and applications. Powder Technology 300: 109–127. — Figs 1, 45",
    "[8]  Garg R., Galvin J., Li T., Pannala S. (2012). Documentation of open-source MFIX-DEM software for gas–solids flows. NETL/ORNL. — architecture & contact model",
    "PLAN REFERENCES  (planning.md, external to the repository)",
    "[9]  Ahmed H., Pang Y., Adema A., et al. (2026). Industrial-scale DEM modelling of segregation in the blast furnace charging system — Tata Steel IJmuiden (plan ref [1], ScienceDirect S0032591026000045).",
    "[10] Experimental and DEM analysis of galvanized steel scrap particles along and after an inclined chute (plan ref [2], ResearchGate).",
    "[11] Modeling scrap composition in electric arc and basic oxygen furnace processes (plan ref [3], arXiv).",
    "[12] Optimization of DEM model to obtain stable and reliable numerical results of mechanical response of granular materials (plan ref [10], MDPI Minerals 2024, 14(8): 758).",
]
for x0, refs in ((0.45, refs_l), (6.75, refs_r)):
    tb, tf = add_box(s, x0, 1.32, 6.1, 5.6)
    first = True
    for ref in refs:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        is_head = ref.startswith(("REPOSITORY", "PLAN"))
        p.space_after = Pt(10 if is_head else 8); p.line_spacing = 1.02
        r = p.add_run(); r.text = ref
        _set_run(r, size=9 if is_head else 8.5, bold=is_head, color=BLUE if is_head else DARK)
notes(s, "Figures are extracted from the PDFs in 'papers/particles-based models' (caption sources on each slide). The plan's external references [9]–[12] are the Topic 2 gap studies and the Topic 3 calibration paper — read and cited as in planning.md. Permission note: figures are reproduced for the PhD interview presentation of the repository owner, who holds these papers; keep this use non-public.")

# remove the two unused original slides (old empty 'Summary' + old image slide)
def delete_slide(prs, slide):
    from pptx.oxml.ns import qn
    rId = None
    for rel in prs.part.rels.values():
        if rel.target_part is slide.part:
            rId = rel.rId
            break
    if rId is None:
        return
    for sldId in list(prs.slides._sldIdLst):
        if sldId.get(qn("r:id")) == rId:
            prs.slides._sldIdLst.remove(sldId)

for idx in (2, 1):  # 0-based: original empty 'Summary' + old image slide
    delete_slide(prs, prs.slides[idx])

prs.save(OUT)
print("Saved:", OUT, "with", len(prs.slides._sldIdLst), "slides")
