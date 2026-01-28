"""
Figuras para Paper 2: Kaelion
1. V(λ), V'(λ), V''(λ)
2. f(λ) vs λ con resonancias
3. Estructura de fases
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import matplotlib.patches as mpatches

# Constantes
V0 = np.sqrt(3)
phi0 = 1/np.sqrt(3)

# Funciones
def V(lam):
    return V0 * lam**2 * (1 - lam)**2

def V_prime(lam):
    return 2 * V0 * lam * (1 - lam) * (1 - 2*lam)

def V_double_prime(lam):
    return 2 * V0 * (1 - 6*lam*(1-lam))

def f_lambda(lam, eps=1e-6):
    """f(λ) regularizada"""
    V_dd = np.abs(V_double_prime(lam))
    denom = np.maximum(V_dd / (2*V0), eps)
    return (1 - lam) * (1 + 1/denom)

# Lambda array
lam = np.linspace(0.001, 0.999, 1000)

# ============================================
# FIGURA 1: Potencial y derivadas
# ============================================
fig1, axes = plt.subplots(1, 3, figsize=(14, 4))

# V(λ)
ax1 = axes[0]
ax1.plot(lam, V(lam), 'b-', linewidth=2)
ax1.axhline(y=V0/16, color='r', linestyle='--', alpha=0.5, label=f'Barrier = √3/16 ≈ {V0/16:.3f}')
ax1.axvline(x=0.5, color='gray', linestyle=':', alpha=0.5)
ax1.set_xlabel('λ', fontsize=12)
ax1.set_ylabel('V(λ)', fontsize=12)
ax1.set_title('Effective Potential', fontsize=12)
ax1.legend(fontsize=9)
ax1.grid(True, alpha=0.3)
ax1.set_xlim(0, 1)

# V'(λ)
ax2 = axes[1]
ax2.plot(lam, V_prime(lam), 'g-', linewidth=2)
ax2.axhline(y=0, color='k', linestyle='-', alpha=0.3)
ax2.axvline(x=0.5, color='gray', linestyle=':', alpha=0.5)
# Marcar extremos
lam1 = (3 - np.sqrt(3))/6
lam2 = (3 + np.sqrt(3))/6
ax2.axvline(x=lam1, color='r', linestyle='--', alpha=0.5, label=f'λ₁ = {lam1:.3f}')
ax2.axvline(x=lam2, color='r', linestyle='--', alpha=0.5, label=f'λ₂ = {lam2:.3f}')
ax2.set_xlabel('λ', fontsize=12)
ax2.set_ylabel("V'(λ)", fontsize=12)
ax2.set_title('First Derivative', fontsize=12)
ax2.legend(fontsize=9)
ax2.grid(True, alpha=0.3)
ax2.set_xlim(0, 1)

# V''(λ)
ax3 = axes[2]
ax3.plot(lam, V_double_prime(lam), 'r-', linewidth=2)
ax3.axhline(y=0, color='k', linestyle='-', alpha=0.3)
ax3.axvline(x=lam1, color='orange', linestyle='--', alpha=0.5, label='Inflection points')
ax3.axvline(x=lam2, color='orange', linestyle='--', alpha=0.5)
ax3.set_xlabel('λ', fontsize=12)
ax3.set_ylabel("V''(λ)", fontsize=12)
ax3.set_title('Second Derivative (Curvature)', fontsize=12)
ax3.legend(fontsize=9)
ax3.grid(True, alpha=0.3)
ax3.set_xlim(0, 1)

plt.tight_layout()
plt.savefig('/home/claude/fig_paper2_potential.png', dpi=150, bbox_inches='tight')
plt.close()

# ============================================
# FIGURA 2: f(λ) con resonancias
# ============================================
fig2, ax = plt.subplots(figsize=(10, 6))

# f(λ) regularizada
f_vals = f_lambda(lam, eps=0.01)
f_vals_clipped = np.clip(f_vals, 0, 10)  # Clip para visualización

ax.plot(lam, f_vals_clipped, 'b-', linewidth=2, label='f(λ) = (1-λ)[1 + 1/max(|V\'\'|/2V₀, ε)]')

# Marcar resonancias
ax.axvline(x=lam1, color='r', linestyle='--', linewidth=2, label=f'λ₁ = {lam1:.3f} (resonance)')
ax.axvline(x=lam2, color='r', linestyle='--', linewidth=2, label=f'λ₂ = {lam2:.3f} (resonance)')

# Regiones
ax.axvspan(0, lam1, alpha=0.1, color='blue', label='LQG stable')
ax.axvspan(lam1, lam2, alpha=0.1, color='yellow', label='Transition')
ax.axvspan(lam2, 1, alpha=0.1, color='green', label='Holographic stable')

ax.set_xlabel('λ', fontsize=14)
ax.set_ylabel('f(λ)', fontsize=14)
ax.set_title('Thermality Correction Function with Resonances', fontsize=14)
ax.legend(loc='upper right', fontsize=10)
ax.grid(True, alpha=0.3)
ax.set_xlim(0, 1)
ax.set_ylim(0, 8)

plt.tight_layout()
plt.savefig('/home/claude/fig_paper2_f_lambda.png', dpi=150, bbox_inches='tight')
plt.close()

# ============================================
# FIGURA 3: Estructura de fases
# ============================================
fig3, ax = plt.subplots(figsize=(12, 6))

# Fondo de fases
ax.axvspan(0, lam1, alpha=0.3, color='#3498db', label='LQG Phase (λ → 0)')
ax.axvspan(lam1, lam2, alpha=0.3, color='#f39c12', label='Critical/Transition')
ax.axvspan(lam2, 1, alpha=0.3, color='#2ecc71', label='Holographic Phase (λ → 1)')

# Potencial escalado para visualización
V_scaled = V(lam) / V(0.5) * 2
ax.plot(lam, V_scaled, 'k-', linewidth=3, label='V(λ) (scaled)')

# Puntos críticos
ax.plot(0, 0, 'bo', markersize=15, label='λ=0: LQG minimum')
ax.plot(1, 0, 'go', markersize=15, label='λ=1: Holographic minimum')
ax.plot(0.5, 2, 'r^', markersize=15, label='λ=0.5: Barrier maximum')

# Anotaciones
ax.annotate('α = -1/2\n(Kaul-Majumdar)', xy=(0.05, 0.5), fontsize=11, 
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
ax.annotate('α = -3/2\n(Sen)', xy=(0.85, 0.5), fontsize=11,
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
ax.annotate('α = -1\n(Critical)', xy=(0.45, 2.5), fontsize=11,
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

# Flechas de flujo RG
ax.annotate('', xy=(0.3, 3.5), xytext=(0.7, 3.5),
            arrowprops=dict(arrowstyle='<->', color='purple', lw=2))
ax.text(0.5, 3.7, 'RG Flow (c = 2π)', ha='center', fontsize=11, color='purple')

ax.set_xlabel('λ (Information Accessibility)', fontsize=14)
ax.set_ylabel('Energy / Scaled Potential', fontsize=14)
ax.set_title('Phase Structure of the Kaelion Framework', fontsize=14)
ax.legend(loc='upper left', fontsize=9, ncol=2)
ax.set_xlim(-0.05, 1.05)
ax.set_ylim(-0.5, 4.5)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/home/claude/fig_paper2_phases.png', dpi=150, bbox_inches='tight')
plt.close()

# ============================================
# FIGURA 4: Perfil radial λ(r)
# ============================================
fig4, ax = plt.subplots(figsize=(10, 6))

# Parámetros
r_h = 1  # Horizon radius (normalized)
w = 0.54  # Transition width in Planck units

r = np.linspace(r_h, r_h + 5*w, 500)
lambda_r = np.exp(-(r - r_h)/w)

ax.plot(r, lambda_r, 'b-', linewidth=2.5)
ax.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5, label='λ = 0.5 (transition)')
ax.axhline(y=1, color='green', linestyle=':', alpha=0.5)
ax.axhline(y=0, color='blue', linestyle=':', alpha=0.5)

# Marcar regiones
ax.axvspan(r_h, r_h + w, alpha=0.2, color='red', label=f'Transition region (w ≈ 0.54 ℓ_P)')

# Anotaciones
ax.annotate('Horizon\n(Holographic)', xy=(r_h, 1), xytext=(r_h + 0.3, 0.85),
            fontsize=11, arrowprops=dict(arrowstyle='->', color='green'))
ax.annotate('Asymptotic\n(LQG)', xy=(r_h + 3*w, 0.05), xytext=(r_h + 2.5*w, 0.25),
            fontsize=11, arrowprops=dict(arrowstyle='->', color='blue'))

ax.set_xlabel('r - r_h (Planck units)', fontsize=14)
ax.set_ylabel('λ(r)', fontsize=14)
ax.set_title('Radial Profile: λ(r) = exp(-(r-r_h)/w)', fontsize=14)
ax.legend(loc='upper right', fontsize=10)
ax.grid(True, alpha=0.3)
ax.set_xlim(r_h - 0.1, r_h + 4*w)
ax.set_ylim(-0.05, 1.1)

plt.tight_layout()
plt.savefig('/home/claude/fig_paper2_radial.png', dpi=150, bbox_inches='tight')
plt.close()

print("✓ Figuras generadas:")
print("  - fig_paper2_potential.png (V, V', V'')")
print("  - fig_paper2_f_lambda.png (f(λ) con resonancias)")
print("  - fig_paper2_phases.png (estructura de fases)")
print("  - fig_paper2_radial.png (perfil radial λ(r))")
