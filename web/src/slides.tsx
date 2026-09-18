import type { ReactNode } from "react";

/* ============================================================
   Slides — 1:1 recreation of
   'Delft Phd scrap handling - completed.pptx' (13 slides)
   Stage design size: 1280 × 720 (16:9).
   ============================================================ */

interface ShellProps {
  kicker: string;
  title: string;
  idx: number;
  children: ReactNode;
  foot?: string;
  smallTitle?: boolean;
}

const FOOT = "Particle-Based Modelling of Scrap Handling for Green Steel Production  •  TU Delft × Tata Steel Netherlands";

function Shell({ kicker, title, idx, children, foot = FOOT, smallTitle }: ShellProps) {
  return (
    <div className="slide">
      <div className="slide-head">
        <p className="kicker">{kicker}</p>
        <h1 className={`slide-title ${smallTitle ? "small" : ""}`}>{title}</h1>
      </div>
      <div className="body">{children}</div>
      <div className="slide-foot">
        <span>{foot}</span>
        <span className="line" />
        <span className="nowrap">{idx}</span>
      </div>
    </div>
  );
}

/* ---------------- slide 1 — title ---------------- */
function Slide01() {
  return (
    <div className="slide title-slide">
      <div>
        <p className="kicker" style={{ justifyContent: "center" }}>PhD Thesis — Research Proposal</p>
      </div>
      <h1>Particle Based Modelling of Scrap Handling<br />for Green Steel Production</h1>
      <p className="sub">
        Discrete Element Modelling of non-spherical, multi-material scrap streams —
        from vibratory feeder to electric arc furnace infeed.
      </p>
      <div className="title-logos">
        <div className="logo-card" style={{ padding: "10px 22px" }}>
          <img className="tud" src="/img/tudelft-logo.png" alt="TU Delft" />
        </div>
        <span className="x">×</span>
        <div className="logo-card" style={{ padding: "14px 26px" }}>
          <img className="tata" src="/img/tata-logo.png" alt="Tata Steel" />
        </div>
      </div>
      <p className="sub" style={{ fontSize: 13, color: "var(--ink-faint)" }}>
        Kevin Tongue  •  tonguekevin00@gmail.com
      </p>
    </div>
  );
}

/* ---------------- slide 2 — agenda ---------------- */
function Slide02() {
  const items = [
    ["Theory of particle-based models (DEM) & conveyor systems", "Non-spherical shape representation • contact mechanics • belt / chute / vibratory-feeder kinematics"],
    ["State of the art & knowledge gaps in scrap / EAF modelling", "Where the literature stands today — and what it has not solved"],
    ["Methodology, novelty & anticipated challenges", "4-year research plan • coarse-graining calibration strategy • project novelty"],
    ["Skills, competencies & personal reflection", "Technical toolkit • data integration • experimental validation • industrial collaboration"],
  ];
  return (
    <Shell kicker="Agenda" title="Agenda" idx={2}>
      <div className="col grow" style={{ justifyContent: "center" }}>
        {items.map(([t, s], i) => (
          <div key={i} className="glass padded" style={{ display: "flex", alignItems: "center", gap: 18, padding: "16px 22px" }}>
            <span className="chip" style={{ width: 40, height: 40, fontSize: 17 }}>{i + 1}</span>
            <div className="grow">
              <div style={{ fontSize: 16, fontWeight: 800, letterSpacing: "-0.01em" }}>{t}</div>
              <div style={{ fontSize: 12.5, color: "var(--ink-soft)", marginTop: 3 }}>{s}</div>
            </div>
          </div>
        ))}
      </div>
    </Shell>
  );
}

/* ---------------- slide 3 — DEM fundamentals ---------------- */
function Slide03() {
  return (
    <Shell kicker="Topic 1 — Particle-based modelling (DEM)" title="DEM Fundamentals & Particle Shape Representation" idx={3} smallTitle>
      <div className="row grow">
        <div className="glass padded grow" style={{ paddingRight: 22 }}>
          <ul className="b-list">
            <li>DEM tracks every scrap fragment individually via Newton's laws (Lagrangian); each contact carries a normal force <b>F<sub>n</sub></b> and a tangential force <b>F<sub>t</sub></b> (spring–damper contact model)</li>
            <li>Scrap is never round — shape controls friction, interlocking, bridging and segregation, so spheres alone roll too easily</li>
            <li><b>Non-spherical shape representation</b> (Lu et al. 2015; Zhong et al. 2016):</li>
            <li className="sub">Multi-sphere clusters — robust; reuses sphere–sphere contacts; best proxy for shredded scrap</li>
            <li className="sub">Polyhedra — angular rock/scrap; common-plane contact; many contact cases to classify</li>
            <li className="sub">Super-quadrics — smooth, regular shapes; ε₁, ε₂ vary roundness → blockiness continuously</li>
            <li className="sub">Voxel / digitised — arbitrary 3D-scanned shapes; grid-resolution limited</li>
            <li className="sub">Bonded particles — add fracture &amp; deformation</li>
            <li>Key trade-off: <span className="hl">contact detection alone can consume &gt;80% of the computation time</span></li>
          </ul>
        </div>
        <div style={{ width: 452, display: "flex", flexDirection: "column", gap: 8 }}>
          <div className="fig-frame" style={{ flex: 1 }}>
            <img src="/img/fig-superquadrics.png" alt="Super-quadric family" />
          </div>
          <p className="fig-cap">Fig. 6 — 3D super-quadric family: ε₁ (left→right), ε₂ (top→bottom) (Lu et al., 2015)</p>
        </div>
      </div>
      <div className="row" style={{ marginTop: 14 }}>
        <div style={{ width: "47%", display: "flex", flexDirection: "column", gap: 6 }}>
          <div className="fig-frame" style={{ height: 128 }}>
            <img src="/img/fig-eq16.png" alt="Equation 16 — super-quadric function" />
          </div>
          <p className="fig-cap">Eq. (16) — 3D super-quadric implicit function; ε₁ = ε₂ = 1 gives an ellipsoid (Lu et al., 2015)</p>
        </div>
        <div style={{ width: "47%", display: "flex", flexDirection: "column", gap: 6 }}>
          <div className="fig-frame" style={{ height: 128 }}>
            <img src="/img/fig-contact.png" alt="Contact region omega" />
          </div>
          <p className="fig-cap">Fig. 4b — approximation of the actual contact region Ω between two super-quadrics (Lu et al., 2015)</p>
        </div>
      </div>
    </Shell>
  );
}

/* ---------------- slide 4 — conveyor & vibratory feeders ---------------- */
function Slide04() {
  const mini = [
    ["Belt conveyor", "chevron patterned belt • wall friction • belt velocity"],
    ["Transfer chute", "impact plate • hood • rock box • build-up & blockage"],
    ["Vibratory feeder", "inertial vibration: frequency, amplitude, inclination"],
    ["EAF infeed", "continuous charging into the furnace"],
  ];
  const papers = [
    ["Rossow & Coetzee (2021) — chevron belt + transfer chute", "Powder Technol. 391:77–96", [
      "First DEM study of a chevron-patterned belt with impact plate, hood and rock box; 3D-laser-scanned particles modelled as 3/5/10-sphere multi-sphere “clumps”",
      "Validated against high-speed footage: mass flow ≤5.4% error, impact velocity <6.1%, impact-wall force <17%",
      "Maximum particle up-scaling factor 1.6 (≤10% error) — DEM beat the analytical model in accuracy",
    ]],
    ["Schefler & Coetzee (2023) — cohesive belt discharge", "Minerals 13(12):1501", [
      "Wet-and-sticky material discharging from belt onto an inclined impact plate: build-up profile, peak impact force and residual weight reproduced with <15% error using upscaled particles",
      "Max acceptable scale factor is a geometric property of the bulk measure of interest — not of the physical particle size",
      "Higher cohesion → thicker discharge stream & taller build-up → higher allowable scale factor",
    ]],
    ["You et al. (2018) — vibration sorting of non-spherical particles", "Powder Technol. (2018)", [
      "DEM of an inclined vibrating plate: non-spherical particles as super-ellipsoids, mixed 1:1 with spheres",
      "Vibration frequency & amplitude control the velocity distribution and discharge sequence of the mixture",
      "Effective separation when (2πf)²A ≈ 1.5g — a practical design rule for vibratory feeders",
    ]],
    ["Xiao et al. (2024) — measuring real scrap feeding", "CSAE 2024 (ACM)", [
      "Vision-based speed measurement of scrap on an inertial vibratory conveyor (SuperPoint feature-point extraction & matching)",
      "Works despite heterogeneous scrap types, sizes and stacking — no object tracking needed",
      "On-site application: measured speed curve matches the horizontal-vibrator frequency curve — an industrial validation pathway for our models",
    ]],
  ];
  return (
    <Shell kicker="Topic 1 — Particle-based modelling (DEM) & conveyor systems" title="Conveyor Belts & Vibratory Feeders: Mechanics at the Boundary" idx={4} smallTitle>
      <div className="row">
        {mini.map(([t, s], i) => (
          <div key={i} className="glass tint padded" style={{ flex: 1, padding: "12px 14px" }}>
            <div style={{ fontSize: 13.5, fontWeight: 800 }}>{t}</div>
            <div style={{ fontSize: 10.5, color: "var(--ink-soft)", marginTop: 4, lineHeight: 1.4 }}>{s}</div>
          </div>
        ))}
      </div>
      <div className="row grow" style={{ marginTop: 14 }}>
        <div className="col grow">
          {papers.slice(0, 2).map(([t, j, b], i) => (
            <div key={i} className="glass padded grow" style={{ padding: "13px 18px" }}>
              <div className="card-title" style={{ fontSize: 13.5 }}>{t}</div>
              <div className="card-sub" style={{ marginBottom: 6, fontSize: 11 }}>{j}</div>
              <ul className="b-list" style={{ gap: 4 }}>
                {(b as string[]).map((x, k) => (
                  <li key={k} style={{ fontSize: 11, lineHeight: 1.38 }}>{x}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
        <div className="col grow">
          {papers.slice(2).map(([t, j, b], i) => (
            <div key={i} className="glass padded grow" style={{ padding: "13px 18px" }}>
              <div className="card-title" style={{ fontSize: 13.5 }}>{t}</div>
              <div className="card-sub" style={{ marginBottom: 6, fontSize: 11 }}>{j}</div>
              <ul className="b-list" style={{ gap: 4 }}>
                {(b as string[]).map((x, k) => (
                  <li key={k} style={{ fontSize: 11, lineHeight: 1.38 }}>{x}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>
    </Shell>
  );
}

/* ---------------- slide 5 — frontier table ---------------- */
function Slide05() {
  const rows = [
    ["Lu et al. (2015) — Chem. Eng. Sci. 127 (review)", "Non-spherical DEM review: polyhedra, super-quadrics, multi-sphere, voxel, bonded", "Shape representation + contact detection; contact detection can cost >80% of CPU time", "No scrap-specific benchmark; generic granular systems"],
    ["Zhong et al. (2016) — Powder Technol. 300 (review)", "DEM / CFD-DEM review: AVM vs. immersed-family coupling", "No single best method; hybrid averaged + resolved strategies", "Generic particulate flows, not scrap handling"],
    ["Ahmed et al. (2026) — Powder Technol. (Tata Steel IJmuiden)", "Industrial BF charging: skip car → top hopper, actual plant geometry", "Plant-faithful DEM; ferrous-burden segregation lowers throat permeability", "Uniform BF burden (ore/sinter) — not heterogeneous EAF scrap"],
    ["Rossow & Coetzee (2021) — Powder Technol. 391", "Chevron belt + transfer chute, multi-sphere particles, high-speed validation", "Quantified DEM accuracy & upscaling limits (≤1.6×)", "Lab-scale corn grains, non-cohesive"],
    ["Schefler & Coetzee (2023) — Minerals 13:1501", "Cohesive material: belt → inclined impact plate", "Upscaled cohesive discharge: force & residual mass <15% error", "Lab-scale sand; single material"],
    ["You et al. (2018) — Powder Technol.", "Inclined vibrating plate, super-ellipsoids + spheres", "Frequency/amplitude → sorting & segregation; (2πf)²A ≈ 1.5g", "Lab-scale idealised shapes"],
    ["Chen et al. (2022) — Metall. Mater. Trans. B", "3D CFD of AC-EAF scrap melting, dual-cell + stack, NLMK 150-t EAF", "Melting, arc & burner physics well resolved and industrially validated", "Scrap enters as a lumped input — infeed dynamics not resolved"],
    ["Li, Provatas & Irons (2008) — AISTech", "Phase-field modelling of late melting in the EAF heel", "“Steel iceberg” formation dominates late melting; size, preheat & convection effects", "Post-charge physics — scrap assumed already in the furnace"],
  ];
  return (
    <Shell kicker="Topic 2 — Current state of the art & knowledge gaps" title="The Frontier of Research: Where the Literature Stands" idx={5} smallTitle>
      <table className="g-table">
        <thead>
          <tr>
            <th style={{ width: "24%" }}>Reference</th>
            <th style={{ width: "27%" }}>System &amp; method</th>
            <th style={{ width: "28%" }}>What it establishes</th>
            <th style={{ width: "21%" }}>Limitation for EAF scrap</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((r, i) => (
            <tr key={i}>
              <td>{r[0]}</td>
              <td>{r[1]}</td>
              <td>{r[2]}</td>
              <td className="gap">{r[3]}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <div className="band soft" style={{ marginTop: 10, fontSize: 12.5 }}>
        <b>Pattern:</b> DEM for conveyors/chutes is mature and validated — EAF CFD is mature and validated — the mechanical charging stage in between is the weak link.
      </div>
    </Shell>
  );
}

/* ---------------- slide 6 — knowledge gaps ---------------- */
function Slide06() {
  return (
    <Shell kicker="Topic 2 — Current state of the art & knowledge gaps" title="The Key Industry Knowledge Gaps" idx={6} smallTitle>
      <div className="row">
        <div className="glass tint padded grow">
          <div className="card-title">GAP 1 · Material heterogeneity</div>
          <p className="lead" style={{ fontSize: 12.5 }}>
            Heavy melting scrap (bundles up to metres, dense, low porosity) vs. shredded &amp; baled scrap (cm-scale, light, porous, high surface area). Multi-material recipes combine very different shape, size, bulk density and chemistry — <b>no particle-level model yet resolves the whole stream.</b>
          </p>
        </div>
        <div className="glass tint padded grow">
          <div className="card-title">GAP 2 · Real-time co-segregation in continuous feeding</div>
          <p className="lead" style={{ fontSize: 12.5 }}>
            How does heterogeneity segregate during vibratory feeding and chute transfer? If fine scrap blocks the chute or heavy bundles drop unpredictably, the charge layers unevenly → <b>thermal imbalances, energy spikes and late melting (“steel icebergs”)</b> in the EAF.
          </p>
        </div>
      </div>
      <div className="row" style={{ marginTop: 14 }}>
        {[
          ["Handling ↔ furnace coupling is missing", "Conveyor/chute DEM is mature; EAF CFD is mature; the interface between them is not yet built."],
          ["Industrial validation of charging dynamics is sparse", "Scrap flow in a running EAF is hard to observe directly; most DEM studies are validated on related lab materials."],
          ["Multiphysics at the charge surface", "Infeed scrap moves from mechanical handling to heating, oxidation, re-soldering and collapse — current models treat these separately."],
        ].map(([t, s], i) => (
          <div key={i} className="glass padded" style={{ flex: 1, padding: "14px 16px" }}>
            <div style={{ fontSize: 13, fontWeight: 800, marginBottom: 6 }}>{t}</div>
            <p className="lead" style={{ fontSize: 11.5 }}>{s}</p>
          </div>
        ))}
      </div>
      <div className="band" style={{ marginTop: 14, fontSize: 12.5 }}>
        <b>Bottom line from the literature:</b> treat scrap infeed as a coupled granular-transport problem — DEM particle mechanics for conveyor / chute / charging, handed off to a furnace model that resolves packing-dependent heat transfer and melting.
      </div>
    </Shell>
  );
}

/* ---------------- slide 7 — 4-year roadmap ---------------- */
function Slide07() {
  const years = [
    ["Y1 — Model development", [
      "Non-spherical DEM of scrap: multi-sphere & super-quadric proxies from 3D scans",
      "Baseline shape characterisation: size, shape, bulk density, porosity",
      "Lab calibration: angle of repose, drop & draw-down tests",
    ]],
    ["Y2 — Industrial calibration", [
      "Tata Steel NL plant data: feeders, chutes, recipes",
      "Build the virtual material library (bale / shredded / HMS)",
      "High-speed video & load-cell validation; upscaling limits at industrial scale",
    ]],
    ["Y3 — Optimisation scenarios", [
      "Multi-material recipe simulations in real plant geometry",
      "Segregation & discharge-sequence optimisation (which scrap goes first)",
      "Coupling with melting model: charge layering, HBI + scrap interaction",
    ]],
    ["Y4 — Plant implementation", [
      "Digital twin of the EAF infeed chain",
      "Actionable operating rules for plant engineers",
      "Wear & energy-reduction recommendations; dissemination & PhD defence",
    ]],
  ];
  return (
    <Shell kicker="Topic 3 — Methodology, novelty & anticipated challenges" title="Research Plan: The 4-Year Roadmap" idx={7} smallTitle>
      <div className="row grow">
        {years.map(([t, b], i) => (
          <div key={i} className="col" style={{ flex: 1 }}>
            <div className="year-head">{t as string}</div>
            <div className="glass padded grow" style={{ padding: "14px 16px" }}>
              <ul className="b-list" style={{ gap: 8 }}>
                {(b as string[]).map((x, k) => (
                  <li key={k} style={{ fontSize: 11.5, lineHeight: 1.42 }}>{x}</li>
                ))}
              </ul>
            </div>
          </div>
        ))}
      </div>
      <div className="band soft" style={{ marginTop: 14, fontSize: 12.5 }}>
        <b>Guiding principle:</b> every year ends in a validated artefact the plant can use — not just a simulation.
      </div>
    </Shell>
  );
}

/* ---------------- slide 8 — calibration strategy ---------------- */
function Slide08() {
  const steps = [
    ["STEP 1", "Physical experiments", "Angle of repose • drop / bounce (COR) • draw-down • feeder mass flow • high-speed video"],
    ["STEP 2", "Parameter optimisation loop", "Friction, rolling resistance, restitution, cohesion; PSD & multi-sphere fitting against bulk response"],
    ["STEP 3", "Calibrated DEM engine", "Altair EDEM / Ansys Rocky (commercial) • LIGGGHTS / MFIX-DEM (open source)"],
    ["STEP 4", "Industrial validation", "Chute flow, build-up, impact force & mass balance vs. plant data (Tata Steel NL)"],
  ];
  return (
    <Shell kicker="Topic 3 — Methodology, novelty & anticipated challenges" title="Calibration Strategy & the Coarse-Graining Dilemma" idx={8} smallTitle>
      <div className="row">
        {steps.map(([l, n, d], i) => (
          <div key={i} className="glass step-head" style={{ flex: 1 }}>
            <div className="lbl">{l}</div>
            <div className="name">{n}</div>
            <div className="desc">{d}</div>
          </div>
        ))}
      </div>
      <div className="row grow" style={{ marginTop: 14 }}>
        <div className="glass padded grow">
          <div className="card-title" style={{ fontSize: 14 }}>The coarse-graining dilemma</div>
          <ul className="b-list" style={{ gap: 7 }}>
            <li style={{ fontSize: 12 }}>Steel scrap piles span millimetres (shreds) to metres (HMS bundles) — simulating every fragment is computationally impossible</li>
            <li style={{ fontSize: 12 }}>Strategy: cluster small particles into representative numerical equivalents — volume-equivalent diameter, mass-matched multi-sphere clusters</li>
            <li style={{ fontSize: 12 }}>The virtual pile must match the real pile: angle of repose, stream thickness, build-up profile, discharge rate</li>
            <li style={{ fontSize: 12 }}>Calibrate rolling friction &amp; shape until the virtual scrap behaves like the physical material at every scale</li>
          </ul>
        </div>
        <div className="glass padded grow">
          <div className="card-title" style={{ fontSize: 14 }}>What the literature says about upscaling</div>
          <ul className="b-list" style={{ gap: 7 }}>
            <li style={{ fontSize: 12 }}>Rossow &amp; Coetzee (2021): scale factor ≤ 1.6 keeps errors ≤ 10% (build-up −9.2%, discharge −5.6%); wall effects negligible when container / particle ≥ 8–10 : 1</li>
            <li style={{ fontSize: 12 }}>Schefler &amp; Coetzee (2023): the maximum scale factor is a geometric property of the bulk measure of interest — and it increases with cohesion</li>
            <li style={{ fontSize: 12 }}>Implication: <span className="hl">calibrate per industrial quantity of interest (build-up, force, flow rate), not per particle</span></li>
            <li style={{ fontSize: 12 }}>Kryszak et al. (2020) / Kozicki &amp; Tejchman (2005): contact force spectra and grid-free methods give the validation toolbox for impact &amp; damage</li>
          </ul>
        </div>
      </div>
    </Shell>
  );
}

/* ---------------- slide 9 — novelty ---------------- */
function Slide09() {
  const cards = [
    ["Digital twin of EAF infeed", [
      "Scrap treated as a variable, uncertain feedstock — not a fixed input",
      "Multi-property particles: size, shape, bulk density, porosity, chemical heterogeneity (Cu, Cr …)",
      "Continuous chain: vibratory feeder → chute → charging, in real plant geometry",
    ]],
    ["Optimised discharge sequences", [
      "Predict which scrap discharges first under given vibration frequency / amplitude",
      "Avoid chute blockage, bridging and stagnant zones",
      "Smooth, continuous feeding — stable layers at the charge surface",
    ]],
    ["Reduced energy & wear", [
      "Fewer late-melting “steel icebergs” → shorter tapping delays (Li et al., 2008)",
      "Predict impact forces & liner wear on chutes and feeders",
      "Cheaper scrap recipes tested virtually before plant trials (HBI + scrap layering)",
    ]],
  ];
  return (
    <Shell kicker="Topic 3 — Methodology, novelty & anticipated challenges" title="Project Novelty & Expected Deliverables" idx={9} smallTitle>
      <div className="band" style={{ fontSize: 13.5, padding: "16px 22px" }}>
        <b>Core novelty:</b> a multi-scale, multi-property characterisation model that transforms raw Tata Steel data into a <b>dynamic digital twin of EAF scrap infeed</b> — multi-material recipes (bale, shredded, heavy melting scrap) moving through real industrial handling equipment.
      </div>
      <div className="row grow" style={{ marginTop: 16 }}>
        {cards.map(([t, b], i) => (
          <div key={i} className="glass padded grow" style={{ padding: "16px 18px" }}>
            <div className="card-title">{t as string}</div>
            <ul className="b-list" style={{ gap: 8 }}>
              {(b as string[]).map((x, k) => (
                <li key={k} style={{ fontSize: 12, lineHeight: 1.45 }}>{x}</li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </Shell>
  );
}

/* ---------------- slide 10 — technical alignment ---------------- */
function Slide10() {
  const rows = [
    ["Non-spherical DEM modelling — shape representation, contact detection, force & torque models", "Numerical programming in Python / C++; multi-sphere & super-quadric particle modelling; hands-on with Altair EDEM, Ansys Rocky, LIGGGHTS and MFIX-DEM (open source)"],
    ["Data integration — plant data into a digital twin", "Experience handling large data arrays; Python data pipelines (pandas / NumPy); statistical composition & uncertainty estimation for scrap recipes"],
    ["Experimental validation — physical boundary tests", "Angle-of-repose, drop/bounce and draw-down tests; feeder mass-flow tracking; high-speed video & PIV analysis of flow trajectories"],
    ["Industrial collaboration — from academia to the plant floor", "Translating dense academic results into clear, operational value for plant operations; structured project management of a 4-year industrial PhD"],
  ];
  return (
    <Shell kicker="Topic 4 — Reflection on personal skills & competencies" title="Technical Alignment with Project Requirements" idx={10} smallTitle>
      <table className="g-table">
        <thead>
          <tr>
            <th style={{ width: "42%" }}>Project requirement</th>
            <th style={{ width: "58%" }}>My toolkit</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((r, i) => (
            <tr key={i}>
              <td>{r[0]}</td>
              <td style={{ color: "var(--ink)" }}>{r[1]}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <div className="band soft" style={{ marginTop: 12, fontSize: 12.5 }}>
        <b>Simulation strategy:</b> commercial engines (EDEM, Rocky) for fast industrial delivery + open-source codes (LIGGGHTS, MFIX-DEM) for custom contact models, CFD-DEM coupling and cost control — validated the same way: physical experiments → bulk response → plant data.
      </div>
    </Shell>
  );
}

/* ---------------- slide 11 — collaboration ---------------- */
function Slide11() {
  return (
    <Shell kicker="Topic 4 — Reflection on personal skills & competencies" title="Communication & Collaborative Mindset" idx={11} smallTitle>
      <div className="row grow" style={{ alignItems: "stretch" }}>
        <div className="glass tint padded" style={{ flex: 1.05, display: "flex", flexDirection: "column", justifyContent: "center" }}>
          <div className="card-title" style={{ fontSize: 16 }}>TU Delft — Academic research</div>
          <ul className="b-list" style={{ gap: 8 }}>
            <li style={{ fontSize: 12.5 }}>DEM / CFD-DEM theory for non-spherical particles</li>
            <li style={{ fontSize: 12.5 }}>Rigorous validation science: lab experiments, uncertainty, upscaling</li>
            <li style={{ fontSize: 12.5 }}>Publication track record (international conferences &amp; journals)</li>
          </ul>
        </div>
        <div style={{ display: "flex", alignItems: "center" }}>
          <div className="pill" style={{ flexDirection: "column", alignItems: "center", gap: 6, padding: "16px 20px", textAlign: "center", background: "var(--liquid)", color: "#fff", borderColor: "rgba(255,255,255,0.5)" }}>
            <span style={{ fontSize: 10, fontWeight: 800, letterSpacing: "0.14em" }}>THIS PHD PROJECT</span>
            <span style={{ fontSize: 12, fontWeight: 600, lineHeight: 1.4 }}>particle-based digital twin of scrap handling</span>
          </div>
        </div>
        <div className="glass tint padded" style={{ flex: 1.15, display: "flex", flexDirection: "column", justifyContent: "center" }}>
          <div className="card-title" style={{ fontSize: 16 }}>Tata Steel Netherlands — Industry</div>
          <ul className="b-list" style={{ gap: 8 }}>
            <li style={{ fontSize: 12.5 }}>IJmuiden plant data, access &amp; operational constraints</li>
            <li style={{ fontSize: 12.5 }}>HBI + scrap recipes for green (hydrogen-based) steel production</li>
            <li style={{ fontSize: 12.5 }}>Plant engineers as co-developers of the digital twin</li>
          </ul>
        </div>
      </div>
      <div className="glass strong padded" style={{ marginTop: 16 }}>
        <p className="lead" style={{ fontSize: 13.5, lineHeight: 1.6, color: "var(--ink)" }}>
          I pride myself on being able to translate dense academic data into clear, operational value for plant operations. I am eager to collaborate directly with industrial engineers in the Netherlands — gathering on-site data, co-designing validation campaigns, and ensuring the doctoral research delivers practical, bottom-line improvements to the steelmaking process.
        </p>
      </div>
    </Shell>
  );
}

/* ---------------- slide 12 — closing ---------------- */
function Slide12() {
  const rows = [
    ["Theory", "DEM with realistic non-spherical representation (multi-sphere / super-quadric / polyhedra) is the right tool for scrap handling — shape is physics, not decoration."],
    ["Gap", "Charging/infeed is the weak link: conveyor DEM and EAF melting CFD are both mature; the mechanical, heterogeneous, real-time charging stage is not yet modelled."],
    ["Plan", "Coarse-graining + industrial calibration turns the gap into a validated digital twin of EAF infeed — optimised sequences, less wear, less energy."],
  ];
  return (
    <Shell kicker="Closing" title="Conclusion & Q&A" idx={12} smallTitle>
      <div className="col grow" style={{ gap: 14, justifyContent: "center" }}>
        {rows.map(([l, t], i) => (
          <div key={i} className="glass padded" style={{ display: "flex", alignItems: "center", gap: 20, padding: "14px 20px" }}>
            <span className="chip" style={{ width: "auto", height: "auto", padding: "8px 16px", borderRadius: 999, fontSize: 12.5, letterSpacing: "0.06em" }}>{l}</span>
            <div style={{ fontSize: 13.5, lineHeight: 1.45 }}>{t}</div>
          </div>
        ))}
        <div style={{ textAlign: "center", padding: "10px 40px" }}>
          <div className="close-line">Developing the next generation of particle models for sustainable, efficient EAF steel production.</div>
          <p className="thanks" style={{ marginTop: 14 }}>
            Thank you for your time — I welcome your questions.<br />
            <b>Kevin Tongue</b>  •  tonguekevin00@gmail.com
          </p>
        </div>
      </div>
    </Shell>
  );
}

/* ---------------- slide 13 — references ---------------- */
function Slide13() {
  const left = [
    "[1]  Lu G., Third J.R., Müller C.R. (2015). Discrete element models for non-spherical particle systems: from theoretical developments to applications. Chemical Engineering Science 127: 425–465.",
    "[2]  Zhong W., Yu A., Liu X., Tong Z., Zhang H. (2016). DEM/CFD-DEM modelling of non-spherical particulate systems: theoretical developments and applications. Powder Technology 300: 109–127.",
    "[3]  Rossow J., Coetzee C.J. (2021). Discrete element modelling of a chevron patterned conveyor belt and a transfer chute. Powder Technology 391: 77–96.",
    "[4]  Schefler O.C., Coetzee C.J. (2023). Discrete element modelling of a bulk cohesive material discharging from a conveyor belt onto an impact plate. Minerals 13(12): 1501.",
    "[5]  You Y., Liu M., Ma H., Xu L., Liu B., Shao Y., Tang Y., Zhao Y. (2018). Investigation of the vibration sorting of non-spherical particles based on DEM simulation. Powder Technology. doi:10.1016/j.powtec.2017.11.002.",
    "[6]  Xiao X., Zhong X., Ma M., Wu X. (2024). A visual based algorithm for measuring the speed of scrap metal vibration feeding. CSAE 2024 (ACM). doi:10.1145/3704814.3704817.",
    "[7]  Chen Y., Ryan S., Silaen A.K., Zhou C.Q. (2022). Simulation of scrap melting process in an AC electric arc furnace: CFD model development and experimental validation. Metallurgical and Materials Transactions B 53: 3256–3272.",
  ];
  const right = [
    "[8]  Li J., Provatas N., Irons G.A. (2008). Modelling of late melting of scrap in an EAF. AISTech 2008, Irons A8046.",
    "[9]  Kryszak D., Bartoszewicz A., Szufa S., Piersa P., Obraniak A., Olejnik T.P. (2020). Modelling of transport of loose products with the use of the non-grid method of discrete elements (DEM). Processes 8(11): 1489.",
    "[10]  Garg R., Galvin J., Li T., Pannala S. (2012). Documentation of open-source MFIX-DEM software for gas-solids flows. National Energy Technology Laboratory / Oak Ridge National Laboratory.",
    "[11]  Kozicki J., Tejchman J. (2005). Application of a cellular automaton to simulations of granular flow in silos. Granular Matter 7: 45–54.",
    "[12]  Ahmed H., Pang Y., Adema A., et al. (2026). Industrial-scale DEM modelling of segregation in the blast furnace charging system (Tata Steel IJmuiden). Powder Technology.",
    "[13]  Guo D., Irons G.A. (2008). Modelling of steel scrap movement. Applied Mathematical Modelling. doi:10.1016/j.apm.2007.06.037.",
    "[14]  Ugarte O., Li J., Haeberle J., et al. (2024). CFD modelling of HBI/scrap melting in industrial EAF and the impact of charge layering on melting performance. Materials 17(21): 5139.",
  ];
  return (
    <Shell kicker="Supporting literature" title="References" idx={13} smallTitle>
      <div className="refs">
        <div className="glass padded ref-col">{left.map((r, i) => <p key={i}>{r}</p>)}</div>
        <div className="glass padded ref-col">{right.map((r, i) => <p key={i}>{r}</p>)}</div>
      </div>
    </Shell>
  );
}

/* ---------------- registry ---------------- */
export interface SlideDef {
  id: string;
  label: string;
  kicker: string;
  component: () => ReactNode;
}

export const SLIDES: SlideDef[] = [
  { id: "title", label: "PhD Thesis — Scrap Handling for Green Steel", kicker: "Title", component: () => <Slide01 /> },
  { id: "agenda", label: "Agenda", kicker: "Agenda", component: () => <Slide02 /> },
  { id: "dem-basics", label: "DEM Fundamentals & Shape Representation", kicker: "Topic 1", component: () => <Slide03 /> },
  { id: "conveyors", label: "Conveyor Belts & Vibratory Feeders", kicker: "Topic 1", component: () => <Slide04 /> },
  { id: "frontier", label: "The Frontier of Research", kicker: "Topic 2", component: () => <Slide05 /> },
  { id: "gaps", label: "The Key Industry Knowledge Gaps", kicker: "Topic 2", component: () => <Slide06 /> },
  { id: "roadmap", label: "Research Plan: The 4-Year Roadmap", kicker: "Topic 3", component: () => <Slide07 /> },
  { id: "calibration", label: "Calibration & the Coarse-Graining Dilemma", kicker: "Topic 3", component: () => <Slide08 /> },
  { id: "novelty", label: "Project Novelty & Expected Deliverables", kicker: "Topic 3", component: () => <Slide09 /> },
  { id: "toolkit", label: "Technical Alignment", kicker: "Topic 4", component: () => <Slide10 /> },
  { id: "collab", label: "Communication & Collaborative Mindset", kicker: "Topic 4", component: () => <Slide11 /> },
  { id: "closing", label: "Conclusion & Q&A", kicker: "Closing", component: () => <Slide12 /> },
  { id: "references", label: "References", kicker: "Supporting literature", component: () => <Slide13 /> },
];
