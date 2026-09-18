# Chat Transcript: Non\-spherical particle DEM

## User

give me in this paper all dem methods for handling non-spherical particles and describe them and then make a comparison

## Aurelle

The paper organizes non-spherical DEM into **single-particle representations**, **composite-particle representations**, and **coupled CFD–DEM schemes**. The central difficulty is that particle representation determines how accurately and efficiently contacts, forces, rotations, and fluid interactions can be computed; contact detection alone can consume more than 80% of the computational time. 

## 1. Single-particle representation methods

In a single-particle method, each non-spherical particle is represented directly as one geometric object rather than as a cluster of simpler particles.

### 1.1 Polygonal and polyhedral particles

In two dimensions, particles are represented by **polygons**; in three dimensions, by **polyhedra** consisting of vertices, edges, and faces. The particle geometry is stored explicitly, usually relative to its center of mass, together with the outward normal of each face. 

The most prominent contact technique for polyhedral particles is the **common-plane method**. A plane is constructed between two contacting particles so that the contact problem is reduced to a corner-to-plane calculation. The normal contact force is taken along the direction perpendicular to this common plane. Several algorithms can be used to locate the plane, including the conventional iterative algorithm, fast common plane, quick updating, and shortest-link methods. 

**Advantages**

- Represents angular particles, sharp corners, and flat faces directly.
- Suitable for rocks, soil grains, ballast, and other inherently angular particles.
- Provides physically meaningful face- and edge-based contacts.

**Limitations**

- Smooth shapes require many vertices, edges, and faces.
- Increasing geometric resolution greatly increases contact-detection cost.
- Contact configurations such as vertex–edge, edge–edge, and face–face can be cumbersome to classify.

The paper therefore considers polyhedral representation particularly appropriate for naturally angular materials, but less attractive for smooth particles. 

### 1.2 Continuous-function representation

The **continuous-function representation (CFR)** describes a particle surface implicitly through a mathematical function. The paper discusses ellipses, ellipsoids, two-dimensional superquadrics, and three-dimensional superquadrics. Superquadrics can represent particles ranging from relatively rounded to more block-like forms by changing their semi-axes and squareness parameters. 

Contact can be computed directly by solving for the intersection of two implicit surfaces, either analytically or iteratively. However, these nonlinear calculations can become very expensive, especially for three-dimensional particles or particles with high squareness. Indirect methods include the geometric-potential method and common-normal algorithms. 

**Advantages**

- Represents smooth, convex, and systematically shape-controlled particles well.
- Provides a compact mathematical description.
- Allows aspect ratio and surface squareness to be varied continuously.
- Offers a good compromise between geometric flexibility and computational cost for superquadric particles.

**Limitations**

- Standard superquadrics are mainly suitable for symmetric or regular shapes.
- Arbitrary irregular particles are difficult to represent.
- Direct contact calculations are nonlinear and expensive.
- Contact normals may contain numerical errors.

The paper notes that CFR is effective for regular smooth particles but is weak for particles with sharp edges and flat faces. 

### 1.3 Discrete-function representation

The **discrete-function representation (DFR)** describes a particle surface using a collection of discrete nodes. During contact detection, nodes belonging to one particle are transformed into the coordinate system of the other particle, and an inside/outside test is performed. 

**Advantages**

- Can describe relatively complex particle surfaces.
- Uses a direct geometric inside/outside test.
- Is more flexible than a simple analytical shape function.

**Limitations**

- Accuracy depends strongly on the number and distribution of surface nodes.
- The calculated contact normal is usually an average approximation rather than the exact normal.
- Efficiency decreases for particles with large aspect ratios. 

### 1.4 Virtual-space or digitized-particle method

The **virtual-space method** digitizes space into cells: pixels in two dimensions or voxels in three dimensions. A particle is represented as a connected group of occupied cells. Real particle shapes can be obtained directly from 3D optical or X-ray scans. 

Contact detection becomes a cell-overlap problem: two particles are in contact or overlap when they occupy the same discrete locations. The approach can also be combined with orientation-discretization databases. 

**Advantages**

- Can reproduce highly irregular shapes directly from scans.
- Contact detection is conceptually simple.
- Computational cost is tied mainly to the number of occupied cells rather than to complicated geometric intersection formulas.

**Limitations**

- Accuracy is limited by grid resolution.
- Particle movement and orientation are effectively discretized.
- High resolution requires many pixels or voxels and therefore substantial memory and computation.
- Smooth surfaces become stair-stepped.

### 1.5 Combined geometric-element method

The **combined geometric-element method** constructs one particle from several different geometric surface elements, such as planar surfaces, curved surfaces, edges, and vertices. It is useful for regular particles that contain both smooth and sharp features—for example, cylinders, hollow cylinders, sphero-cylinders, and bi-convex tablets. 

For a cylinder, for example, the surface consists of one curved cylindrical part and two flat ends. The contact algorithm must nevertheless handle multiple contact types, including vertex–edge, edge–edge, edge–face, and face–face contacts. A coarse search using circumscribing spheres or boxes can be applied before the detailed contact test to improve efficiency. 

**Advantages**

- Represents mixed smooth/angular geometry better than pure polyhedra or pure analytical functions.
- Particularly suitable for cylinders, tablets, and other engineered shapes.
- Can preserve important geometric features.

**Limitations**

- Requires many geometric data to be stored and updated.
- Has many possible contact configurations.
- More expensive than sphere-based contact detection.
- Usually works best for a limited family of known geometries rather than arbitrary scanned particles.

## 2. Composite-particle methods

Composite methods approximate one non-spherical particle using multiple simpler elements. The elements are treated together as a rigid or deformable composite body.

### 2.1 Multi-sphere model

The **multi-sphere model (MSM)** approximates an arbitrary particle using overlapping spheres of different sizes and positions. Once assembled, the relative positions of the spheres remain fixed, so the cluster moves as a rigid body. Its main computational advantage is that it reuses the well-established sphere–sphere contact algorithm. 

The model has been applied to gravel, biomass, pharmaceutical tablets, industrial particles, and mixtures of particles with very different shapes. 

**Advantages**

- Simple and robust contact detection.
- Easy to combine with existing spherical DEM codes.
- Convenient for mixtures of spheres and non-spherical particles.
- Suitable for practical engineering simulations and large particle systems.
- Flexible enough to approximate many elongated or irregular shapes.

**Limitations**

- Selecting the number, size, and location of spheres is difficult.
- The surface can become artificially “knobbly.”
- Accurate shape reproduction may require many spheres.
- Increasing the number of spheres reduces computational efficiency.
- The composite mass distribution and moment of inertia may be inaccurate.
- Applicability is often limited to relatively simple particle shapes. 

Several sphere-generation strategies are mentioned, including optimized clustering, dynamic methods, four-point sphere fitting, sphere growing, and modified greedy heuristic algorithms.

### 2.2 Bonded-particle model

The **bonded-particle model** joins spheres or other discrete elements using bonds. Unlike a rigid multi-sphere cluster, the elements can move relative to one another when the bonds deform or break. This allows the composite particle to be flexible or breakable. 

**Advantages**

- Can represent fracture, breakage, and deformation.
- Suitable for cohesive or internally structured particles.
- Retains the relatively simple contact treatment of the constituent elements.

**Limitations**

- Requires calibration of bond stiffness, strength, damping, and failure behavior.
- The internal structure may depend strongly on how the elements are arranged.
- More computationally demanding than a rigid multi-sphere particle.
- It is not primarily intended for perfectly rigid particles.

## 3. Other particle representations

The paper also lists several less conventional methods:

- **Racetrack particles**
- **Potential particles**
- **Minkowski particles**
- **Boolean particles**

These are presented as promising alternatives, but the review does not develop them to the same level of detail as polyhedra, superquadrics, digitized particles, or multi-sphere clusters. The paper emphasizes that most representation methods have a preferred application range rather than being universally effective. 

The paper also mentions more general contact-detection strategies that can potentially work across different shape representations:

- Probability-based contact algorithms.
- GJK-based contact detection.
- Orientation-discretization database methods.

These are **contact algorithms**, not independent particle-shape representations. Their purpose is to reduce the dependence between the selected shape description and the contact-resolution procedure.

## 4. Contact-force treatment for non-spherical particles

Representation and contact detection determine where contact occurs; a separate issue is how to calculate the force once contact has been detected.

For spherical DEM, contact models commonly use the overlap distance to calculate normal and tangential forces. For non-spherical particles, force calculation is more difficult because the force depends not only on overlap magnitude but also on the overlap area or volume, contact geometry, contact normal, and reference contact point. 

The paper groups elastic normal-force models into:

1. **Linear models**
2. **Nonlinear models**
3. **Hysteresis models**
4. **Continuous-interaction or short-range-force models**

Dissipation is generally introduced through a viscous or damping force. Tangential forces use either complex local models or global history-dependent models involving tangential displacement, friction, and energy dissipation. 

For multi-sphere particles, the usual strategy is to apply standard sphere–sphere contact laws to each pair of constituent spheres. This is computationally convenient, but it means that the resulting particle force and torque depend on the quality of the sphere assembly. 

## 5. Rotational treatment

All DEM methods must track both translation and rotation. For generic non-spherical particles, the moment of inertia changes in the laboratory frame as the particle rotates. The paper therefore distinguishes between:

- A **space-fixed coordinate system**, attached to the laboratory.
- A **body-fixed coordinate system**, attached to the particle and aligned with its principal axes.

The rotational equations are handled using the inertia tensor and a transformation between these coordinate systems. 

For single-particle representations, orientation can be described using Euler angles or quaternions. For multi-sphere particles, the orientation of the rigid sphere cluster is updated as a composite body. 

## 6. CFD–DEM methods for non-spherical particles

When fluid flow is included, the paper describes two broad coupling families.

### 6.1 Averaged Volume Method

In the **Averaged Volume Method (AVM)**, several particles occupy a CFD cell. Fluid–particle forces are estimated using empirical correlations for quantities such as drag, lift, and voidage. The method is computationally convenient and can handle many particles, but it does not resolve the actual particle geometry in detail. 

For non-spherical particles, the drag coefficient may depend on sphericity, projected area, aspect ratio, orientation, and Reynolds number. Applying spherical-particle correlations directly can produce substantial errors; the paper specifically notes that even the commonly used Ergun equation may deviate significantly for non-spherical particles. 

### 6.2 Immersed Family Methods

In **Immersed Family Methods (IFM)**, the particle is resolved within the surrounding fluid mesh. This family includes:

- Immersed boundary methods.
- Direct numerical simulation.

IFM can provide detailed information near the particle surface and can better capture shape-dependent fluid forces. However, the computational cost is much higher, so it is generally more appropriate for small-scale or fundamental studies. 

In DNS, fluid and boundary nodes are distinguished, the local velocity and stress near the particle surface are calculated, and the hydrodynamic force is obtained by integrating the stress over the particle boundary. This allows the actual shape and surface force distribution to be resolved. 

## 7. Comparison of the main methods

| Method | Shape fidelity | Irregular shapes | Smooth shapes | Contact cost | Best use | Main weakness |
|---|---:|---:|---:|---:|---|---|
| Polygon/polyhedron | High for angular particles | High for convex angular shapes | Low unless highly refined | High | Rocks, soil, ballast, angular grains | Expensive for smooth surfaces and many contact types |
| Continuous function / superquadric | High for regular smooth shapes | Low to moderate | High | Moderate to high | Ellipsoids, rounded particles, controlled aspect ratios | Poor for arbitrary irregular and sharp-edged particles |
| Discrete-function representation | Moderate to high | Moderate to high | Moderate | Moderate | Complex surfaces represented by nodes | Accuracy depends on node density and placement |
| Virtual-space / voxel method | Depends on grid resolution | Very high | Moderate | Potentially low per test, but memory-heavy | Scanned particles and arbitrary geometries | Grid discretization, stair-step surfaces, memory cost |
| Combined geometric elements | High for mixed smooth/angular shapes | Moderate | High | High | Cylinders, tablets, engineered particles | Many special contact cases |
| Multi-sphere model | Moderate; approximation-based | Moderate | Moderate | Low to moderate | Large engineering simulations and mixed-shape systems | Knobbly surfaces, inaccurate inertia, sphere-generation problem |
| Bonded-particle model | Moderate; assembly-based | High for breakable bodies | Moderate | Moderate to high | Fracture, deformation, breakage | Requires bond calibration and increases model complexity |
| Racetrack/potential/Minkowski/Boolean | Varies by method | Potentially high | Potentially high | Not established uniformly in this review | Specialized applications | Less mature and less comprehensively validated in the paper |
| AVM–CFD–DEM | Shape effects represented through correlations | Moderate | Moderate | Lowest CFD cost | Large, dense industrial systems | Does not resolve local flow around the particle |
| IFM–CFD–DEM / DNS | Very high | High | High | Very high | Small-scale, detailed fluid–particle studies | Computationally expensive and difficult to scale |

## 8. Overall assessment

The paper’s main conclusion is that **no single DEM method is best for every non-spherical particulate system**.

- Choose **polyhedra** when sharp edges and angular contacts are essential.
- Choose **superquadrics or other continuous functions** for smooth, regular particles whose aspect ratio and roundness must be varied.
- Choose **multi-sphere particles** when computational robustness, implementation simplicity, and large-scale simulation are more important than exact surface fidelity.
- Choose **voxel or discrete representations** when the actual irregular shape comes from particle scans.
- Choose **bonded particles** when fracture, deformation, or breakage must be modeled.
- Use **AVM–CFD–DEM** for large dense multiphase systems and **IFM/DNS** when resolving detailed fluid forces around individual particles is more important than scale.

The most promising practical direction identified by the paper is a **hybrid strategy**: use efficient averaged-volume coupling for much of a large system while applying more detailed immersed or resolved methods where particle-scale fluid information is needed. The authors also identify generalized contact detection, improved non-spherical force models, parallel computation, and shape-dependent heat-transfer models as important future developments.