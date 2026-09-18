To deliver a highly compelling 15-minute PhD interview presentation, your academic literature must bridge the gap between abstract granular physics and the highly harsh, chaotic reality of steel plant scrap yards.
Because your project is backed by Tata Steel Netherlands, demonstrating a command of industrially calibrated simulations will separate you from candidates who only understand idealized spherical particles. [1] 
------------------------------
## Topic 1: The Theory of Particle-Based Models (DEM) & Conveyor Systems
These papers establish your core fundamental mechanics. They show you understand contact force laws and how to efficiently simulate bulk material tracking across moving boundaries.

* 
* The Core Mathematical Framework (DEM Basics & Shape Representation):
* Proposed Reading: "DEM/CFD-DEM Modelling of Non-Spherical Particulate Systems: Theoretical Developments and Applications" by Zhou et al.
   * Why you need it: This paper outlines how to mathematically represent non-spherical particles (via Multi-Sphere clusters, polyhedra, or superquadrics) and handle complex contact-detection mechanics. Scrap is never round; you must show you understand the heavy computational tradeoffs of non-spherical shapes. [2, 3, 4, 5] 
* Kinematics of Conveyor Belts & Chute Transfers:
* Proposed Reading: "Discrete Element Modelling of a Bulk Cohesive Material Discharging from a Belt Conveyor onto an Inclined Impact Plate" by Hastie.
   * Why you need it: This covers the precise tracking of material velocity, preferential wear on chute linings, and avoiding stagnation zones during belt discharge—perfect for mapping continuous furnace infeed. [6, 7] 
* Vibratory Feeders & Discharging Mechanics:
* Proposed Reading: "Investigation of the Vibration Sorting of Non-Spherical Particles Based on DEM Simulation" by Jiang et al.
   * Why you need it: Vibratory feeders induce highly dynamic contact friction and segregation. This text helps you explain how vibration frequencies and amplitudes change the velocity distribution and discharge sequences of heterogeneous material streams. [8, 9] 
* 

------------------------------
## Topic 2: Current State of the Art & Knowledge Gaps in Scrap/EAF Modelling
These references establish the absolute frontier of your field and highlight exactly what the academic community hasn't solved yet.

| Focus Area | State-of-the-Art Source | Critical Knowledge Gap to Highlight |
|---|---|---|
| Industrial Co-segregation & Charging Geometry | "Industrial Multi-Component Segregation in the Blast Furnace Charging Process Using Actual Plant Geometry... at Tata Steel IJmuiden" by dynamic researchers (ScienceDirect). | Existing models usually handle uniform raw materials (like iron ore pellets). There is an immense gap in applying this rigorous plant-geometry framework to highly chaotic, large-scale steel scrap. |
| Scrap Chute Behavior & Calibration | "Experimental and Discrete Element Method Analysis of Galvanized Steel Scrap Particles Along and After an Inclined Chute" (ResearchGate). | Most EAF models focus heavily on the thermal/CFD chemistry inside the furnace rather than the mechanical, physical flow tracking of scrap during the continuous feeding process before it melts. |
| Material Heterogeneity & Chemical Analytics | "Modeling Scrap Composition in Electric Arc and Basic Oxygen Furnace Processes" (arXiv). | Current plant models rely on post-facto statistical mass balances or statistical AI. There is a failure to link physical particle tracking (size, shape, bulk density) directly with real-time spatial distribution tracking during continuous infeed. |

------------------------------
## Topic 3: Methodology, Novelty, & Anticipated Challenges
Use these concepts to structurally defend your proposed 4-year research plan.

* 
* The Calibration Challenge (The "Coarse-Graining" Dilemma):
* Proposed Reading: "Optimization of Discrete Element Method Model to Obtain Stable and Reliable Numerical Results of Mechanical Response of Granular Materials" (MDPI).
   * Why you need it: Steel scrap piles can vary from millimeters to meters. Simulating every single tiny scrap particle is computationally impossible. You must explain your methodology for coarse-graining / upscaling the particles while using angle-of-repose physical experiments to validate the virtual model's accuracy. [4, 6, 10, 11] 
* The Core Novelty of Your Project:
* Your novelty is creating a multi-scale, multi-property characterization model that transforms raw data from Tata Steel into a dynamic digital twin. You aren't just simulating generic rocks; you are simulating multi-material recipes (bale scrap, shredded scrap, heavy melting scrap) moving in real industrial environments. [1, 12, 13] 
* 

------------------------------
## Topic 4: Reflection on Your Personal Skills & Competencies
To make yourself look like the ideal candidate, reference these software tools and validation workflows in your slides.

* 
* Software Literacy: Mention your interest or experience with industrial particle-simulation engines like [Altair EDEM](https://www.altair.com/edem/), Ansys Rocky, or open-source codes like LIGGGHTS. [14, 15, 16, 17, 18] 
* Data Integration & Experimental Validation: Emphasize that you have the skills to execute physical boundary validations (e.g., dropping tests, tilting boxes, or tracking feeder mass flow rates) to ensure the numerical code mirrors the true physical mechanics at Tata Steel. [15, 19] 
* 

------------------------------
To help me tailor this explicitly to your slide deck, could you tell me:

   1. What programming languages or simulation tools (like Python, MATLAB, DEM software) do you have experience with?
   2. What is your academic background (e.g., Mechanical Engineering, Metallurgy, Physics)?

With that info, I can generate a slide-by-slide script for your 15 minutes!

[1] [https://www.sciencedirect.com](https://www.sciencedirect.com/science/article/pii/S0032591026000045)
[2] [https://era.ed.ac.uk](https://era.ed.ac.uk/handle/1842/41915)
[3] [https://www.researchgate.net](https://www.researchgate.net/publication/305077659_DEMCFD-DEM_Modelling_of_Non-spherical_Particulate_Systems_Theoretical_Developments_and_Applications)
[4] [https://www.scielo.br](https://www.scielo.br/j/remi/a/yWyJTLJSjn6HHXCWRTSx6Vf/?lang=en)
[5] [https://www.researchgate.net](https://www.researchgate.net/publication/334751569_NURBS-based_DEM_for_non-spherical_particles)
[6] [https://www.mdpi.com](https://www.mdpi.com/2075-163X/13/12/1501)
[7] [https://ro.uow.edu.au](https://ro.uow.edu.au/ndownloader/files/50445729)
[8] [https://www.researchgate.net](https://www.researchgate.net/publication/320907288_Investigation_of_the_vibration_sorting_of_non-spherical_particles_based_on_DEM_simulation)
[9] [https://www.nature.com](https://www.nature.com/articles/s41598-021-96111-2)
[10] [https://www.mdpi.com](https://www.mdpi.com/2075-163X/14/8/758)
[11] [https://www.researchgate.net](https://www.researchgate.net/publication/289779904_Simulation_of_handling_impact_load_of_bulk_material_by_DEM_method)
[12] [https://www.sciencedirect.com](https://www.sciencedirect.com/science/article/abs/pii/S0967066107000044)
[13] [https://www.mdpi.com](https://www.mdpi.com/1996-1944/17/21/5139)
[14] [https://www.researchgate.net](https://www.researchgate.net/publication/329615098_Mixing_study_of_non-spherical_particles_using_DEM)
[15] [https://openscholarship.wustl.edu](https://openscholarship.wustl.edu/eng_etds/1148/)
[16] [https://www.youtube.com](https://www.youtube.com/watch?v=gvGBVHtmsPs&t=33)
[17] [https://www.youtube.com](https://www.youtube.com/watch?v=49qBqDj2Ms8)
[18] [https://www.cfdem.com](https://www.cfdem.com/conveyor-model)
[19] [https://www.youtube.com](https://www.youtube.com/watch?v=XeIohf4GAuE)
