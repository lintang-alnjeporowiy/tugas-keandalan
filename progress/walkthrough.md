# Walkthrough - Ship Structural Reliability Analysis (3-Component Dynamic Load Cases)

We have successfully updated the ship structural reliability analysis to combine the three wave bending moment components (vertical, horizontal, torsional) using the correlation-based Turkstra's Rule.

## 🚀 Key Accomplishments

1. **3-Component Dynamic Wave Load Combination**:
   - For head wave ($180^\circ$), the dominant component is vertical wave bending moment.
   - For beam wave ($90^\circ$), the dominant component is horizontal wave bending moment.
   - Secondary and tertiary components are combined using correlation factors:
     $$WBM_{\text{dynamic}}(t) = |f_1(t)| + K_2 |f_2(t)| + K_3 |f_3(t)|$$
     where $K_2 = |\rho_{12}|$ and $K_3 = |\rho_{13}|$.
   - The correlation coefficients $\rho_{12}$ and $\rho_{13}$ are computed dynamically from the raw time-series data of each wave configuration file.

2. **24-Case Multi-Load Matrix**:
   - Systematically covers 3 wave heights ($H_s = 1.73$ m, $2.16$ m, $2.58$ m) $\times$ 2 directions ($D = 180^\circ$, $90^\circ$) $\times$ 4 time intervals (0, 10, 20, 30 years).
   - Combines the 3-component wave bending moment with static vertical SWBM ($1.5464 \times 10^8$ N.m) and constant ship SWBM ($1.2 \times 10^8$ N.m).

3. **Visualizations & Output Reports**:
   - Added a new subplot showing all three **Raw Wave Bending Moments** (Vertical, Horizontal, Torsional) in their original signed time-series, with consistent colors (blue for Vertical, red for Horizontal, green for Torsional).
   - Re-plotted the **Combined Loads** and their JPDF curves with the new 3-component load profile.
   - Recalculated all reliability indices ($\beta$, FoS, $P_f$) for both Ultimate and Yield strength criteria.

---

## 📈 Key Findings (Yield Strength = 250 MPa)

Below is a summary of the structural reliability indices under the worst-case wave height ($H_s = 2.58$ m) using the 3-component combination:

### Head Wave ($D = 180^\circ$, Vertical Dominant)
| Age (years) | $W_{\text{pantau}}$ ($m^3$) | Mean Stress $\mu_{\sigma_L}$ (MPa) | Std Dev Stress $\sigma_{\sigma_L}$ (MPa) | Safety Factor (FoS) | Safety Index ($\beta$) | Failure Prob ($P_f$) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0** | 3.2292 | 88.1435 | 13.3946 | 2.8363 | 4.2383 | $< 10^{-4}$ |
| **10** | 3.0895 | 92.1290 | 14.0003 | 2.7136 | 4.1107 | $< 10^{-4}$ |
| **20** | 2.9508 | 96.4583 | 14.6582 | 2.5918 | 3.9726 | $< 10^{-4}$ |
| **30** | 2.8132 | 101.1770 | 15.3752 | 2.4709 | 3.8231 | $6.6 \times 10^{-5}$ |

### Beam Wave ($D = 90^\circ$, Horizontal Dominant)
| Age (years) | $W_{\text{pantau}}$ ($m^3$) | Mean Stress $\mu_{\sigma_L}$ (MPa) | Std Dev Stress $\sigma_{\sigma_L}$ (MPa) | Safety Factor (FoS) | Safety Index ($\beta$) | Failure Prob ($P_f$) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0** | 3.2292 | 86.3223 | 11.4783 | 2.8961 | 4.3578 | $< 10^{-4}$ |
| **10** | 3.0895 | 90.2255 | 11.9973 | 2.7708 | 4.2357 | $< 10^{-4}$ |
| **20** | 2.9508 | 94.4653 | 12.5610 | 2.6465 | 4.1033 | $< 10^{-4}$ |
| **30** | 2.8132 | 99.0865 | 13.1755 | 2.5230 | 3.9597 | $3.7 \times 10^{-5}$ |

---

## 🛠️ Verification & Outputs
- **Jupyter Notebook**: [main.ipynb](file:///mnt/GG/Sekolah_Lagi/SEM1/Keandalan-Struktur/1/main.ipynb) compiled and ran all cells successfully.
- **Exported Scantlings CSV**: [scantling_corroded.csv](file:///mnt/GG/Sekolah_Lagi/SEM1/Keandalan-Struktur/1/scantling_corroded.csv) exported with the correct dimensions.
