#!/usr/bin/env python3
"""Build the complete PhD-interview deck from the started 'Delft Phd scrap handling.pptx'.

Structure follows slides.md / planning.md; technical details are drawn from the
papers in 'papers/particles-based models/' (Lu et al. 2015; Zhong et al. 2016;
Rossow & Coetzee 2021; Schefler & Coetzee 2023; You et al. 2018; Xiao et al. 2024;
Chen et al. 2022; Li/Provatas/Irons 2008; Kryszak et al. 2020; Garg et al. 2012;
Kozicki & Tejchman 2005; Ahmed et al. 2026 (Tata Steel IJmuiden BF charging)).
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
import copy

SRC = "presentation/Delft Phd scrap handling.pptx"
OUT = "presentation/Delft Phd scrap handling - completed.pptx"

# ---------------- palette ----------------
BLUE      = RGBColor(0x00, 0xA4, 0xE4)   # Delft blue (accent)
NAVY      = RGBColor(0x14, 0x3B, 0x5C)   # dark navy (titles)
DARK      = RGBColor(0x2B, 0x2B, 0x2B)   # body text
GRAY      = RGBColor(0x6B, 0x6B, 0x6B)   # captions
LIGHT     = RGBColor(0xEA, 0xF4, 0xFB)   # light blue fill
LIGHT2    = RGBColor(0xF5, 0xF9, 0xFC)   # lighter fill
AMBER     = RGBColor(0xE8, 0xA3, 0x3D)   # highlight accent
WHITE     = RGBColor(0xFF, 0xFF, 0xFF)
LINEGRAY  = RGBColor(0xD9, 0xD9, 0xD9)

FONT = "Calibri"

prs = Presentation(SRC)
BLANK = None
for layout in prs.slide_layouts:
    if layout.name == "Blank":
        BLANK = layout
        break

SW, SH = 13.333, 7.5  # inches

# ---------------- helpers ----------------

def _set_run(r, size=12, bold=False, color=DARK, italic=False, font=FONT):
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = color
    r.font.name = font


def add_box(slide, x, y, w, h):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    return tb, tf


def para(tf, text, size=12, bold=False, color=DARK, align=PP_ALIGN.LEFT,
         space_after=4, space_before=0, line=1.0, first=False, italic=False):
    p = tf.paragraphs[0] if first and not tf.paragraphs[0].runs else tf.add_paragraph()
    p.alignment = align
    p.space_after = Pt(space_after)
    p.space_before = Pt(space_before)
    p.line_spacing = line
    r = p.add_run()
    r.text = text
    _set_run(r, size=size, bold=bold, color=color, italic=italic)
    return p


def bullets(tf, items, size=11.5, color=DARK, space_after=6, line=1.06,
            bullet_color=BLUE, first=True):
    """items: list of (level, text) or (level, text, bold)"""
    started = first
    for it in items:
        lvl, text = it[0], it[1]
        bold = it[2] if len(it) > 2 else False
        p = tf.paragraphs[0] if started and not tf.paragraphs[0].runs else tf.add_paragraph()
        started = False
        p.space_after = Pt(space_after)
        p.line_spacing = line
        indent = 0.0 if lvl == 0 else 0.28
        pPr = p._p.get_or_add_pPr()
        pPr.set("marL", str(int(Inches(indent))))
        mark = "•  " if lvl == 0 else "–  "
        r1 = p.add_run()
        r1.text = mark
        _set_run(r1, size=size, bold=True, color=bullet_color)
        r2 = p.add_run()
        r2.text = text
        _set_run(r2, size=size, bold=bold, color=color)


def header(slide, kicker, title, idx=None):
    tb, tf = add_box(slide, 0.45, 0.26, 12.4, 0.85)
    para(tf, kicker, size=10.5, bold=True, color=BLUE, space_after=2, first=True)
    para(tf, title, size=25, bold=True, color=NAVY, space_after=0, line=0.98)
    # accent rule
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.47), Inches(1.06),
                                 Inches(1.35), Inches(0.045))
    bar.fill.solid(); bar.fill.fore_color.rgb = BLUE
    bar.line.fill.background()
    bar.shadow.inherit = False
    if idx is not None:
        footer(slide, idx)


def footer(slide, idx):
    ln = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.45), Inches(7.12),
                                Inches(12.43), Inches(0.012))
    ln.fill.solid(); ln.fill.fore_color.rgb = LINEGRAY
    ln.line.fill.background(); ln.shadow.inherit = False
    tb, tf = add_box(slide, 0.45, 7.17, 9.5, 0.3)
    para(tf, "Particle-Based Modelling of Scrap Handling for Green Steel Production  •  TU Delft × Tata Steel Netherlands",
         size=8, color=GRAY, first=True)
    tb2, tf2 = add_box(slide, 12.0, 7.17, 0.88, 0.3)
    para(tf2, str(idx), size=9, bold=True, color=GRAY, align=PP_ALIGN.RIGHT, first=True)


def card(slide, x, y, w, h, fill=LIGHT, line_color=BLUE, line_w=1.0, round_=True):
    shp = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE if round_ else MSO_SHAPE.RECTANGLE,
        Inches(x), Inches(y), Inches(w), Inches(h))
    shp.fill.solid(); shp.fill.fore_color.rgb = fill
    if line_color is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line_color
        shp.line.width = Pt(line_w)
    shp.shadow.inherit = False
    if round_:
        try:
            shp.adjustments[0] = 0.045
        except Exception:
            pass
    return shp


def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


def new_slide():
    return prs.slides.add_slide(BLANK)


def cell_text(cell, text, size=9, bold=False, color=DARK, align=PP_ALIGN.LEFT,
              anchor=MSO_ANCHOR.MIDDLE, line=1.0):
    tf = cell.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.07)
    tf.margin_right = Inches(0.07)
    tf.margin_top = Inches(0.03)
    tf.margin_bottom = Inches(0.03)
    cell.vertical_anchor = anchor
    p = tf.paragraphs[0]
    p.alignment = align
    p.line_spacing = line
    r = p.add_run()
    r.text = text
    _set_run(r, size=size, bold=bold, color=color)


def strip_border(shape):
    shape.line.fill.background()
    shape.shadow.inherit = False


# =====================================================================
# SLIDE 2 — Agenda (existing "Summary" slide)
# =====================================================================
s2 = prs.slides[1]
# retit
for sh in s2.shapes:
    if sh.has_text_frame and sh.text_frame.text.strip() == "Summary":
        tf = sh.text_frame
        for p in tf.paragraphs:
            for r in p.runs:
                r.text = ""
        p = tf.paragraphs[0]
        r = p.add_run(); r.text = "Agenda"
        _set_run(r, size=30, bold=True, color=NAVY)
        break

agenda = [
    ("1", "Theory of particle-based models (DEM) & conveyor systems",
     "Non-spherical shape representation • contact mechanics • belt / chute / vibratory-feeder kinematics"),
    ("2", "State of the art & knowledge gaps in scrap / EAF modelling",
     "Where the literature stands today — and what it has not solved"),
    ("3", "Methodology, novelty & anticipated challenges",
     "4-year research plan • coarse-graining calibration strategy • project novelty"),
    ("4", "Skills, competencies & personal reflection",
     "Technical toolkit • data integration • experimental validation • industrial collaboration"),
]
y = 1.55
for num, title, sub in agenda:
    c = s2.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.55), Inches(y), Inches(0.62), Inches(0.62))
    c.fill.solid(); c.fill.fore_color.rgb = BLUE
    strip_border(c)
    ctf = c.text_frame
    ctf.word_wrap = False
    cp = ctf.paragraphs[0]; cp.alignment = PP_ALIGN.CENTER
    cr = cp.add_run(); cr.text = num
    _set_run(cr, size=20, bold=True, color=WHITE)
    ctf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tb, tf = add_box(s2, 1.5, y - 0.04, 11.2, 0.95)
    para(tf, title, size=17, bold=True, color=NAVY, first=True, space_after=2)
    para(tf, sub, size=11.5, color=GRAY)
    y += 1.28
footer(s2, 2)
notes(s2, "[1:00 – 1:45]\n\"Our agenda today directly addresses the key requirements: First, the core mechanics of DEM applied to conveyor systems; second, the state of the art and literature gaps; third, my explicit research methodology and anticipated challenges; and finally, a personal reflection on my competencies.\"\n\nSlide notes: the four agenda items map 1:1 to the four topics requested for the interview (see planning.md, Topics 1-4).")

# =====================================================================
# SLIDE 3 — DEM fundamentals & shape representation (existing image slide)
# =====================================================================
s3 = prs.slides[2]
# title block (no footer on this image-heavy slide)
tb, tf = add_box(s3, 0.45, 0.26, 12.4, 0.85)
para(tf, "TOPIC 1 — PARTICLE-BASED MODELLING (DEM)", size=10.5, bold=True, color=BLUE, space_after=2, first=True)
para(tf, "DEM Fundamentals & Particle Shape Representation", size=25, bold=True, color=NAVY, space_after=0, line=0.98)
bar = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.47), Inches(1.06), Inches(1.35), Inches(0.045))
bar.fill.solid(); bar.fill.fore_color.rgb = BLUE
bar.line.fill.background(); bar.shadow.inherit = False
# locate the three pictures and reposition
pics = {}
for sh in s3.shapes:
    if sh.shape_type == 13:  # picture
        pics[sh.name] = sh
# image3.png = Fig.6 superquadric grid (big, top-left originally)
# image2.png = Eq.(16) (wide, bottom-left originally)
# image5.png = Fig.4b contact approximation (right-middle originally)
# map by original size: Fig6 7772400x5278719 ; Eq 5829300x723900 ; contact 7226300x3098800
def find_pic(w_emu, h_emu):
    for name, sh in pics.items():
        if sh.width == w_emu and sh.height == h_emu:
            return sh
    return None

fig6  = find_pic(7772400, 5278719)
eq16  = find_pic(5829300, 723900)
fig4b = find_pic(7226300, 3098800)

def place(sh, x, y, w):
    if sh is None:
        return None
    sh.left = Inches(x); sh.top = Inches(y); sh.width = Inches(w)
    sh.height = int(w * sh.height / sh.width) if False else None
    return sh

# Fig 6 (ratio h/w = 5278719/7772400 = 0.6792)
if fig6 is not None:
    w = 6.32
    fig6.left, fig6.top = Inches(6.55), Inches(1.12)
    fig6.width = Inches(w)
    fig6.height = Inches(w * 0.67918)
# Eq 16 (ratio h/w = 723900/5829300 = 0.12419)
if eq16 is not None:
    w = 5.05
    eq16.left, eq16.top = Inches(0.50), Inches(5.74)
    eq16.width = Inches(w)
    eq16.height = Inches(w * 0.12419)
# Fig 4b (ratio h/w = 3098800/7226300 = 0.42882)
if fig4b is not None:
    w = 3.95
    fig4b.left, fig4b.top = Inches(6.55), Inches(5.72)
    fig4b.width = Inches(w)
    fig4b.height = Inches(w * 0.42882)

tb, tf = add_box(s3, 0.45, 1.12, 5.95, 4.5)
bullets(tf, [
    (0, "DEM tracks every scrap fragment individually via Newton's laws (Lagrangian); each contact carries a normal force Fn and a tangential force Ft (spring–damper contact model)", 0),
    (0, "Scrap is never round — shape controls friction, interlocking, bridging and segregation, so spheres alone roll too easily", 0),
    (0, "Non-spherical shape representation (Lu et al. 2015; Zhong et al. 2016):", 1),
    (1, "Multi-sphere clusters — robust; reuses sphere–sphere contacts; best proxy for shredded scrap", 0),
    (1, "Polyhedra — angular rock/scrap; common-plane contact; many contact cases to classify", 0),
    (1, "Super-quadrics — smooth, regular shapes; ε₁, ε₂ vary roundness → blockiness continuously", 0),
    (1, "Voxel / digitised — arbitrary 3D-scanned shapes; grid-resolution limited", 0),
    (1, "Bonded particles — add fracture & deformation", 0),
    (0, "Key trade-off: contact detection alone can consume >80% of the computation time", 1),
], size=11.5, space_after=7)

tb, tf = add_box(s3, 0.50, 6.42, 5.95, 0.6)
para(tf, "Eq. (16) — 3D super-quadric implicit function; ε₁ = ε₂ = 1 gives an ellipsoid (Lu et al., 2015)",
     size=8, color=GRAY, first=True)
tb, tf = add_box(s3, 6.55, 5.45, 6.3, 0.26)
para(tf, "Fig. 6 — 3D super-quadric family: ε₁ (left→right), ε₂ (top→bottom) (Lu et al., 2015)",
     size=8, color=GRAY, first=True)
tb, tf = add_box(s3, 10.62, 5.72, 2.28, 1.6)
para(tf, "Fig. 4b — approximation of the actual contact region Ω between two super-quadrics (Lu et al., 2015)",
     size=7.5, color=GRAY, first=True, line=1.0)
notes(s3, "[1:45 – 3:15]\n\"Let's begin with the fundamental physics. The Discrete Element Method operates by tracking individual particles via Newton's laws of motion. In industrial scrap yards, particles are highly non-spherical. To capture realistic friction and interlocking behaviour, I will employ Multi-Sphere models or Polyhedral elements. While spheres are computationally cheap, they roll too easily. We must account for the high aspect ratios and sharp edges typical of steel scrap to accurately simulate structural bridging and interlocking.\"\n\nSlide notes: right column shows (top) the 3D super-quadric shape family from Lu et al. (2015) Fig. 6 — blockiness parameters ε1/ε2 sweep from rounded to blocky; (bottom) their implicit equation (16) and Fig. 4b contact-region approximation. Emphasise: for scrap we will mainly use multi-sphere clusters built from 3D scans (robust + fast contact detection), with super-quadrics/polyhedra where smooth/angular fidelity matters. Contact detection can take >80% of CPU time, so the choice of representation is a compute decision, not just a physics decision.")

# =====================================================================
# SLIDE 4 — Conveyor belts & vibratory feeders
# =====================================================================
s4 = new_slide()
header(s4, "TOPIC 1 — PARTICLE-BASED MODELLING (DEM) & CONVEYOR SYSTEMS",
       "Conveyor Belts & Vibratory Feeders: Mechanics at the Boundary", 4)

# schematic
sx, sy, sw_, sh_ = 0.45, 1.42, 2.75, 0.98
stages = [
    ("Belt conveyor", "chevron patterned belt • wall friction • belt velocity"),
    ("Transfer chute", "impact plate • hood • rock box • build-up & blockage"),
    ("Vibratory feeder", "inertial vibration: frequency, amplitude, inclination"),
    ("EAF infeed", "continuous charging into the furnace"),
]
gap = 0.5
for i, (t, sub) in enumerate(stages):
    x = sx + i * (sw_ + gap)
    fill = LIGHT if i < 3 else RGBColor(0xD9, 0xEE, 0xFB)
    box = card(s4, x, sy, sw_, sh_, fill=fill, line_color=BLUE, line_w=1.2)
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.09); tf.margin_right = Inches(0.09)
    tf.margin_top = Inches(0.06); tf.margin_bottom = Inches(0.06)
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = t
    _set_run(r, size=12.5, bold=True, color=NAVY)
    p2 = tf.add_paragraph(); p2.alignment = PP_ALIGN.CENTER
    p2.line_spacing = 0.95
    r2 = p2.add_run(); r2.text = sub
    _set_run(r2, size=8.5, color=GRAY)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    if i < 3:
        ar = s4.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW,
                                 Inches(x + sw_ + 0.07), Inches(sy + sh_/2 - 0.11),
                                 Inches(gap - 0.14), Inches(0.22))
        ar.fill.solid(); ar.fill.fore_color.rgb = BLUE
        strip_border(ar)

# four evidence panels (2x2)
panels = [
    ("Rossow & Coetzee (2021) — chevron belt + transfer chute", "Powder Technol. 391:77–96",
     ["First DEM study of a chevron-patterned belt with impact plate, hood and rock box; 3D-laser-scanned particles modelled as 3/5/10-sphere multi-sphere “clumps”",
      "Validated against high-speed footage: mass flow ≤5.4% error, impact velocity <6.1%, impact-wall force <17%",
      "Maximum particle up-scaling factor 1.6 (≤10% error) — DEM beat the analytical model in accuracy"]),
    ("Schefler & Coetzee (2023) — cohesive belt discharge", "Minerals 13(12):1501",
     ["Wet-and-sticky material discharging from belt onto an inclined impact plate: build-up profile, peak impact force and residual weight reproduced with <15% error using upscaled particles",
      "Max acceptable scale factor is a geometric property of the bulk measure of interest — not of the physical particle size",
      "Higher cohesion → thicker discharge stream & taller build-up → higher allowable scale factor"]),
    ("You et al. (2018) — vibration sorting of non-spherical particles", "Powder Technol. (2018)",
     ["DEM of an inclined vibrating plate: non-spherical particles as super-ellipsoids, mixed 1:1 with spheres",
      "Vibration frequency & amplitude control the velocity distribution and discharge sequence of the mixture",
      "Effective separation when (2πf)²A ≈ 1.5g — a practical design rule for vibratory feeders"]),
    ("Xiao et al. (2024) — measuring real scrap feeding", "CSAE 2024 (ACM)",
     ["Vision-based speed measurement of scrap on an inertial vibratory conveyor (SuperPoint feature-point extraction & matching)",
      "Works despite heterogeneous scrap types, sizes and stacking — no object tracking needed",
      "On-site application: measured speed curve matches the horizontal-vibrator frequency curve — an industrial validation pathway for our models"]),
]
pw, ph = 6.12, 1.86
for i, (t, src, items) in enumerate(panels):
    x = 0.45 + (i % 2) * (pw + 0.19)
    y = 2.72 + (i // 2) * (ph + 0.14)
    box = card(s4, x, y, pw, ph, fill=LIGHT2, line_color=BLUE, line_w=1.0)
    tb, tf = add_box(s4, x + 0.14, y + 0.09, pw - 0.28, ph - 0.18)
    para(tf, t, size=10.5, bold=True, color=NAVY, first=True, space_after=1)
    para(tf, src, size=8.5, italic=True, color=GRAY, space_after=3)
    for it in items:
        p = tf.add_paragraph()
        p.space_after = Pt(2); p.line_spacing = 0.98
        r1 = p.add_run(); r1.text = "•  "
        _set_run(r1, size=9, bold=True, color=BLUE)
        r2 = p.add_run(); r2.text = it
        _set_run(r2, size=9, color=DARK)
notes(s4, "[3:15 – 4:45]\n\"When bulk scrap transfers from a conveyor belt to an EAF infeed chute, it undergoes severe dynamic stress. By solving the contact force equations at moving boundaries, our model will simulate wall friction, boundary velocity distributions, and impact energy. On vibratory feeders, the frequency and amplitude of the bed dictate particle acceleration. DEM allows us to isolate how different frequencies cause structural segregation, ensuring we can predict which particles discharge first and where the mechanical wear on the hopper liners will be most severe.\"\n\nSlide notes: cite Rossow & Coetzee (chevron belt + chute, high-speed validation, upscaling limit 1.6) and Schefler & Coetzee (cohesive discharge, <15% error) as the mature modelling base; You et al. as the vibration-segregation evidence; Xiao et al. as proof that real scrap-feeding measurement exists today (vision-based) — our models can be validated against it.")

# =====================================================================
# SLIDE 5 — State of the art
# =====================================================================
s5 = new_slide()
header(s5, "TOPIC 2 — CURRENT STATE OF THE ART & KNOWLEDGE GAPS",
       "The Frontier of Research: Where the Literature Stands", 5)

rows = [
    ("Reference", "System & method", "What it establishes", "Limitation for EAF scrap"),
    ("Lu et al. (2015) — Chem. Eng. Sci. 127 (review)", "Non-spherical DEM review: polyhedra, super-quadrics, multi-sphere, voxel, bonded",
     "Shape representation + contact detection; contact detection can cost >80% of CPU time", "No scrap-specific benchmark; generic granular systems"),
    ("Zhong et al. (2016) — Powder Technol. 300 (review)", "DEM / CFD-DEM review: AVM vs. immersed-family coupling",
     "No single best method; hybrid averaged + resolved strategies", "Generic particulate flows, not scrap handling"),
    ("Ahmed et al. (2026) — Powder Technol. (Tata Steel IJmuiden)", "Industrial BF charging: skip car → top hopper, actual plant geometry",
     "Plant-faithful DEM; ferrous-burden segregation lowers throat permeability", "Uniform BF burden (ore/sinter) — not heterogeneous EAF scrap"),
    ("Rossow & Coetzee (2021) — Powder Technol. 391", "Chevron belt + transfer chute, multi-sphere particles, high-speed validation",
     "Quantified DEM accuracy & upscaling limits (≤1.6×)", "Lab-scale corn grains, non-cohesive"),
    ("Schefler & Coetzee (2023) — Minerals 13:1501", "Cohesive material: belt → inclined impact plate",
     "Upscaled cohesive discharge: force & residual mass <15% error", "Lab-scale sand; single material"),
    ("You et al. (2018) — Powder Technol.", "Inclined vibrating plate, super-ellipsoids + spheres",
     "Frequency/amplitude → sorting & segregation; (2πf)²A ≈ 1.5g", "Lab-scale idealised shapes"),
    ("Chen et al. (2022) — Metall. Mater. Trans. B", "3D CFD of AC-EAF scrap melting, dual-cell + stack, NLMK 150-t EAF",
     "Melting, arc & burner physics well resolved and industrially validated", "Scrap enters as a lumped input — infeed dynamics not resolved"),
    ("Li, Provatas & Irons (2008) — AISTech", "Phase-field modelling of late melting in the EAF heel",
     "“Steel iceberg” formation dominates late melting; size, preheat & convection effects", "Post-charge physics — scrap assumed already in the furnace"),
]
tbl_shape = s5.shapes.add_table(len(rows), 4, Inches(0.45), Inches(1.22), Inches(12.43), Inches(5.55))
tbl = tbl_shape.table
tbl.first_row = True
tbl.horz_banding = True
widths = [3.30, 3.30, 3.10, 2.73]
for i, w in enumerate(widths):
    tbl.columns[i].width = Inches(w)
tbl.rows[0].height = Inches(0.32)
for ri in range(1, len(rows)):
    tbl.rows[ri].height = Inches(0.60)
for ci, val in enumerate(rows[0]):
    c = tbl.cell(0, ci)
    c.fill.solid(); c.fill.fore_color.rgb = NAVY
    cell_text(c, val, size=9.5, bold=True, color=WHITE)
for ri in range(1, len(rows)):
    for ci in range(4):
        c = tbl.cell(ri, ci)
        c.fill.solid()
        c.fill.fore_color.rgb = WHITE if ri % 2 == 1 else LIGHT2
        bold = (ci == 0)
        col = NAVY if ci == 0 else DARK
        cell_text(c, rows[ri][ci], size=8.5, bold=bold, color=col, line=0.95)
tb, tf = add_box(s5, 0.45, 6.72, 12.43, 0.35)
para(tf, "Pattern: DEM for conveyors/chutes is mature and validated — EAF CFD is mature and validated — the mechanical charging stage in between is the weak link.",
     size=10, bold=True, color=NAVY, first=True)
notes(s5, "[4:45 – 6:15]\n\"Reviewing the current state of the art shows a significant disconnect. Excellent DEM models exist for blast furnace charging — such as research calibrated at Tata Steel IJmuiden — but these focus on uniform materials like iron ore pellets. Conversely, current EAF literature focuses heavily on the thermodynamic and CFD chemical melting inside the furnace, completely neglecting the mechanical bulk flow of raw scrap before it enters the liquid bath. There is a profound lack of physical particle tracking models for heterogeneous scrap recipes.\"\n\nSlide notes: table walks top→bottom: reviews (Lu 2015, Zhong 2016) → industrial BF charging at Tata Steel IJmuiden (Ahmed et al. 2026) → conveyor/chute DEM validation studies (Rossow 2021, Schefler 2023, You 2018) → EAF melting models (Chen 2022, Li 2008). Close on the bottom strip: both halves are mature, the interface is not.")

# =====================================================================
# SLIDE 6 — Knowledge gaps
# =====================================================================
s6 = new_slide()
header(s6, "TOPIC 2 — CURRENT STATE OF THE ART & KNOWLEDGE GAPS",
       "The Key Industry Knowledge Gaps", 6)

# two big gap cards
gc = [
    ("GAP 1", "Material heterogeneity", 
     "Heavy melting scrap (bundles up to metres, dense, low porosity) vs. shredded & baled scrap (cm-scale, light, porous, high surface area). Multi-material recipes combine very different shape, size, bulk density and chemistry — no particle-level model yet resolves the whole stream."),
    ("GAP 2", "Real-time co-segregation in continuous feeding",
     "How does heterogeneity segregate during vibratory feeding and chute transfer? If fine scrap blocks the chute or heavy bundles drop unpredictably, the charge layers unevenly → thermal imbalances, energy spikes and late melting (“steel icebergs”) in the EAF."),
]
for i, (tag, t, body) in enumerate(gc):
    x = 0.45 + i * 6.31
    box = card(s6, x, 1.24, 6.12, 2.28, fill=LIGHT, line_color=BLUE, line_w=1.4)
    tb, tf = add_box(s6, x + 0.18, 1.38, 5.78, 2.0)
    p = tf.paragraphs[0]
    r = p.add_run(); r.text = tag + "  "
    _set_run(r, size=11, bold=True, color=AMBER)
    r2 = p.add_run(); r2.text = t
    _set_run(r2, size=14.5, bold=True, color=NAVY)
    p.space_after = Pt(5)
    p2 = tf.add_paragraph(); p2.line_spacing = 1.04
    r3 = p2.add_run(); r3.text = body
    _set_run(r3, size=10.5, color=DARK)

# three secondary gap chips
subs = [
    ("Handling ↔ furnace coupling is missing", "Conveyor/chute DEM is mature; EAF CFD is mature; the interface between them is not yet built."),
    ("Industrial validation of charging dynamics is sparse", "Scrap flow in a running EAF is hard to observe directly; most DEM studies are validated on related lab materials."),
    ("Multiphysics at the charge surface", "Infeed scrap moves from mechanical handling to heating, oxidation, re-soldering and collapse — current models treat these separately."),
]
cw, ch = 4.02, 2.02
for i, (t, b) in enumerate(subs):
    x = 0.45 + i * (cw + 0.185)
    box = card(s6, x, 3.78, cw, ch, fill=LIGHT2, line_color=LINEGRAY, line_w=1.0)
    tb, tf = add_box(s6, x + 0.14, 3.92, cw - 0.28, ch - 0.26)
    para(tf, t, size=10.5, bold=True, color=NAVY, first=True, space_after=4, line=0.98)
    p = tf.add_paragraph(); p.line_spacing = 1.0
    r = p.add_run(); r.text = b
    _set_run(r, size=9.5, color=GRAY)

band = card(s6, 0.45, 6.05, 12.43, 0.82, fill=NAVY, line_color=None)
tf = band.text_frame
tf.word_wrap = True
tf.margin_left = Inches(0.2); tf.margin_right = Inches(0.2)
tf.vertical_anchor = MSO_ANCHOR.MIDDLE
p = tf.paragraphs[0]; p.line_spacing = 1.0
r = p.add_run(); r.text = "Bottom line from the literature:  "
_set_run(r, size=11.5, bold=True, color=AMBER)
r2 = p.add_run()
r2.text = "treat scrap infeed as a coupled granular-transport problem — DEM particle mechanics for conveyor / chute / charging, handed off to a furnace model that resolves packing-dependent heat transfer and melting."
_set_run(r2, size=11.5, color=WHITE)
notes(s6, "[6:15 – 7:30]\n\"This brings us to the two key knowledge gaps this PhD will bridge. First, how do we model a bulk material stream that is structurally heterogeneous, ranging from lightweight shredded metal to massive, dense heavy melting scrap bundles? Second, how does this heterogeneity trigger material segregation during continuous charging? If fine scrap blocks the chute or heavy bundles drop unpredictably, it causes thermal imbalances and massive energy spikes in the EAF.\"\n\nSlide notes: the three secondary gaps come from the literature review (see LeapSpace summary in the repo): coupling of handling & furnace physics; realistic scrap shape & packing; charge dynamics during delivery; validation with industrial scrap; multiphysics at the charge surface. Tie Gap 2 to Li et al. 2008: late/iceberg melting is exactly what happens when the charge arrives wrong.")

# =====================================================================
# SLIDE 7 — 4-year research plan
# =====================================================================
s7 = new_slide()
header(s7, "TOPIC 3 — METHODOLOGY, NOVELTY & ANTICIPATED CHALLENGES",
       "Research Plan: The 4-Year Roadmap", 7)

years = [
    ("Y1", "Model development",
     ["Non-spherical DEM of scrap: multi-sphere & super-quadric proxies from 3D scans",
      "Baseline shape characterisation: size, shape, bulk density, porosity",
      "Lab calibration: angle of repose, drop & draw-down tests"]),
    ("Y2", "Industrial calibration",
     ["Tata Steel NL plant data: feeders, chutes, recipes",
      "Build the virtual material library (bale / shredded / HMS)",
      "High-speed video & load-cell validation; upscaling limits at industrial scale"]),
    ("Y3", "Optimisation scenarios",
     ["Multi-material recipe simulations in real plant geometry",
      "Segregation & discharge-sequence optimisation (which scrap goes first)",
      "Coupling with melting model: charge layering, HBI + scrap interaction"]),
    ("Y4", "Plant implementation",
     ["Digital twin of the EAF infeed chain",
      "Actionable operating rules for plant engineers",
      "Wear & energy-reduction recommendations; dissemination & PhD defence"]),
]
cw, ch = 2.95, 3.95
for i, (tag, t, items) in enumerate(years):
    x = 0.45 + i * (cw + 0.12)
    chev = s7.shapes.add_shape(MSO_SHAPE.CHEVRON, Inches(x), Inches(1.30), Inches(cw + 0.27), Inches(0.85))
    chev.fill.solid(); chev.fill.fore_color.rgb = BLUE if i % 2 == 0 else NAVY
    strip_border(chev)
    try:
        chev.adjustments[0] = 0.55
    except Exception:
        pass
    ctf = chev.text_frame
    ctf.word_wrap = True
    ctf.margin_left = Inches(0.18)
    p = ctf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = f"{tag} — {t}"
    _set_run(r, size=12, bold=True, color=WHITE)
    ctf.vertical_anchor = MSO_ANCHOR.MIDDLE

    box = card(s7, x, 2.35, cw, ch, fill=LIGHT2, line_color=BLUE, line_w=1.0)
    tb, tf = add_box(s7, x + 0.14, 2.52, cw - 0.28, ch - 0.32)
    first = True
    for it in items:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.space_after = Pt(8); p.line_spacing = 1.02
        r1 = p.add_run(); r1.text = "•  "
        _set_run(r1, size=10, bold=True, color=BLUE)
        r2 = p.add_run(); r2.text = it
        _set_run(r2, size=10, color=DARK)

band = card(s7, 0.45, 6.55, 12.43, 0.48, fill=LIGHT, line_color=None)
tf = band.text_frame
tf.word_wrap = True
tf.vertical_anchor = MSO_ANCHOR.MIDDLE
tf.margin_left = Inches(0.2)
p = tf.paragraphs[0]
r = p.add_run(); r.text = "Guiding principle:  "
_set_run(r, size=11, bold=True, color=NAVY)
r2 = p.add_run()
r2.text = "every year ends in a validated artefact the plant can use — not just a simulation."
_set_run(r2, size=11, color=DARK)
notes(s7, "[7:30 – 9:00]\n\"To address these gaps, my proposed 4-year research plan is structured systematically. Year 1 focuses on mathematical code development and baseline shape characterisation. Year 2 will integrate industrial data sets from Tata Steel Netherlands to calibrate our virtual materials. Year 3 will focus on simulating various charging recipes and sequence optimisation. Year 4 will translate these computational models into practical, actionable rules for industrial plant engineers.\"\n\nSlide notes: Y1 = Lu/Zhong shape representations + lab calibration suite; Y2 = Tata Steel NL data + validation (Rossow-style high-speed footage, Xiao-style vision measurement); Y3 = recipe optimisation incl. segregation; Y4 = digital twin + recommendations. Emphasise the artefact-per-year discipline.")

# =====================================================================
# SLIDE 8 — Calibration strategy & coarse-graining
# =====================================================================
s8 = new_slide()
header(s8, "TOPIC 3 — METHODOLOGY, NOVELTY & ANTICIPATED CHALLENGES",
       "Calibration Strategy & the Coarse-Graining Dilemma", 8)

steps = [
    ("1", "Physical experiments",
     "Angle of repose • drop / bounce (COR) • draw-down • feeder mass flow • high-speed video"),
    ("2", "Parameter optimisation loop",
     "Friction, rolling resistance, restitution, cohesion; PSD & multi-sphere fitting against bulk response"),
    ("3", "Calibrated DEM engine",
     "Altair EDEM / Ansys Rocky (commercial) • LIGGGHTS / MFIX-DEM (open source)"),
    ("4", "Industrial validation",
     "Chute flow, build-up, impact force & mass balance vs. plant data (Tata Steel NL)"),
]
bw, bh = 2.86, 1.62
for i, (n, t, b) in enumerate(steps):
    x = 0.45 + i * (bw + 0.48)
    box = card(s8, x, 1.28, bw, bh, fill=LIGHT if i != 3 else RGBColor(0xD9, 0xEE, 0xFB), line_color=BLUE, line_w=1.2)
    tb, tf = add_box(s8, x + 0.13, 1.40, bw - 0.26, bh - 0.24)
    p = tf.paragraphs[0]
    r = p.add_run(); r.text = f"STEP {n}   "
    _set_run(r, size=9, bold=True, color=AMBER)
    r2 = p.add_run(); r2.text = t
    _set_run(r2, size=11.5, bold=True, color=NAVY)
    p.space_after = Pt(4)
    p2 = tf.add_paragraph(); p2.line_spacing = 0.98
    r3 = p2.add_run(); r3.text = b
    _set_run(r3, size=9, color=DARK)
    if i < 3:
        ar = s8.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW,
                                 Inches(x + bw + 0.07), Inches(1.28 + bh/2 - 0.11),
                                 Inches(0.34), Inches(0.22))
        ar.fill.solid(); ar.fill.fore_color.rgb = BLUE
        strip_border(ar)

# two evidence boxes
boxA = card(s8, 0.45, 3.22, 6.12, 3.55, fill=LIGHT2, line_color=LINEGRAY, line_w=1.0)
tb, tf = add_box(s8, 0.63, 3.38, 5.78, 3.25)
para(tf, "The coarse-graining dilemma", size=13, bold=True, color=NAVY, first=True, space_after=6)
bullets(tf, [
    (0, "Steel scrap piles span millimetres (shreds) to metres (HMS bundles) — simulating every fragment is computationally impossible", 0),
    (0, "Strategy: cluster small particles into representative numerical equivalents — volume-equivalent diameter, mass-matched multi-sphere clusters", 0),
    (0, "The virtual pile must match the real pile: angle of repose, stream thickness, build-up profile, discharge rate", 0),
    (0, "Calibrate rolling friction & shape until the virtual scrap behaves like the physical material at every scale", 0),
], size=10, space_after=8)

boxB = card(s8, 6.75, 3.22, 6.13, 3.55, fill=LIGHT, line_color=BLUE, line_w=1.2)
tb, tf = add_box(s8, 6.93, 3.38, 5.78, 3.25)
para(tf, "What the literature says about upscaling", size=13, bold=True, color=NAVY, first=True, space_after=6)
bullets(tf, [
    (0, "Rossow & Coetzee (2021): scale factor ≤ 1.6 keeps errors ≤ 10% (build-up −9.2%, discharge −5.6%); wall effects negligible when container / particle ≥ 8–10 : 1", 0),
    (0, "Schefler & Coetzee (2023): the maximum scale factor is a geometric property of the bulk measure of interest — and it increases with cohesion", 0),
    (0, "Implication: calibrate per industrial quantity of interest (build-up, force, flow rate), not per particle", 0),
    (0, "Kryszak et al. (2020) / Kozicki & Tejchman (2005): contact force spectra and grid-free methods give the validation toolbox for impact & damage", 0),
], size=10, space_after=8)
notes(s8, "[9:00 – 10:30]\n\"The greatest anticipated challenge in this project is scale and computation time. Simulating millions of unique scrap fragments down to the millimetre scale is computationally impossible. My strategy involves coarse-graining / upscaling methodologies. We will cluster smaller particles into representative numerical equivalents. We will then perform laboratory-scale calibration experiments — such as angle of repose and pouring tests — to adjust rolling friction coefficients until the virtual scrap pile matches the behaviour of the real physical material.\"\n\nSlide notes: the 4-step loop is the core methodological claim. Quote the numbers: Rossow & Coetzee max scale factor 1.6 (errors ≤10%); Schefler & Coetzee — scale limit is geometric to the measured quantity; container/particle ≥ 8–10:1 for negligible wall effects. This is the 'industrially calibrated simulation' that separates this project from idealised spherical-particle work.")

# =====================================================================
# SLIDE 9 — Novelty & deliverables
# =====================================================================
s9 = new_slide()
header(s9, "TOPIC 3 — METHODOLOGY, NOVELTY & ANTICIPATED CHALLENGES",
       "Project Novelty & Expected Deliverables", 9)

band = card(s9, 0.45, 1.22, 12.43, 0.92, fill=NAVY, line_color=None)
tf = band.text_frame; tf.word_wrap = True
tf.vertical_anchor = MSO_ANCHOR.MIDDLE
tf.margin_left = Inches(0.22); tf.margin_right = Inches(0.22)
p = tf.paragraphs[0]; p.line_spacing = 1.02
r = p.add_run(); r.text = "Core novelty:  "
_set_run(r, size=12.5, bold=True, color=AMBER)
r2 = p.add_run()
r2.text = ("a multi-scale, multi-property characterisation model that transforms raw Tata Steel data into a dynamic digital twin of EAF scrap infeed — "
           "multi-material recipes (bale, shredded, heavy melting scrap) moving through real industrial handling equipment.")
_set_run(r2, size=12.5, color=WHITE)

cards = [
    ("Digital twin of EAF infeed", 
     ["Scrap treated as a variable, uncertain feedstock — not a fixed input",
      "Multi-property particles: size, shape, bulk density, porosity, chemical heterogeneity (Cu, Cr …)",
      "Continuous chain: vibratory feeder → chute → charging, in real plant geometry"]),
    ("Optimised discharge sequences",
     ["Predict which scrap discharges first under given vibration frequency / amplitude",
      "Avoid chute blockage, bridging and stagnant zones",
      "Smooth, continuous feeding — stable layers at the charge surface"]),
    ("Reduced energy & wear",
     ["Fewer late-melting “steel icebergs” → shorter tapping delays (Li et al., 2008)",
      "Predict impact forces & liner wear on chutes and feeders",
      "Cheaper scrap recipes tested virtually before plant trials (HBI + scrap layering)"]),
]
cw, ch = 4.02, 3.62
for i, (t, items) in enumerate(cards):
    x = 0.45 + i * (cw + 0.185)
    box = card(s9, x, 2.42, cw, ch, fill=LIGHT, line_color=BLUE, line_w=1.3)
    # header strip inside card
    hd = s9.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(2.42), Inches(cw), Inches(0.52))
    hd.fill.solid(); hd.fill.fore_color.rgb = BLUE
    strip_border(hd)
    htf = hd.text_frame
    htf.vertical_anchor = MSO_ANCHOR.MIDDLE
    htf.margin_left = Inches(0.14)
    hp = htf.paragraphs[0]
    hr = hp.add_run(); hr.text = t
    _set_run(hr, size=12, bold=True, color=WHITE)
    tb, tf = add_box(s9, x + 0.16, 3.10, cw - 0.32, ch - 0.8)
    first = True
    for it in items:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.space_after = Pt(8); p.line_spacing = 1.02
        r1 = p.add_run(); r1.text = "•  "
        _set_run(r1, size=10, bold=True, color=BLUE)
        r2 = p.add_run(); r2.text = it
        _set_run(r2, size=10, color=DARK)
notes(s9, "[10:30 – 11:45]\n\"The true core novelty of this PhD project is the creation of an industrially validated Digital Twin for multi-property scrap flows. We are moving away from treating raw materials as uniform rocks. Instead, this framework will allow Tata Steel to test new, cheaper scrap recipes virtually, optimising discharge sequences to guarantee smooth, continuous feeding. The direct outcomes will be a measurable reduction in mechanical wear on handling infrastructure and optimised energy efficiency during EAF startup phases.\"\n\nSlide notes: novelty = multi-scale + multi-property + industrial (three words to remember). Deliverables map to the interview's 'industrial value' expectation: twin (asset), sequence optimisation (process gain), energy/wear (money).")

# =====================================================================
# SLIDE 10 — Technical alignment
# =====================================================================
s10 = new_slide()
header(s10, "TOPIC 4 — REFLECTION ON PERSONAL SKILLS & COMPETENCIES",
       "Technical Alignment with Project Requirements", 10)

rows = [
    ("Project requirement", "My toolkit"),
    ("Non-spherical DEM modelling — shape representation, contact detection, force & torque models",
     "Numerical programming in Python / C++; multi-sphere & super-quadric particle modelling; hands-on with Altair EDEM, Ansys Rocky, LIGGGHTS and MFIX-DEM (open source)"),
    ("Data integration — plant data into a digital twin",
     "Experience handling large data arrays; Python data pipelines (pandas / NumPy); statistical composition & uncertainty estimation for scrap recipes"),
    ("Experimental validation — physical boundary tests",
     "Angle-of-repose, drop/bounce and draw-down tests; feeder mass-flow tracking; high-speed video & PIV analysis of flow trajectories"),
    ("Industrial collaboration — from academia to the plant floor",
     "Translating dense academic results into clear, operational value for plant operations; structured project management of a 4-year industrial PhD"),
]
tbl_shape = s10.shapes.add_table(len(rows), 2, Inches(0.45), Inches(1.30), Inches(12.43), Inches(4.35))
tbl = tbl_shape.table
tbl.first_row = True
tbl.horz_banding = True
tbl.columns[0].width = Inches(4.55)
tbl.columns[1].width = Inches(7.88)
tbl.rows[0].height = Inches(0.4)
for ri in range(1, len(rows)):
    tbl.rows[ri].height = Inches(1.0)
c = tbl.cell(0, 0); c.fill.solid(); c.fill.fore_color.rgb = NAVY
cell_text(c, "Project requirement", size=11, bold=True, color=WHITE)
c = tbl.cell(0, 1); c.fill.solid(); c.fill.fore_color.rgb = BLUE
cell_text(c, "My toolkit", size=11, bold=True, color=WHITE)
for ri in range(1, len(rows)):
    c0 = tbl.cell(ri, 0)
    c0.fill.solid(); c0.fill.fore_color.rgb = LIGHT2
    cell_text(c0, rows[ri][0], size=10.5, bold=True, color=NAVY, line=1.0)
    c1 = tbl.cell(ri, 1)
    c1.fill.solid(); c1.fill.fore_color.rgb = WHITE if ri % 2 == 1 else LIGHT2
    cell_text(c1, rows[ri][1], size=10.5, color=DARK, line=1.0)

band = card(s10, 0.45, 5.95, 12.43, 0.95, fill=LIGHT, line_color=None)
tf = band.text_frame; tf.word_wrap = True
tf.vertical_anchor = MSO_ANCHOR.MIDDLE
tf.margin_left = Inches(0.22); tf.margin_right = Inches(0.22)
p = tf.paragraphs[0]; p.line_spacing = 1.04
r = p.add_run(); r.text = "Simulation strategy:  "
_set_run(r, size=11.5, bold=True, color=NAVY)
r2 = p.add_run()
r2.text = ("commercial engines (EDEM, Rocky) for fast industrial delivery + open-source codes (LIGGGHTS, MFIX-DEM) for custom contact models, CFD-DEM coupling and cost control — "
           "validated the same way: physical experiments → bulk response → plant data.")
_set_run(r2, size=11.5, color=DARK)
notes(s10, "[11:45 – 13:15]\n\"Why am I the right candidate for this specific project? My academic training has provided me with a robust foundation in granular physics, continuum mechanics, and numerical programming. I have practical experience handling large data arrays and translating raw physical phenomena into structural code. Furthermore, I am deeply familiar with modern engineering simulation frameworks and possess the hands-on laboratory discipline required to design and execute validation experiments that will make our virtual models reliable.\"\n\nSlide notes: be ready to name the exact tools you have touched (EDEM/Rocky/LIGGGHTS/MFIX-DEM) and the exact experiments you can run (AOR, drop, draw-down, mass flow). The open-source angle shows cost awareness for a 4-year industrial PhD.")

# =====================================================================
# SLIDE 11 — Communication & collaborative mindset
# =====================================================================
s11 = new_slide()
header(s11, "TOPIC 4 — REFLECTION ON PERSONAL SKILLS & COMPETENCIES",
       "Communication & Collaborative Mindset", 11)

# left box — academia
Lx, Ly, Lw, Lh = 0.65, 1.65, 3.95, 3.6
card(s11, Lx, Ly, Lw, Lh, fill=LIGHT, line_color=BLUE, line_w=1.4)
tb, tf = add_box(s11, Lx + 0.25, Ly + 0.22, Lw - 0.5, Lh - 0.4)
para(tf, "TU Delft — Academic research", size=14, bold=True, color=NAVY, first=True, space_after=6)
bullets(tf, [
    (0, "DEM / CFD-DEM theory for non-spherical particles", 0),
    (0, "Rigorous validation science: lab experiments, uncertainty, upscaling", 0),
    (0, "Publication track record (international conferences & journals)", 0),
], size=10.5, space_after=7)

# right box — industry
Rx, Rw = 8.33, 4.35
card(s11, Rx, Ly, Rw, Lh, fill=RGBColor(0xD9, 0xEE, 0xFB), line_color=NAVY, line_w=1.4)
tb, tf = add_box(s11, Rx + 0.25, Ly + 0.22, Rw - 0.5, Lh - 0.4)
para(tf, "Tata Steel Netherlands — Industry", size=14, bold=True, color=NAVY, first=True, space_after=6)
bullets(tf, [
    (0, "IJmuiden plant data, access & operational constraints", 0),
    (0, "HBI + scrap recipes for green (hydrogen-based) steel production", 0),
    (0, "Plant engineers as co-developers of the digital twin", 0),
], size=10.5, space_after=7)

# bridge in the middle
bridge = s11.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5.12), Inches(3.05), Inches(3.1), Inches(0.82))
bridge.fill.solid(); bridge.fill.fore_color.rgb = NAVY
strip_border(bridge)
bt = bridge.text_frame
bt.word_wrap = True
bt.vertical_anchor = MSO_ANCHOR.MIDDLE
bt.margin_left = Inches(0.1); bt.margin_right = Inches(0.1)
p = bt.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
r = p.add_run(); r.text = "THIS PHD PROJECT"
_set_run(r, size=11, bold=True, color=AMBER)
p2 = bt.add_paragraph(); p2.alignment = PP_ALIGN.CENTER
r2 = p2.add_run(); r2.text = "particle-based digital twin of scrap handling"
_set_run(r2, size=9.5, color=WHITE)
# blue arrows: flow towards the project (right-pointing) on the top row
for dx in (4.86, 8.02):
    ar = s11.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(dx), Inches(3.28), Inches(0.28), Inches(0.30))
    ar.fill.solid(); ar.fill.fore_color.rgb = BLUE
    strip_border(ar)
# amber arrows: feedback flowing back (left-pointing) on the bottom row
for dx in (4.86, 8.02):
    ar = s11.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(dx), Inches(3.62), Inches(0.28), Inches(0.30))
    ar.fill.solid(); ar.fill.fore_color.rgb = AMBER
    strip_border(ar)
    ar.rotation = 180

tb, tf = add_box(s11, 0.65, 5.62, 12.0, 1.3)
para(tf, "I pride myself on being able to translate dense academic data into clear, operational value for plant operations.",
     size=13, bold=True, color=NAVY, first=True, space_after=6)
para(tf, "I am eager to collaborate directly with industrial engineers in the Netherlands — gathering on-site data, co-designing validation campaigns, and ensuring the doctoral research delivers practical, bottom-line improvements to the steelmaking process.",
     size=11, color=DARK, line=1.1)
notes(s11, "[13:15 – 14:15]\n\"Beyond technical software skills, a project backed by Tata Steel requires strong project management and cross-functional communication. I pride myself on being able to translate dense academic data into clear, operational value for plant operations. I am eager to collaborate directly with industrial engineers in the Netherlands, gathering on-site data and ensuring that my doctoral research delivers highly practical, bottom-line improvements to the steelmaking process.\"\n\nSlide notes: this is a values slide, not a CV. Name-drop the IJmuiden site and the green-steel context (HBI + scrap, hydrogen-based route) to show you know what the partner is building.")

# =====================================================================
# SLIDE 12 — Conclusion & Q&A
# =====================================================================
s12 = new_slide()
header(s12, "CLOSING", "Conclusion & Q&A", 12)

tks = [
    ("Theory", "DEM with realistic non-spherical representation (multi-sphere / super-quadric / polyhedra) is the right tool for scrap handling — shape is physics, not decoration."),
    ("Gap", "Charging/infeed is the weak link: conveyor DEM and EAF melting CFD are both mature; the mechanical, heterogeneous, real-time charging stage is not yet modelled."),
    ("Plan", "Coarse-graining + industrial calibration turns the gap into a validated digital twin of EAF infeed — optimised sequences, less wear, less energy."),
]
y = 1.42
for tag, t in tks:
    chip = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.45), Inches(y), Inches(1.35), Inches(0.62))
    chip.fill.solid(); chip.fill.fore_color.rgb = BLUE
    strip_border(chip)
    try:
        chip.adjustments[0] = 0.3
    except Exception:
        pass
    ctf = chip.text_frame
    ctf.vertical_anchor = MSO_ANCHOR.MIDDLE
    cp = ctf.paragraphs[0]; cp.alignment = PP_ALIGN.CENTER
    cr = cp.add_run(); cr.text = tag
    _set_run(cr, size=12, bold=True, color=WHITE)
    tb, tf = add_box(s12, 2.05, y - 0.03, 10.85, 0.9)
    para(tf, t, size=12, color=DARK, first=True, line=1.05)
    y += 1.02

band = card(s12, 0.45, 4.62, 12.43, 1.15, fill=NAVY, line_color=None)
tf = band.text_frame; tf.word_wrap = True
tf.vertical_anchor = MSO_ANCHOR.MIDDLE
tf.margin_left = Inches(0.25); tf.margin_right = Inches(0.25)
p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
r = p.add_run()
r.text = "Developing the next generation of particle models for sustainable, efficient EAF steel production."
_set_run(r, size=16, bold=True, color=WHITE)

tb, tf = add_box(s12, 0.45, 6.05, 12.43, 0.9)
p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
r = p.add_run(); r.text = "Thank you for your time — I welcome your questions."
_set_run(r, size=14, bold=True, color=NAVY)
p2 = tf.add_paragraph(); p2.alignment = PP_ALIGN.CENTER
r2 = p2.add_run(); r2.text = "Your Name  •  TU Delft  •  email@tu.nl"
_set_run(r2, size=10.5, color=GRAY)
notes(s12, "[14:15 – 15:00]\n\"In conclusion, this project represents a vital step toward making continuous EAF furnace feeding more predictable, energy-efficient, and physically stable. By mastering non-spherical particle mechanics, bridging the literature gap in scrap handling, and applying rigorous coarse-graining calibration, this research will provide invaluable tools for Tata Steel Netherlands. Thank you for your time, and I welcome any questions you may have.\"\n\nAnticipated questions to prepare: (1) Why multi-sphere instead of polyhedra/voxels for scrap? → contact-detection cost >80% CPU, robustness, existing EDEM support. (2) How do you validate at industrial scale? → high-speed video, load cells, vision-based feeder speed (Xiao et al.), mass balance. (3) What if upscaling breaks? → per-quantity scale limits (Rossow/Schefler), hybrid AVM+IFM-style strategy. (4) HBI relevance to Tata's green steel route.")

# =====================================================================
# SLIDE 13 — References
# =====================================================================
s13 = new_slide()
header(s13, "SUPPORTING LITERATURE", "References", 13)

refs_left = [
    "[1]  Lu G., Third J.R., Müller C.R. (2015). Discrete element models for non-spherical particle systems: from theoretical developments to applications. Chemical Engineering Science 127: 425–465.",
    "[2]  Zhong W., Yu A., Liu X., Tong Z., Zhang H. (2016). DEM/CFD-DEM modelling of non-spherical particulate systems: theoretical developments and applications. Powder Technology 300: 109–127.",
    "[3]  Rossow J., Coetzee C.J. (2021). Discrete element modelling of a chevron patterned conveyor belt and a transfer chute. Powder Technology 391: 77–96.",
    "[4]  Schefler O.C., Coetzee C.J. (2023). Discrete element modelling of a bulk cohesive material discharging from a conveyor belt onto an impact plate. Minerals 13(12): 1501.",
    "[5]  You Y., Liu M., Ma H., Xu L., Liu B., Shao Y., Tang Y., Zhao Y. (2018). Investigation of the vibration sorting of non-spherical particles based on DEM simulation. Powder Technology. doi:10.1016/j.powtec.2017.11.002.",
    "[6]  Xiao X., Zhong X., Ma M., Wu X. (2024). A visual based algorithm for measuring the speed of scrap metal vibration feeding. CSAE 2024 (ACM). doi:10.1145/3704814.3704817.",
    "[7]  Chen Y., Ryan S., Silaen A.K., Zhou C.Q. (2022). Simulation of scrap melting process in an AC electric arc furnace: CFD model development and experimental validation. Metallurgical and Materials Transactions B 53: 3256–3272.",
]
refs_right = [
    "[8]  Li J., Provatas N., Irons G.A. (2008). Modelling of late melting of scrap in an EAF. AISTech 2008, Irons A8046.",
    "[9]  Kryszak D., Bartoszewicz A., Szufa S., Piersa P., Obraniak A., Olejnik T.P. (2020). Modelling of transport of loose products with the use of the non-grid method of discrete elements (DEM). Processes 8(11): 1489.",
    "[10]  Garg R., Galvin J., Li T., Pannala S. (2012). Documentation of open-source MFIX-DEM software for gas-solids flows. National Energy Technology Laboratory / Oak Ridge National Laboratory.",
    "[11]  Kozicki J., Tejchman J. (2005). Application of a cellular automaton to simulations of granular flow in silos. Granular Matter 7: 45–54.",
    "[12]  Ahmed H., Pang Y., Adema A., et al. (2026). Industrial-scale DEM modelling of segregation in the blast furnace charging system (Tata Steel IJmuiden). Powder Technology.",
    "[13]  Guo D., Irons G.A. (2008). Modelling of steel scrap movement. Applied Mathematical Modelling. doi:10.1016/j.apm.2007.06.037.",
    "[14]  Ugarte O., Li J., Haeberle J., et al. (2024). CFD modelling of HBI/scrap melting in industrial EAF and the impact of charge layering on melting performance. Materials 17(21): 5139.",
]
for x0, refs in ((0.45, refs_left), (6.75, refs_right)):
    tb, tf = add_box(s13, x0, 1.35, 6.1, 5.6)
    first = True
    for ref in refs:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.space_after = Pt(8)
        p.line_spacing = 1.0
        r = p.add_run(); r.text = ref
        _set_run(r, size=8.5, color=DARK)
notes(s13, "Reference list — no speaking time. References [1]–[11] have full PDFs in the 'papers/particles-based models' folder of the project repository; [12]–[14] are the additional state-of-the-art sources from the literature plan (planning.md).")

# =====================================================================
# SLIDE 1 — Title (kept from the started deck); add opening script
# =====================================================================
notes(prs.slides[0], "[0:00 – 1:00]\n\"Good morning, everyone. Today, I am excited to present my research proposal for developing an advanced particle-based modelling framework for optimising scrap handling systems. In the next 15 minutes, I will walk you through the fundamental theory of the Discrete Element Method (DEM), the critical knowledge gaps in EAF scrap feeding, my proposed 4-year methodology, and how my technical background aligns with Tata Steel's operational goals.\"\n\nSlide notes: keep the opening short and confident; make eye contact; the committee values time management — this deck is timed for exactly 15 minutes of speaking (slides 2–12), with the reference slide [13] as backup.")

prs.save(OUT)
print("Saved:", OUT, "with", len(prs.slides._sldIdLst), "slides")
