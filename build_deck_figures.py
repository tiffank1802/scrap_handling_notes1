#!/usr/bin/env python3
"""Build the figure-based evidence deck.

A companion to 'Delft Phd scrap handling - completed.pptx': every statement
is backed by a figure taken from the papers in 'papers/particles-based models/'.
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image
import os

SRC = "presentation/Delft Phd scrap handling.pptx"   # the started deck (logos/title)
OUT = "presentation/Delft Phd scrap handling - paper figures.pptx"
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
    para(tf, "Particle-Based Modelling of Scrap Handling  •  evidence from the literature  •  TU Delft × Tata Steel",
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

# =====================================================================
# SLIDE 1 — title (kept from started deck)
# =====================================================================
notes(prs.slides[0], "Companion deck to the main 15-minute presentation. Every claim in the main deck is supported here by a figure taken directly from the papers in the repository ('papers/particles-based models'). Use as backup / evidence slides, or walk through the ~6 strongest (S3, S7, S8, S10, S11, S12) if time allows.")

# =====================================================================
# SLIDE 2 — evidence map
# =====================================================================
s = new_slide()
header(s, "HOW TO READ THIS DECK", "Evidence Map: From Particle Physics to the Furnace", 2)
steps = [
    ("1", "Shape & contact", "how non-spherical scrap is represented"),
    ("2", "Shape → flow", "packing, angle of repose, discharge"),
    ("3", "Belt & chevron", "DEM at the moving boundary"),
    ("4", "Chute & upscaling", "flow, build-up, scaling limits"),
    ("5", "Vibratory feeding", "sorting, segregation, design rules"),
    ("6", "Into the furnace", "late melting — and the infeed gap"),
]
cw, ch = 3.98, 2.35
for i, (n, t, sub) in enumerate(steps):
    x = 0.45 + (i % 3) * (cw + 0.24)
    y = 1.45 + (i // 3) * (ch + 0.3)
    card(s, x, y, cw, ch, fill=LIGHT2, line_color=BLUE, line_w=1.1)
    c = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x + 0.18), Inches(y + 0.18), Inches(0.5), Inches(0.5))
    c.fill.solid(); c.fill.fore_color.rgb = BLUE
    c.line.fill.background(); c.shadow.inherit = False
    ctf = c.text_frame; ctf.vertical_anchor = MSO_ANCHOR.MIDDLE
    cp = ctf.paragraphs[0]; cp.alignment = PP_ALIGN.CENTER
    cr = cp.add_run(); cr.text = n; _set_run(cr, size=16, bold=True, color=WHITE)
    tb, tf = add_box(s, x + 0.85, y + 0.22, cw - 1.0, 0.85)
    para(tf, t, size=14.5, bold=True, color=NAVY, first=True)
    tb, tf = add_box(s, x + 0.22, y + 1.0, cw - 0.44, ch - 1.1)
    para(tf, sub, size=10.5, color=GRAY, first=True, line=1.05)
band = card(s, 0.45, 6.35, 12.43, 0.6, fill=NAVY, line_color=None)
tf = band.text_frame; tf.word_wrap = True; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
tf.margin_left = Inches(0.2)
p = tf.paragraphs[0]
r = p.add_run(); r.text = "Each of the 6 blocks = one slide below with figures from the papers + the statements they support."
_set_run(r, size=10.5, color=WHITE)
notes(s, "One minute: show the committee the evidence chain. 35 figures from 10 papers in the repository, each supporting a specific statement from the main deck.")

# =====================================================================
# SLIDE 3 — shape & contact
# =====================================================================
s = new_slide()
header(s, "EVIDENCE 1 — SHAPE & CONTACT", "Scrap Is Not Spherical: Representation & Contact Mechanics", 3)
tb, tf = add_box(s, 0.45, 1.30, 4.35, 5.6)
para(tf, "What the figures show", size=12.5, bold=True, color=NAVY, first=True, space_after=6)
bullets(tf, [
    ("Multi-sphere clusters are the workhorse: 3D-scanned grains → STL → 3/5/10-sphere “clumps” (Rossow & Coetzee 2021, Fig. 1)", False),
    ("Polyhedra / voxelised meshes capture angular, non-convex geometry directly (Lu et al. 2015, Fig. 14)", False),
    ("Super-ellipsoids vary blockiness continuously via the shape index s (You et al. 2018)", False),
    ("Every contact carries Fn + Ft; defining the contact point is where non-sphericals get hard (Lu et al. 2015, Fig. 3)", True),
], size=10.5, space_after=8)
place_fig(s, "s3_clumps",      5.05, 1.30, 3.95, 2.55, "Scanned grains → 3 / 5 / 10-sphere multi-sphere clumps (Rossow & Coetzee, 2021, Fig. 1)")
place_fig(s, "s3_polyhedra",   9.15, 1.30, 3.75, 2.55, "Voxelised non-convex polyhedron: vertex/edge/face offsets (Lu et al., 2015, Fig. 14)")
place_fig(s, "s3_fig3",        5.05, 4.00, 5.20, 2.85, "Contact point, normal, overlap — spheres (a) vs non-sphericals (b, c) (Lu et al., 2015, Fig. 3)")
place_fig(s, "s3_superellip",  10.45, 4.00, 2.45, 2.85, "Super-ellipsoid family, s = 2…7 (You et al., 2018)")
notes(s, "Walk the four quadrants: (top-left) the clump workflow used for irregular particles — the same workflow applies to 3D-scanned scrap; (top-right) angular geometry via voxels; (bottom-left) why contact mechanics is harder for non-sphericals (Fig. 3c: sudden contact-point jumps → multi-point contact needed); (bottom-right) smooth shapes via super-ellipsoids. Message: representation choice = physics choice, and it drives contact-detection cost (>80% of CPU, Lu 2015).")

# =====================================================================
# SLIDE 4 — superquadric
# =====================================================================
s = new_slide()
header(s, "EVIDENCE 1 — SHAPE & CONTACT", "Super-Quadrics: One Equation, a Whole Shape Family", 4)
tb, tf = add_box(s, 0.45, 1.30, 4.35, 5.6)
para(tf, "What the figures show", size=12.5, bold=True, color=NAVY, first=True, space_after=6)
bullets(tf, [
    ("The super-quadric equation sweeps ellipsoid → blocky → star-like shapes by the exponents ε₁, ε₂ (Lu et al. 2015, Fig. 6)", False),
    ("The surface normal is available analytically — a compact, parameterisable description (Lu et al. 2015, Eq. 16)", False),
    ("Contact between two super-quadrics is found iteratively inside a curvilinear region Ω (Lu et al. 2015, Fig. 4b)", False),
    ("Best for smooth, regular, systematically varied shapes; weak for sharp edges & flat faces", True),
], size=10.5, space_after=8)
place_fig(s, "s4_family",   5.05, 1.30, 7.85, 3.30, "Fig. 6 — 3D super-quadric family: ε₁ (left→right), ε₂ (top→bottom), exponents 0.3–10 (Lu et al., 2015)")
place_fig(s, "s4_eq16",     5.05, 4.72, 4.30, 1.95, "Eq. (16) — implicit 3D super-quadric function (Lu et al., 2015)")
place_fig(s, "s4_contactom",9.50, 4.72, 3.40, 1.95, "Fig. 4b — contact region Ω approximation (Lu et al., 2015)")
notes(s, "For shredded/baled scrap, super-quadrics model the rounded bales; for HMS bundles, polyhedra; for general fragments, multi-sphere clusters from scans. The figure also shows why we don't rely on one representation: every method has a preferred application range (Lu 2015 §7; Zhong 2016).")

# =====================================================================
# SLIDE 5 — shape affects flow
# =====================================================================
s = new_slide()
header(s, "EVIDENCE 2 — SHAPE → FLOW", "Shape Decides Packing, Piling and Discharge", 5)
tb, tf = add_box(s, 0.45, 1.22, 12.4, 1.15)
bullets(tf, [
    ("Same material, different shape representation → different hopper discharge (Zhong et al. 2016, Fig. 20)", False),
    ("Bed structure & layering differ between spherical, cuboidal, prolate and oblate particles (Zhong et al. 2016, Fig. 45)", False),
    ("Angle of repose grows as particles become less spherical (Lu et al. 2015, Fig. 32) — the classic calibration experiment", True),
], size=10.5, space_after=5)
place_fig(s, "s5_hopper", 0.45, 2.60, 4.05, 4.15, "Hopper discharge: smoothed polyhedra / multi-sphere / super-ellipsoid (Zhong et al., 2016, Fig. 20)")
place_fig(s, "s5_bed",    4.65, 2.60, 4.05, 4.15, "Bed structure by shape (Zhong et al., 2016, Fig. 45)")
place_fig(s, "s5_aor",    8.85, 2.60, 4.05, 4.15, "Angle-of-repose piles — shape effect (Lu et al., 2015, Fig. 32)")
notes(s, "These three figures justify the whole non-spherical effort: shape changes discharge, layering and pile angle — exactly the phenomena behind chute blockage, bridging and segregation of scrap. Note AOR (angle of repose) as the cheapest lab calibration for our virtual scrap.")

# =====================================================================
# SLIDE 6 — chevron belt
# =====================================================================
s = new_slide()
header(s, "EVIDENCE 3 — BELT & CHEVRON", "The Chevron Belt: DEM at the Moving Boundary", 6)
tb, tf = add_box(s, 0.45, 1.30, 4.35, 5.6)
para(tf, "What the figures show", size=12.5, bold=True, color=NAVY, first=True, space_after=6)
bullets(tf, [
    ("First DEM study of a chevron-patterned belt: CAD model and the physical test belt (Rossow & Coetzee 2021, Fig. 3)", False),
    ("Wall friction + belt-velocity boundary conditions carry the material — the same physics as a scrap conveyor", False),
    ("Particle-by-particle comparison with high-speed footage (Rossow & Coetzee 2021, Fig. 8)", True),
], size=10.5, space_after=8)
place_fig(s, "s6_chev_cad",   5.05, 1.30, 7.85, 1.75, "Chevron-patterned belt in the DEM model (Rossow & Coetzee, 2021, Fig. 3a)")
place_fig(s, "s6_chev_photo", 5.05, 3.15, 1.95, 3.70, "The physical chevron belt (Rossow & Coetzee, 2021, Fig. 3)")
place_fig(s, "s6_belt_flow",  7.15, 3.15, 5.75, 3.70, "Material flow on the chevron belt — DEM (left) vs high-speed footage (right) (Rossow & Coetzee, 2021, Fig. 8)")
notes(s, "Chevron belts grip the material by geometry, not friction alone — crucial for scrap. The side-by-side DEM/footage comparison is the validation standard we will reuse for scrap feeders: high-speed video + PIV at Tata Steel NL.")

# =====================================================================
# SLIDE 7 — chute transfer
# =====================================================================
s = new_slide()
header(s, "EVIDENCE 4 — CHUTE & TRANSFER", "Chute Transfer: DEM Predicts Flow, Build-Up and Blockage", 7)
tb, tf = add_box(s, 0.45, 1.22, 12.4, 1.5)
bullets(tf, [
    ("One calibrated model covers belt → impact plate → hood → rock box → chute (first study to do all of this, Rossow & Coetzee 2021)", False),
    ("Accuracy vs experiment: mass flow ≤ 5.4%, impact velocity < 6.1%, impact-wall force < 17% — better than analytical models", False),
    ("Build-up and blockage are predicted, not assumed — the exact failure mode of EAF infeed chutes", True),
], size=10.5, space_after=5)
place_fig(s, "s7_chute",   0.45, 2.85, 4.05, 3.90, "Chute transfer flow — DEM (left) vs high-speed footage (right) (Rossow & Coetzee, 2021, Fig. 13)")
place_fig(s, "s7_rockbox", 4.65, 2.85, 4.05, 3.90, "Rock-box build-up — DEM & experiment (Rossow & Coetzee, 2021, Fig. 21)")
place_fig(s, "s7_impact",  8.85, 2.85, 4.05, 3.90, "Impact-plate outflow velocity field — DEM & footage (Rossow & Coetzee, 2021, Fig. 10)")
notes(s, "The key quote for the committee: 'DEM can be used with confidence in modelling similar applications if a calibrated parameter set is used, and the guidelines presented here in terms of particle scaling are adhered to' (Rossow & Coetzee, 2021). For EAF scrap: same methodology, more irregular particles.")

# =====================================================================
# SLIDE 8 — cohesive & upscaling
# =====================================================================
s = new_slide()
header(s, "EVIDENCE 4 — CHUTE & TRANSFER", "Cohesive Scrap: Build-Up, and the Limits of Upscaling", 8)
tb, tf = add_box(s, 0.45, 1.22, 4.35, 5.7)
para(tf, "What the figures show", size=12.5, bold=True, color=NAVY, first=True, space_after=6)
bullets(tf, [
    ("Wet-and-sticky material builds up and can block — realistic for dusty/wet scrap (Schefler & Coetzee 2023)", False),
    ("Upscaled DEM reproduces discharge, build-up, force & residual mass with < 15% error", False),
    ("But upscaling has hard limits: scale ≤ 1.6 keeps error ≤ 10% (Rossow & Coetzee 2021, Table 9)", True),
    ("The maximum scale factor is a geometric property of the bulk measure of interest — and grows with cohesion (Schefler & Coetzee 2023)", True),
], size=10.5, space_after=7)
place_fig(s, "s8_discharge",   5.05, 1.30, 3.95, 2.75, "Discharge from belt to inclined impact plate — experiment (Schefler & Coetzee, 2023)")
place_fig(s, "s8_buildup_exp", 9.15, 1.30, 3.75, 2.75, "Adhesion build-up on the plate — experiment (Schefler & Coetzee, 2023)")
place_fig(s, "s8_buildup_dem", 5.05, 4.15, 2.60, 2.75, "DEM build-up profile (Schefler & Coetzee, 2023)")
place_fig(s, "s8_table9",      7.80, 4.15, 5.10, 2.75, "Table 9 — scale factor vs error; red = > 10% = inaccurate (Rossow & Coetzee, 2021)")
notes(s, "This slide answers the inevitable 'how do you simulate metres of scrap?' question with numbers, not promises: 1.6× upscaling is validated (≤10% error), the limit depends on the quantity you care about, and cohesion relaxes the limit. Our coarse-graining strategy inherits exactly these guidelines.")

# =====================================================================
# SLIDE 9 — vibratory feeding
# =====================================================================
s = new_slide()
header(s, "EVIDENCE 5 — VIBRATORY FEEDING", "Vibratory Feeders: Sorting, Segregation and a Design Rule", 9)
tb, tf = add_box(s, 0.45, 1.22, 4.35, 5.7)
para(tf, "What the figures show", size=12.5, bold=True, color=NAVY, first=True, space_after=6)
bullets(tf, [
    ("DEM of an inclined vibrating plate reproduces the sorting experiment (You et al. 2018, Fig. 6)", False),
    ("Non-spherical test particles modelled as super-ellipsoids (sphere & cube), mixed 1:1", False),
    ("Vibration frequency & amplitude set the discharge order → structural segregation", False),
    ("Effective separation when (2πf)²A ≈ 1.5g — a usable design rule for scrap feeders", True),
], size=10.5, space_after=7)
place_fig(s, "s9_device",     5.05, 1.30, 7.85, 2.60, "Vibration sorting device — experiment & DEM side by side (You et al., 2018, Fig. 6)")
place_fig(s, "s9_dem_models", 5.05, 4.00, 1.95, 2.85, "DEM super-ellipsoid models: sphere & cube (You et al., 2018)")
place_fig(s, "s9_sorting",    7.15, 4.00, 5.75, 2.85, "Separation patterns on the plate — DEM (You et al., 2018)")
notes(s, "Why this matters for scrap: heterogeneous recipes (bales + shreds + HMS) on a vibratory feeder will self-segregate before the chute. The 1.5g rule (You et al. 2018) tells us when sorting happens — we will use it to predict which scrap discharges first and prevent chute blockage.")

# =====================================================================
# SLIDE 10 — vision measurement
# =====================================================================
s = new_slide()
header(s, "EVIDENCE 5 — VIBRATORY FEEDING", "Measuring Real Scrap Feeding: It Is Possible Today", 10)
tb, tf = add_box(s, 0.45, 1.22, 4.35, 5.7)
para(tf, "What the figures show", size=12.5, bold=True, color=NAVY, first=True, space_after=6)
bullets(tf, [
    ("Feature-point tracking (SuperPoint) measures feeding speed on real scrap — no object detection needed (Xiao et al. 2024)", False),
    ("Works despite heterogeneous types, sizes, stacking & occlusion on the vibratory conveyor", False),
    ("On-site validation: measured speed curve matches the horizontal-vibrator frequency curve", True),
    ("→ a real industrial measurement target exists for validating our DEM feeding models", True),
], size=10.5, space_after=7)
place_fig(s, "s10_feeder",   5.05, 1.30, 7.85, 2.30, "Real scrap on the vibratory feeder with tracked feature trajectories (Xiao et al., 2024)")
place_fig(s, "s10_speed",    5.05, 3.70, 4.55, 2.15, "Feeding speed vs vibrator frequency — on-site data (Xiao et al., 2024)")
place_fig(s, "s10_pipeline", 9.75, 3.70, 3.15, 2.15, "Method pipeline (Xiao et al., 2024)")
notes(s, "This is the strongest 'industrial awareness' slide: someone at CISDI is already measuring scrap feeder speed with vision in a running plant. Our plan reuses exactly this class of measurement (plus high-speed video & load cells from Rossow/Schefler) to validate the digital twin at Tata Steel NL.")

# =====================================================================
# SLIDE 11 — late melting
# =====================================================================
s = new_slide()
header(s, "EVIDENCE 6 — INTO THE FURNACE", "After the Charge: Late Melting and “Steel Icebergs”", 11)
tb, tf = add_box(s, 0.45, 1.22, 4.35, 5.7)
para(tf, "What the figures show", size=12.5, bold=True, color=NAVY, first=True, space_after=6)
bullets(tf, [
    ("Scrap in the bath grows a solidified shell that agglomerates into “steel icebergs” — they dominate the final melting time (Li et al. 2008)", False),
    ("Porosity decides the regime: full iceberg → partial iceberg → independent melting (final melting time varies 3–4×)", False),
    ("The bath is virtually stagnant (thermal stratification); preheating & stirring cut melting time sharply", False),
    ("→ an uneven, heterogeneous charge arrives wrong → late melting, tapping delays, energy spikes", True),
], size=10.5, space_after=7)
place_fig(s, "s11_iceberg",    5.05, 1.30, 3.95, 2.80, "Final melting time vs porosity — iceberg regimes (Li et al., 2008, Fig. 2)")
place_fig(s, "s11_melttime",   9.15, 1.30, 3.75, 2.80, "Effective melting time vs solid fraction & bath temperature (Li et al., 2008)")
place_fig(s, "s11_phasefield", 5.05, 4.20, 3.00, 2.70, "Phase-field melting evolution, 0 → 3393 s (Li et al., 2008, Fig. 1)")
# right-bottom: text callout
card(s, 8.25, 4.20, 4.65, 2.70, fill=LIGHT, line_color=BLUE, line_w=1.2)
tb, tf = add_box(s, 8.45, 4.38, 4.25, 2.4)
para(tf, "Link to handling", size=11, bold=True, color=NAVY, first=True, space_after=5)
para(tf, "Iceberg formation is driven by how the charge packs and settles — i.e. by the mechanical infeed we propose to model. Better, more uniform feeding → smaller, more uniform melting units → shorter, steadier heats.",
     size=10.5, color=DARK, line=1.08)
notes(s, "The causal chain that justifies the whole project: infeed heterogeneity → charge packing/porosity → iceberg formation → late melting → energy & productivity losses (Li, Provatas & Irons 2008). This is the 'so what' behind gap 2 in the main deck.")

# =====================================================================
# SLIDE 12 — EAF CFD
# =====================================================================
s = new_slide()
header(s, "EVIDENCE 6 — INTO THE FURNACE", "EAF Melting: Mature & Validated — the Infeed Is Not", 12)
tb, tf = add_box(s, 0.45, 1.22, 4.35, 5.7)
para(tf, "What the figures show", size=12.5, bold=True, color=NAVY, first=True, space_after=6)
bullets(tf, [
    ("Fully 3-D integrated CFD: melting + collapse + arc + burners, in an industrial 150-t EAF (Chen et al. 2022)", False),
    ("Scrap enters as a lumped stack input (dual-cell / stack approach) — its mechanical history is not resolved", False),
    ("Validated against plant data (electrode behaviour, pit diameter: shredded & busheling)", True),
    ("→ melting is the strong half; the mechanical infeed upstream is the missing half", True),
], size=10.5, space_after=7)
place_fig(s, "s12_eaf3d",    5.05, 1.30, 3.95, 2.80, "3-D EAF model: electrodes, scrap pile, coherent jet burner, hot heel (Chen et al., 2022)")
place_fig(s, "s12_dualcell", 9.15, 1.30, 3.75, 2.80, "Dual-cell (stack) approach for melting & collapse (Chen et al., 2022)")
place_fig(s, "s12_sequence", 5.05, 4.20, 4.55, 2.70, "Melting & collapse of the second bucket (Chen et al., 2022)")
place_fig(s, "s12_pit",      9.75, 4.20, 3.15, 2.70, "Validation: measured vs simulated pit diameter (Chen et al., 2022)")
notes(s, "Balance slide: we do NOT question EAF melting modelling — it is excellent and industrially validated. Our contribution is everything upstream: how the charge actually arrives (structure, sequence, segregation). The digital twin hands off to models like this one.")

# =====================================================================
# SLIDE 13 — the gap -> PhD
# =====================================================================
s = new_slide()
header(s, "CONCLUSION — THE GAP & THE PHD PROJECT", "Both Ends Are Mature — the Infeed Interface Is Missing", 13)
place_fig(s, "s13_apps", 0.45, 1.35, 4.35, 4.35, "DEM applications across industry — bulk handling is everywhere (Zhong et al., 2016, Fig. 1)")
place_fig(s, "s13_buckets", 5.05, 1.35, 7.85, 4.35, "Charge buckets enter the furnace as discrete, structured inputs (Chen et al., 2022)")
cards = [
    ("Conveyor / chute DEM", "mature, calibrated, validated (Rossow 2021; Schefler 2023; You 2018)"),
    ("EAF melting CFD", "mature, industrially validated (Chen 2022; Li 2008)"),
    ("Heterogeneous scrap infeed", "the missing link — size, shape, density, chemistry, real-time segregation"),
]
cw = 4.02
for i, (t, b) in enumerate(cards):
    x = 0.45 + i * (cw + 0.185)
    fill = LIGHT if i < 2 else NAVY
    tc = NAVY if i < 2 else WHITE
    bc = DARK if i < 2 else RGBColor(0xD9, 0xEE, 0xFB)
    card(s, x, 5.95, cw, 1.05, fill=fill, line_color=None)
    tb, tf = add_box(s, x + 0.14, 6.04, cw - 0.28, 0.9)
    p = tf.paragraphs[0]
    r = p.add_run(); r.text = t + "  —  "
    _set_run(r, size=10, bold=True, color=tc)
    r2 = p.add_run(); r2.text = b
    _set_run(r2, size=9, color=bc)
    p.line_spacing = 0.98
notes(s, "The closing argument, backed by figures: mature DEM + mature CFD + missing interface = the PhD. The project builds the interface: a multi-scale, multi-property digital twin of EAF scrap infeed, calibrated on Tata Steel NL data over 4 years.")

# =====================================================================
# SLIDE 14 — figure references
# =====================================================================
s = new_slide()
header(s, "SUPPORTING LITERATURE", "Figure Sources (papers in the repository)", 14)
refs_l = [
    "[1]  Lu G., Third J.R., Müller C.R. (2015). Discrete element models for non-spherical particle systems: from theoretical developments to applications. Chemical Engineering Science 127: 425–465. — Figs 1, 3, 6, 14, 32, 4b, Eq. 16",
    "[2]  Rossow J., Coetzee C.J. (2021). Discrete element modelling of a chevron patterned conveyor belt and a transfer chute. Powder Technology 391: 77–96. — Figs 1, 3, 8, 10, 13, 21, Table 9",
    "[3]  Schefler O.C., Coetzee C.J. (2023). Discrete element modelling of a bulk cohesive material discharging from a conveyor belt onto an impact plate. Minerals 13(12): 1501. — discharge, build-up & DEM profile figures",
    "[4]  You Y., Liu M., Ma H., et al. (2018). Investigation of the vibration sorting of non-spherical particles based on DEM simulation. Powder Technology. doi:10.1016/j.powtec.2017.11.002 — Figs 6, super-ellipsoids, sorting patterns",
    "[5]  Xiao X., Zhong X., Ma M., Wu X. (2024). A visual based algorithm for measuring the speed of scrap metal vibration feeding. CSAE 2024 (ACM). doi:10.1145/3704814.3704817 — feeder tracking, speed curve, pipeline",
    "[6]  Li J., Provatas N., Irons G.A. (2008). Modelling of late melting of scrap in an EAF. AISTech 2008, Irons A8046. — Figs 1, 2, melting-time charts",
]
refs_r = [
    "[7]  Chen Y., Ryan S., Silaen A.K., Zhou C.Q. (2022). Simulation of scrap melting process in an AC electric arc furnace: CFD model development and experimental validation. Metall. Mater. Trans. B 53: 3256–3272. — 3-D model, dual-cell, sequence, pit validation",
    "[8]  Zhong W., Yu A., Liu X., Tong Z., Zhang H. (2016). DEM/CFD-DEM modelling of non-spherical particulate systems: theoretical developments and applications. Powder Technology 300: 109–127. — Figs 1, 20, 45",
    "[9]  Kryszak D., Bartoszewicz A., Szufa S., Piersa P., Obraniak A., Olejnik T.P. (2020). Modelling of transport of loose products with the use of the non-grid method of discrete elements (DEM). Processes 8(11): 1489. — force spectra on conveyed product",
    "[10] Garg R., Galvin J., Li T., Pannala S. (2012). Documentation of open-source MFIX-DEM software for gas-solids flows. NETL/ORNL.",
    "[11] Kozicki J., Tejchman J. (2005). Application of a cellular automaton to simulations of granular flow in silos. Granular Matter 7: 45–54.",
    "[12] Ahmed H., Pang Y., Adema A., et al. (2026). Industrial-scale DEM modelling of segregation in the blast furnace charging system (Tata Steel IJmuiden). Powder Technology.",
]
for x0, refs in ((0.45, refs_l), (6.75, refs_r)):
    tb, tf = add_box(s, x0, 1.35, 6.1, 5.6)
    first = True
    for ref in refs:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.space_after = Pt(9); p.line_spacing = 1.02
        r = p.add_run(); r.text = ref
        _set_run(r, size=8.5, color=DARK)
notes(s, "All figures were extracted from the PDFs in 'papers/particles-based models' (see file names in the slide captions). Permission note: figures are reproduced for the PhD interview presentation of the repository owner, who holds these papers; keep this use non-public.")

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
