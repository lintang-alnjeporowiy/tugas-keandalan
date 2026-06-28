# Implementation Plan: 3-Component Dynamic Wave Bending Moment combination

This plan outlines the design and implementation details for updating the ship reliability calculations to combine the three wave bending moment components (vertical, horizontal, torsional) using the correlation-based Turkstra's Rule described in `penggabungan-beban.md`.

## Proposed Load Combination Formulation

### 1. Dominant and Secondary Components
For each wave case, we define the three components from the CSV file:
- **Head Wave ($D = 180^\circ$)**:
  - Dominant load ($f_1$): `Momen Vertikal (N.m)`
  - Secondary load ($f_2$): `Momen Horizontal (N.m)`
  - Tertiary load ($f_3$): `Momen Torsional (N.m)`
- **Beam Wave ($D = 90^\circ$)**:
  - Dominant load ($f_1$): `Momen Horizontal (N.m)`
  - Secondary load ($f_2$): `Momen Vertikal (N.m)`
  - Tertiary load ($f_3$): `Momen Torsional (N.m)`

### 2. Combination Factors (Turkstra's Rule)
We calculate the correlation coefficients $\rho_{12}$ and $\rho_{13}$ based on the raw time-series data:
$$\rho_{12} = \text{correlation}(f_1, f_2)$$
$$\rho_{13} = \text{correlation}(f_1, f_3)$$

To ensure that the combined dynamic wave bending moment is always additive and physically realistic, we define the combination factors using the absolute values of the correlation coefficients:
$$K_2 = |\rho_{12}|$$
$$K_3 = |\rho_{13}|$$

> [!NOTE]
> Using the absolute value $K = |\rho|$ is standard in structural engineering for envelopes of absolute responses, preventing negative combination factors from non-physically subtracting dynamic contributions when there is a negative correlation.

### 3. Combined Dynamic Moment
The combined dynamic wave bending moment at each time step $t$ is calculated as:
$$WBM_{\text{dynamic}}(t) = |f_1(t)| + K_2 |f_2(t)| + K_3 |f_3(t)|$$

### 4. Combined Total Bending Moment
The total vertical bending moment ($VBM_{\text{total}}$) is then:
$$VBM_{\text{total}}(t) = WBM_{\text{dynamic}}(t) + |SWBM_{\text{static\_max, vertical}}| + swbm\_ship$$
where:
- $|SWBM_{\text{static\_max, vertical}}| = 1.5464 \times 10^8$ N.m (the absolute maximum static vertical bending moment from `SWBM.csv`).
- $swbm\_ship = 1.2000 \times 10^8$ N.m (the constant ship vertical SWBM).

---

## User Review Required

> [!IMPORTANT]
> **Use of Absolute Correlation Factors $K = |\rho|$**
> We propose using $K_2 = |\rho_{12}|$ and $K_3 = |\rho_{13}|$. If we used the signed correlation coefficient, the negative correlation for the torsional moment ($\rho_{13} \approx -0.30$) in beam waves would result in subtracting the torsional contribution, which is non-conservative and can lead to unphysical negative combined moments when the horizontal moment is small. Please let us know if you agree with using the absolute value $|\rho|$ for these factors.

---

## Proposed Changes

### Python Scripts & Notebooks

#### [MODIFY] [generate_notebook.py](file:///home/lintang/.gemini/antigravity/brain/e43c3a4c-a1c1-4334-b829-e3f5b0e99580/scratch/generate_notebook.py)
Update the programmatical notebook builder to construct `main.ipynb` with the new load combination:
1. **Section 1: Load Analysis**:
   - In cell `load-stats`, load all three components of the wave bending moment for each file.
   - Calculate $\rho_{12}$ and $\rho_{13}$ using `np.corrcoef`.
   - Calculate the combined $VBM_{\text{total}}$ using the 3-component formula.
   - Display a table of the calculated correlation coefficients ($\rho_{12}, \rho_{13}$) and combination factors ($K_2, K_3$) for each of the 6 wave files.
   - Plot time-series (3x2 grid of subplots) of the combined $VBM_{\text{total}}$ and its components.
2. **Section 3: Reliability Analysis**:
   - Update the reliability loop cells for both Ultimate and Yield strength cases to use the new load statistics (mean and corrected standard deviation).

---

## Verification Plan

### Automated Tests
- Run `generate_notebook.py` to compile `main.ipynb`.
- Execute `main.ipynb` using `jupyter nbconvert --to notebook --execute --inplace main.ipynb` to verify that all cells run without error and outputs are embedded.
