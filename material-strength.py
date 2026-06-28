import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Data A36 Ultimate Strength (MPa)
data = np.array([
    355.504, 439.795, 472.011, 263.955, 376.981, 342.362,
    478.974, 484.172, 485.152,
    360.7, 400.4, 468.2, 426.9, 363.9, 391.1,
    462.3, 435.7, 355.7, 401.1, 472.0, 418.0
])

# Statistik
mean = np.mean(data)
std  = np.std(data, ddof=1)   # ddof=1 → sample std deviation
n    = len(data)

print(f"Jumlah data (n)     : {n}")
print(f"Rata-rata (μ)       : {mean:.3f} MPa")
print(f"Std. Deviasi (σ)    : {std:.3f} MPa")

# Plot
x = np.linspace(mean - 4*std, mean + 4*std, 500)
pdf = norm.pdf(x, mean, std)

fig, ax = plt.subplots(figsize=(9, 5))

# Histogram (dinormalisasi ke density)
ax.hist(data, bins=8, density=True,
        color='#5DCAA5', edgecolor='#0F6E56', alpha=0.55,
        label='Histogram data')

# Kurva PDF
ax.plot(x, pdf, color='#185FA5', linewidth=2.5,
        label=f'PDF Normal\nμ = {mean:.2f} MPa\nσ = {std:.2f} MPa')

# Garis vertikal mean
ax.axvline(mean, color='#D85A30', linestyle='--', linewidth=1.5,
           label=f'Mean = {mean:.2f} MPa')

# Label & format
ax.set_xlabel('Ultimate Strength (MPa)', fontsize=13)
ax.set_ylabel('Probability Density', fontsize=13)
ax.set_title('A36 Steel Ultimate Strength Probability Density Function', fontsize=14)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.25)

plt.tight_layout()
plt.savefig('pdf_a36.png', dpi=150)
plt.show()